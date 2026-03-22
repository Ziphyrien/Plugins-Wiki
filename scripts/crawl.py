#!/usr/bin/env python3
"""
Wiki documentation crawler CLI.
"""
import argparse
import logging
import shutil
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
PROJECT_ROOT = SCRIPT_DIR.parent.resolve()

CRAWLER_MAP = {
    "gitbook": GitBookCrawler,
    "retype": RetypeCrawler,
}


def resolve_output_dir(config: dict) -> Path | None:
    """Resolve and validate output_dir relative to the project root."""
    raw_output_dir = str(config.get("output_dir", "")).strip()
    if not raw_output_dir:
        logger.error("配置缺少 output_dir")
        return None

    output_dir = (PROJECT_ROOT / raw_output_dir).resolve()

    try:
        output_dir.relative_to(PROJECT_ROOT)
    except ValueError:
        logger.error(f"output_dir 超出项目目录: {output_dir}")
        return None

    return output_dir


def create_staging_dir(output_dir: Path) -> Path:
    """Create a clean staging directory next to the final output directory."""
    staging_dir = output_dir.parent / f".{output_dir.name}.staging"
    if staging_dir.exists():
        shutil.rmtree(staging_dir)
    staging_dir.mkdir(parents=True, exist_ok=True)
    return staging_dir


def publish_staging_dir(staging_dir: Path, output_dir: Path) -> None:
    """Atomically replace the final output directory with staged content."""
    if output_dir.exists():
        shutil.rmtree(output_dir)
    staging_dir.rename(output_dir)


def run_crawler(name: str, config: dict) -> tuple[int, int]:
    """Run a crawler for the given wiki config."""
    crawler_type = config.get("type")
    crawler_class = CRAWLER_MAP.get(crawler_type)

    if not crawler_class:
        logger.error(f"未知爬虫类型: {crawler_type}")
        return 0, 1

    output_dir = resolve_output_dir(config)
    if output_dir is None:
        return 0, 1

    staging_dir = create_staging_dir(output_dir)
    logger.info(f"输出目录: {output_dir.relative_to(PROJECT_ROOT)}")

    crawl_config = config.copy()
    crawl_config["output_dir"] = staging_dir

    crawler = crawler_class(name, crawl_config)

    try:
        success, failed = crawler.run()

        if success == 0 and failed == 0:
            logger.error("未抓取到任何页面，保留现有输出目录")
            return 0, 1

        if failed > 0:
            logger.error("存在抓取失败页面，保留现有输出目录")
            return success, failed

        publish_staging_dir(staging_dir, output_dir)
        logger.info(f"📦 已发布到: {output_dir.relative_to(PROJECT_ROOT)}")
        return success, failed
    finally:
        if staging_dir.exists():
            shutil.rmtree(staging_dir)


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
