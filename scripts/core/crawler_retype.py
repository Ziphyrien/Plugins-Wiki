import os
import re
import json
import requests
from urllib.parse import urljoin
from email.utils import parsedate_to_datetime
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
from .markdown_utils import process_markdown

def retype_language_callback(el):
    code_elem = el.find('code')
    if code_elem and code_elem.get('class'):
        for c in code_elem.get('class'):
            if c.startswith('language-'):
                return c.replace('language-', '')
    
    # Also check pre tag itself for language- class
    if el.get('class'):
         for c in el.get('class'):
            if c.startswith('language-'):
                return c.replace('language-', '')
    return None

class RetypeConverter(MarkdownConverter):
    def __init__(self, crawler, page_url, current_file_path, **options):
        super().__init__(**options)
        self.crawler = crawler
        self.page_url = page_url
        self.current_file_path = current_file_path

    def convert_a(self, el, text, parent_tags):
        href = el.get('href', '')
        href = self.crawler.resolve_link(href, self.page_url, self.current_file_path)
        return f"[{text.strip()}]({href})"

    def convert_svg(self, el, text, parent_tags):
        # Retype uses inline SVGs for icons. 
        # For now we suppress them to avoid weird text artifacts or giant SVG codes if markdownify tried to process internals.
        # If we identified specific icons (like 'home'), we could map to emojis.
        return ""

    def convert_i(self, el, text, parent_tags):
        # Suppress icon fonts to avoid empty spaces or garbled text
        return ""

    def convert_div(self, el, text, parent_tags):
        classes = el.get('class', []) or []
        
        if 'doc-callout' in classes:
            alert_type = "NOTE"
            icon_div = el.find('div', recursive=False)
            if icon_div:
                svg = icon_div.find('svg')
                if svg:
                    svg_classes = svg.get('class', [])
                    for c in svg_classes:
                        if c.startswith('text-callout-'):
                            t = c.replace('text-callout-', '')
                            if t == 'warning': alert_type = "WARNING"
                            elif t == 'danger': alert_type = "CAUTION"
                            elif t == 'success': alert_type = "TIP"
                            elif t == 'primary': alert_type = "NOTE"
                            break
            
            content_divs = el.find_all('div', recursive=False)
            if content_divs:
                content_div = content_divs[-1]
                inner_md = self.convert_soup(content_div)
                lines = inner_md.strip().split('\n')
                quoted_lines = [f"> {line}" for line in lines]
                return f"\n> [!{alert_type}]\n" + "\n".join(quoted_lines) + "\n\n"
            
            return text

        return text

    def convert_span(self, el, text, parent_tags):
        classes = el.get('class', []) or []
        if any('badge-' in c for c in classes):
             return f"`{el.get_text().strip()}`"
        return text

    def convert_img(self, el, text, parent_tags):
        alt = el.get('alt', '')
        src = el.get('src', '')
        return f"![{alt}]({src})"

