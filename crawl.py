import argparse
import os
import sys
from wiki_configs import WIKI_CONFIGS
from core.crawler_gitbook import GitBookCrawler
from core.crawler_retype import RetypeCrawler

# Get project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = SCRIPT_DIR
# Assume content root is sibling to main
CONTENT_ROOT = os.path.join(os.path.dirname(PROJECT_ROOT), "content")

def run_crawler(name, config):
    crawler_type = config.get("type")
    
    # Inject output_dir base on content root if relative
    # Actually wiki_configs.json has "../content/en/..."
    # We should resolve that to absolute path
    
    raw_output_dir = config.get("output_dir")
    # Resolve relative to main/scripts/ (where we run) or main/ (Project Root)
    # The config has "../content/en/...", which is relative to main/
    abs_output_dir = os.path.abspath(os.path.join(PROJECT_ROOT, raw_output_dir))
    
    crawl_config = config.copy()
    crawl_config["output_dir"] = abs_output_dir
    
    if crawler_type == "gitbook":
        crawler = GitBookCrawler(name, crawl_config, CONTENT_ROOT)
        crawler.run()
    elif crawler_type == "retype":
        crawler = RetypeCrawler(name, crawl_config, CONTENT_ROOT)
        crawler.run()
    else:
        print(f"未知爬虫类型: {crawler_type}")

def main():
    parser = argparse.ArgumentParser(description="Wiki 文档爬取工具")
    parser.add_argument("wiki", nargs="?", help="要爬取的 Wiki 名称 (在 wiki_configs.py 中定义)，输入 'all' 爬取所有")
    parser.add_argument("-l", "--list", action="store_true", help="列出所有可用的 Wiki")
    
    args = parser.parse_args()
    
    if args.list:
        print("可用的 Wiki 配置:")
        for name in WIKI_CONFIGS:
            print(f"  - {name} ({WIKI_CONFIGS[name]['type']})")
        return

    if not args.wiki:
        parser.print_help()
        return

    if args.wiki == "all":
        for name, config in WIKI_CONFIGS.items():
            run_crawler(name, config)
        
    elif args.wiki in WIKI_CONFIGS:
        run_crawler(args.wiki, WIKI_CONFIGS[args.wiki])
    else:
        print(f"错误: 找不到名为 '{args.wiki}' 的 Wiki 配置。")
        print("使用 --list 查看可用配置。")

if __name__ == "__main__":
    main()
