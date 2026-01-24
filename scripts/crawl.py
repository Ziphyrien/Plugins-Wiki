#!/usr/bin/env python3
"""
Wiki documentation crawler CLI.
"""
import argparse
import logging
import sys
from pathlib import Path

from wiki_configs import WIKI_CONFIGS
from core.crawler_gitbook import GitBookCrawler
from core.crawler_retype import RetypeCrawler


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONTENT_ROOT = PROJECT_ROOT.parent / "content"

CRAWLER_MAP = {
    "gitbook": GitBookCrawler,
    "retype": RetypeCrawler,
}


def run_crawler(name: str, config: dict) -> tuple[int, int]:
    """Run a crawler for the given wiki config."""
    crawler_type = config.get("type")
    crawler_class = CRAWLER_MAP.get(crawler_type)

    if not crawler_class:
        logger.error(f"未知爬虫类型: {crawler_type}")
        return 0, 0

    # Resolve output_dir relative to PROJECT_ROOT
    raw_output_dir = config.get("output_dir", "")
    abs_output_dir = (PROJECT_ROOT / raw_output_dir).resolve()

    crawl_config = config.copy()
    crawl_config["output_dir"] = abs_output_dir

    crawler = crawler_class(name, crawl_config, CONTENT_ROOT)
    return crawler.run()


def main():
    parser = argparse.ArgumentParser(
        description="Wiki 文档爬取工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "wiki",
        nargs="?",
        help="要爬取的 Wiki 名称，输入 'all' 爬取所有",
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="列出所有可用的 Wiki 配置",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="显示详细日志",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.list:
        print("可用的 Wiki 配置:")
        for name, cfg in WIKI_CONFIGS.items():
            print(f"  - {name} ({cfg['type']})")
        return 0

    if not args.wiki:
        parser.print_help()
        return 1

    total_success, total_failed = 0, 0

    if args.wiki == "all":
        for name, config in WIKI_CONFIGS.items():
            success, failed = run_crawler(name, config)
            total_success += success
            total_failed += failed
    elif args.wiki in WIKI_CONFIGS:
        total_success, total_failed = run_crawler(args.wiki, WIKI_CONFIGS[args.wiki])
    else:
        logger.error(f"错误: 找不到名为 '{args.wiki}' 的 Wiki 配置")
        logger.info("使用 --list 查看可用配置")
        return 1

    print(f"\n总计: {total_success} 成功, {total_failed} 失败")
    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
