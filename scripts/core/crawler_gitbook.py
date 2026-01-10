import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from .markdown_utils import process_markdown

class GitBookCrawler:
    def __init__(self, name, config, project_root):
        self.name = name
        self.config = config
        self.project_root = project_root
        self.sitemap_url = config["sitemap_url"]
        self.base_url = config["base_url"]
        # output_dir is already absolute from crawl.py
        self.output_dir = config["output_dir"]

    def fetch_sitemap(self, url):
        print(f"正在获取 sitemap: {url}...")
        response = requests.get(url)
        response.raise_for_status()
        return response.content

    def parse_sitemap(self, xml_content):
        root = ET.fromstring(xml_content)
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        items = []
        for url in root.findall('ns:url', namespace):
            loc = url.find('ns:loc', namespace).text
            # decode URL encoding
            loc = requests.utils.unquote(loc)
            lastmod_elem = url.find('ns:lastmod', namespace)
            lastmod = lastmod_elem.text if lastmod_elem is not None else None
            items.append({'loc': loc, 'lastmod': lastmod})
        return items

    def download_file(self, url, local_path, title, order):
        """
        下载文件
        """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                content_str = response.content.decode('utf-8')
                
                # Apply Starlight transformations
                final_content = process_markdown(content_str, local_path, title, order)
                final_content_bytes = final_content.encode('utf-8')
                
                is_new = not os.path.exists(local_path)
                
                # Check for existing content
                if not is_new:
                    try:
                        with open(local_path, 'rb') as f:
                            local_content = f.read()
                        if local_content == final_content_bytes:
                            return False # No change
                    except:
                        pass # Read failed, plain overwrite
                
                # Save file
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                with open(local_path, 'wb') as f:
                    f.write(final_content_bytes)
                
                rel_path = os.path.relpath(local_path, self.output_dir)
                if not is_new:
                    print(f"    ✅ 更新: {rel_path}")
                else:
                    print(f"    🆕 新增: {rel_path}")
                
                return True
            else:
                print(f"    [失败] {url} 状态码 {response.status_code}")
                return False
        except Exception as e:
            print(f"    [错误] {url}: {e}")
            return False

    def run(self):
        print("="*60)
        print(f"文档同步工具 - {self.name} (GitBook)")
        print("="*60 + "\n")
        
        try:
            xml_content = self.fetch_sitemap(self.sitemap_url)
            items = self.parse_sitemap(xml_content)
            
            print(f"\n📄 Sitemap 中发现 {len(items)} 个页面\n")
            print("-"*60)
            
            updated_count = 0
            
            # 记录本次处理的文件路径，用于检测删除
            processed_files = set()
            
            # Map items to order based on appearance in sitemap
            # GitBook sitemap usually reflects structure order? Not always guaranteed but best guess.
            
            # Remove base url components to sort or match
            base_domain = self.base_url.replace("https://", "").replace("http://", "").rstrip('/')
            
            # Sort items by URL length/depth might help, but let's just use index as order for now
            # Or text processing later
            
            for index, item in enumerate(items):
                page_url = item['loc']
                
                # Determine title from URL last segment (fallback)
                # GitBook crawler fetches raw HTML usually? 
                # This download_file assumes raw markdown download?
                # GitBook sitemap usually points to HTML pages.
                # If we are downloading raw markdown, we need the markdown URL.
                # Standard GitBook (v2) exposed git repo. Modern GitBook is SaaS.
                # If this is SaaS gitbook, requests.get(loc) returns HTML.
                # If the user's config points to a site, we might need to parse HTML like ReType.
                
                # WAIT: The original code just did `requests.get(url)`. 
                # If the URL is an HTML page, it saved HTML to .md file?
                # That would be bad. The original code seemed to assume content IS markdown 
                # or the response content is directly usable.
                # GitBook SaaS doesn't give raw MD easily without API.
                # Assuming the original crawler logic worked (fetching content), 
                # I will stick to it but just adding the transform.
                
                # Generate title
                path_segments = page_url.split('/')
                slug = path_segments[-1] or path_segments[-2]
                title = slug.replace('-', ' ').title()
                
                # 确定目标 URL 和本地路径
                if page_url.rstrip('/') == self.base_url.rstrip('/'):
                    target_url = f"{self.base_url}/welcome.md"
                    local_path = os.path.join(self.output_dir, "welcome.md")
                    title = "Welcome"
                else:
                    if page_url.endswith('/'):
                        page_url = page_url[:-1]
                    
                    # Original logic was appending .md directly to URL?
                    target_url = f"{page_url}.md"
                    rel_path = page_url.replace(self.base_url, '').lstrip('/')
                    local_path = os.path.join(self.output_dir, f"{rel_path}.md")
                
                processed_files.add(os.path.abspath(local_path))
                
                # Pass index+1 as order
                if self.download_file(target_url, local_path, title, index + 1):
                    updated_count += 1
            
            # 删除旧文件
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
            print(f"   🔄 更新/新增: {updated_count}")
            print(f"   🗑️  删除: {deleted_count}")
                
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            # import traceback
            # traceback.print_exc()
