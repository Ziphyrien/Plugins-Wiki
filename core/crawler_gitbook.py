import os
import requests
import xml.etree.ElementTree as ET
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
                
                # Save file
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                with open(local_path, 'wb') as f:
                    f.write(final_content_bytes)
                
                rel_path = os.path.relpath(local_path, self.output_dir)
                print(f"    ✅ 下载: {rel_path}")
                
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
            
            for index, item in enumerate(items):
                page_url = item['loc']
                
                # Determine title from URL last segment (fallback)
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
                    
                    target_url = f"{page_url}.md"
                    rel_path = page_url.replace(self.base_url, '').lstrip('/')
                    local_path = os.path.join(self.output_dir, f"{rel_path}.md")
                
                # Pass index+1 as order
                self.download_file(target_url, local_path, title, index + 1)

            print("\n" + "-"*60)
            print(f"\n📊 同步完成")
                
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")