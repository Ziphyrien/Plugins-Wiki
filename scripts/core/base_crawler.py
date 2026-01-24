"""
Base crawler class with common functionality.
"""
from abc import ABC, abstractmethod
from pathlib import Path
import logging
import requests


logger = logging.getLogger(__name__)


class BaseCrawler(ABC):
    """Abstract base class for all wiki crawlers."""

    def __init__(self, name: str, config: dict, content_root: Path):
        self.name = name
        self.config = config
        self.content_root = Path(content_root)
        self.base_url = config["base_url"].rstrip("/")
        self.output_dir = Path(config["output_dir"])
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Plugins-Wiki-Crawler/1.0"
        })

    @abstractmethod
    def fetch_pages(self) -> list[dict]:
        """Fetch the list of pages to crawl. Returns list of page info dicts."""
        pass

    @abstractmethod
    def process_page(self, page: dict, order: int) -> bool:
        """Process a single page. Returns True on success."""
        pass

    def run(self) -> tuple[int, int]:
        """
        Main entry point. Returns (success_count, fail_count).
        """
        logger.info("=" * 60)
        logger.info(f"文档同步工具 - {self.name} ({self.__class__.__name__})")
        logger.info("=" * 60)

        try:
            pages = self.fetch_pages()
            total = len(pages)
            logger.info(f"📄 发现 {total} 个页面")
            logger.info("-" * 60)

            success, failed = 0, 0
            for idx, page in enumerate(pages, start=1):
                if self.process_page(page, order=idx):
                    success += 1
                else:
                    failed += 1

            logger.info("-" * 60)
            logger.info(f"📊 同步完成: {success} 成功, {failed} 失败")
            return success, failed

        except Exception as e:
            logger.exception(f"❌ 爬取过程中发生错误: {e}")
            return 0, 0

    def download(self, url: str) -> requests.Response | None:
        """Helper to download a URL with error handling."""
        try:
            resp = self.session.get(url, timeout=30)
            resp.raise_for_status()
            return resp
        except requests.RequestException as e:
            logger.warning(f"下载失败 {url}: {e}")
            return None

    def save_file(self, path: Path, content: str) -> None:
        """Save content to file, creating directories as needed."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        rel_path = path.relative_to(self.output_dir) if self.output_dir in path.parents or path.parent == self.output_dir else path.name
        logger.info(f"    ✅ 保存: {rel_path}")