class RetypeCrawler:
    def __init__(self, name, config, project_root):
        self.name = name
        self.config = config
        self.project_root = project_root
        self.base_url = config["base_url"]
        self.config_url = config["config_url"]
        self.output_dir = os.path.join(project_root, config["output_dir"])

    def get_site_structure(self):
        print(f"正在获取站点配置: {self.config_url}...")
        try:
            response = requests.get(self.config_url)
            response.raise_for_status()
            content = response.text
            match = re.search(r"var __DOCS_CONFIG__ = ({.*})", content)
            if match:
                config_json = match.group(1)
                config_json = re.sub(r',\s*}', '}', config_json)
                config_json = re.sub(r',\s*]', ']', config_json)
                try:
                    config = json.loads(config_json)
                    return config
                except json.JSONDecodeError:
                    print(f"JSON 解析错误，尝试简单修复...")
                    return None
            else:
                print("未找到配置对象")
                return None
        except Exception as e:
            print(f"获取配置失败: {e}")
            return None

    def parse_sidebar(self, sidebar, parent_path=""):
        pages = []
        for item in sidebar:
            n = item.get('n', '')
            if n.startswith('/'):
                path = n.lstrip('/')
            else:
                path = os.path.join(parent_path, n).replace("\\", "/")
            has_children = 'i' in item
            if has_children:
                pages.extend(self.parse_sidebar(item['i'], path))
            if not n and 'l' in item:
                 continue
            if path == "":
                url = self.base_url
                file_path = "welcome.md"
            else:
                url = f"{self.base_url}{path}/"
                file_path = f"{path}.md"
            pages.append({
                'url': url,
                'rel_path': file_path,
                'has_children': has_children
            })
        return pages

    def resolve_link(self, href, page_url, current_file_path):
        if not href: return href
        if href.startswith('#'): return href
        full_url = urljoin(page_url, href)
        if not full_url.startswith(self.base_url): return href
        rel_url = full_url[len(self.base_url):]
        anchor = ""
        if '#' in rel_url:
            rel_url, anchor = rel_url.split('#', 1)
            anchor = '#' + anchor
        if rel_url == "" or rel_url == "/":
            target_file_path = "welcome.md"
        else:
            path_part = rel_url.lstrip('/')
            if path_part.endswith('/'): path_part = path_part.rstrip('/')
            elif not os.path.splitext(path_part)[1]: pass
            target_file_path = f"{path_part}.md"
        start_dir = os.path.dirname(current_file_path)
        try:
            rel_link = os.path.relpath(target_file_path, start_dir)
            rel_link = rel_link.replace('\\', '/')
            return rel_link + anchor
        except ValueError:
            return href

    def process_page(self, url, rel_path, has_children=False, order=None):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                content_div = soup.find('div', id='retype-content')
                
                if content_div:
                    for tag in content_div.find_all(['doc-anchor-trigger', 'doc-sidebar-right', 'doc-toolbar-member-filter-no-results']):
                        tag.decompose()
                    toggle = content_div.find(id='retype-sidebar-right-toggle')
                    if toggle: toggle.decompose()

                    converter = RetypeConverter(
                        crawler=self, 
                        page_url=url, 
                        current_file_path=rel_path,
                        heading_style="ATX",
                        code_language_callback=retype_language_callback
                    )
                    md_content = converter.convert_soup(content_div)
                    
                    # Extract title from H1 if present, else fallback
                    title = "Untitled"
                    h1 = content_div.find('h1')
                    if h1:
                        title = h1.get_text().strip()
                        # Markdownify might leave H1 in content, frontmatter also sets title.
                        # Starlight might duplicate if we keep H1.
                        # For now, let's keep H1 in body as process_markdown just adds frontmatter.
                        # Ideally we strip H1 from body if it matches title.
                    else:
                        base = os.path.basename(rel_path)
                        title = os.path.splitext(base)[0].replace('-', ' ').title()

                    # Apply Starlight transformations
                    local_path = os.path.join(self.output_dir, rel_path)
                    final_content = process_markdown(md_content, local_path, title, order)
                    content_bytes = final_content.encode('utf-8')
                    
                    is_new = not os.path.exists(local_path)
                    if not is_new:
                        try:
                            with open(local_path, 'rb') as f:
                                local_content = f.read()
                            if local_content == content_bytes:
                                return True # No change
                        except: pass

                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    with open(local_path, 'wb') as f:
                        f.write(content_bytes)
                    
                    rel_path_disp = os.path.relpath(local_path, self.output_dir)
                    if not is_new:
                        print(f"    ✅ 更新: {rel_path_disp}")
                    else:
                        print(f"    🆕 新增: {rel_path_disp}")
                    return True
                else:
                    print(f"    [警告] {rel_path}: 未找到内容区域")
                    return False
            else:
                if not (has_children and response.status_code in [403, 404]):
                     print(f"    [失败] {rel_path}: 状态码 {response.status_code}")
                return False
        except Exception as e:
            print(f"    [错误] {rel_path}: {e}")
            # import traceback
            # traceback.print_exc()
            return False

    def run(self):
        print("="*60)
        print(f"文档同步工具 - {self.name} (Retype)")
        print("="*60 + "\n")
        
        config = self.get_site_structure()
        if not config or 'sidebar' not in config:
            print("配置错误")
            return

        pages = self.parse_sidebar(config['sidebar'])
        print(f"\n📄 发现 {len(pages)} 个页面\n")
        print("-"*60)
        
        updated_count = 0
        processed_files = set()
        
        for index, page in enumerate(pages):
            url = page['url']
            rel_path = page['rel_path']
            has_children = page.get('has_children', False)
            
            local_path = os.path.join(self.output_dir, rel_path)
            processed_files.add(os.path.abspath(local_path))
            
            # Use index + 1 as order
            if self.process_page(url, rel_path, has_children, index + 1):
                updated_count += 1


        # Delete old files
        deleted_count = 0
        if os.path.exists(self.output_dir):
            for root, dirs, files in os.walk(self.output_dir):
                for file in files:
                    if not file.endswith('.md'):
                        continue
                    full_path = os.path.join(root, file)
                    if os.path.abspath(full_path) not in processed_files:
                        print(f"    🗑️  删除: {os.path.relpath(full_path, self.output_dir)}")
                        try:
                            os.remove(full_path)
                            deleted_count += 1
                        except Exception as e:
                            print(f"    [删除失败] {e}")

        print("\n" + "-"*60)
        print(f"\n📊 同步完成:")
        print(f"   🔄 更新/新增/检查: {updated_count}")
        print(f"   🗑️  删除: {deleted_count}")
