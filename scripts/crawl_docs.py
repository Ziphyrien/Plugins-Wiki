"""
文档爬取工具
集成版本控制系统，跟踪原文时间、变更时间和汉化状态
"""

import os
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from datetime import datetime, timezone
from version_control import VersionControl

SITEMAP_URL = "https://mythicprefixes.superiormc.cn/sitemap-pages.xml"
BASE_URL = "https://mythicprefixes.superiormc.cn"

# 获取项目根目录 (scripts 的上级目录)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "docs")

def fetch_sitemap(url):
    print(f"正在获取 sitemap: {url}...")
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def parse_sitemap(xml_content):
    root = ET.fromstring(xml_content)
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    items = []
    for url in root.findall('ns:url', namespace):
        loc = url.find('ns:loc', namespace).text
        lastmod_elem = url.find('ns:lastmod', namespace)
        lastmod = lastmod_elem.text if lastmod_elem is not None else None
        items.append({'loc': loc, 'lastmod': lastmod})
    return items

def parse_date(date_str):
    if not date_str:
        return None
    try:
        if date_str.endswith('Z'):
            date_str = date_str[:-1] + '+00:00'
        return datetime.fromisoformat(date_str)
    except ValueError:
        return None

def download_file(url, local_path, vc: VersionControl, lastmod: str = None):
    """
    下载文件并注册到版本控制
    """
    print(f"  正在下载: {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.content
            
            # 检查文件是否有变化
            rel_path = os.path.relpath(local_path, PROJECT_ROOT)
            existing_info = vc.get_file_info(rel_path)
            
            if existing_info:
                current_hash = vc.compute_hash(content)
                if existing_info["original_hash"] == current_hash:
                    print(f"    [跳过] 内容无变化")
                    return False
            
            # 保存文件
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(content)
            
            # 注册到版本控制
            vc.register_original(rel_path, content, lastmod)
            return True
        else:
            print(f"    [失败] 状态码 {response.status_code}")
            return False
    except Exception as e:
        print(f"    [错误] {e}")
        return False

def main():
    print("="*60)
    print("文档同步工具")
    print("="*60 + "\n")
    
    # 初始化版本控制 (使用项目根目录)
    vc = VersionControl(PROJECT_ROOT)
    
    try:
        xml_content = fetch_sitemap(SITEMAP_URL)
        items = parse_sitemap(xml_content)
        
        print(f"\n📄 Sitemap 中发现 {len(items)} 个页面\n")
        print("-"*60)
        
        new_count = 0
        updated_count = 0
        skipped_count = 0
        
        # 记录本次处理的文件路径，用于检测删除
        processed_files = set()

        for item in items:
            page_url = item['loc']
            lastmod = item['lastmod']
            
            # 确定目标 URL 和本地路径
            if page_url.rstrip('/') == BASE_URL.rstrip('/'):
                target_url = f"{BASE_URL}/welcome.md"
                local_path = os.path.join(OUTPUT_DIR, "welcome.md")
            else:
                if page_url.endswith('/'):
                    page_url = page_url[:-1]
                
                target_url = f"{page_url}.md"
                rel_path = page_url.replace(BASE_URL, '').lstrip('/')
                local_path = os.path.join(OUTPUT_DIR, f"{rel_path}.md")
            
            rel_path = os.path.relpath(local_path, PROJECT_ROOT)
            processed_files.add(rel_path)
            
            existing_info = vc.get_file_info(rel_path)
            
            if existing_info is None:
                # 新文件
                print(f"🆕 新文件: {rel_path}")
                if download_file(target_url, local_path, vc, lastmod):
                    new_count += 1
            else:
                # 如果文件之前被标记为删除，现在又出现了，恢复它
                if existing_info.get("status") == "deleted":
                    vc.restore_file(rel_path)

                # 检查是否需要更新（基于 lastmod）
                remote_dt = parse_date(lastmod)
                original_dt = parse_date(existing_info.get("original_modified"))
                
                should_check = False
                if remote_dt and original_dt:
                    if remote_dt > original_dt:
                        should_check = True
                        print(f"⚡ 检测到更新 ({lastmod}): {rel_path}")
                elif lastmod:
                    # 有新的 lastmod 但没有记录，检查内容
                    should_check = True
                
                if should_check:
                    if download_file(target_url, local_path, vc, lastmod):
                        updated_count += 1
                    else:
                        skipped_count += 1
                else:
                    print(f"⏭️  跳过 (无更新): {rel_path}")
                    skipped_count += 1
        
        # 检测已删除的文件
        all_tracked_files = set(vc.metadata["files"].keys())
        deleted_files = all_tracked_files - processed_files
        
        if deleted_files:
            print("\n" + "-"*60)
            print("🗑️  检测到以下文件已从 Sitemap 中移除:")
            for deleted_path in deleted_files:
                # 忽略已经被标记为删除的文件
                if vc.get_file_info(deleted_path).get("status") != "deleted":
                    print(f"   - {deleted_path}")
                    vc.mark_file_deleted(deleted_path)

        print("\n" + "-"*60)
        print(f"\n📊 同步完成:")
        print(f"   🆕 新增: {new_count}")
        print(f"   🔄 更新: {updated_count}")
        print(f"   ⏭️  跳过: {skipped_count}")
        if deleted_files:
            print(f"   🗑️  删除: {len(deleted_files)}")
        
        # 打印版本控制摘要
        vc.print_summary()
            
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
