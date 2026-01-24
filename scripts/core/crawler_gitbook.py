"""
GitBook crawler implementation.
"""
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote
import logging

from .base_crawler import BaseCrawler
from .markdown_utils import process_markdown


logger = logging.getLogger(__name__)


class GitBookCrawler(BaseCrawler):
    """Crawler for GitBook-based wikis using sitemap."""

    def __init__(self, name: str, config: dict, content_root: Path):
        super().__init__(name, config, content_root)
        self.sitemap_url = config["sitemap_url"]

    def fetch_pages(self) -> list[dict]:
        """Fetch pages from sitemap XML."""
        logger.info(f"正在获取 sitemap: {self.sitemap_url}")
        resp = self.download(self.sitemap_url)
        if not resp:
            return []

        root = ET.fromstring(resp.content)
        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

        pages = []
        for url_elem in root.findall("ns:url", namespace):
            loc = url_elem.find("ns:loc", namespace)
            if loc is None:
                continue
            page_url = unquote(loc.text or "")
            lastmod_elem = url_elem.find("ns:lastmod", namespace)
            lastmod = lastmod_elem.text if lastmod_elem is not None else None
            pages.append({"url": page_url, "lastmod": lastmod})

        return pages

    def process_page(self, page: dict, order: int) -> bool:
        """Download and process a single GitBook page."""
        page_url = page["url"].rstrip("/")

        # Determine if this is the root page
        is_root = page_url == self.base_url

        if is_root:
            md_url = f"{self.base_url}/welcome.md"
            local_path = self.output_dir / "welcome.md"
            title = "Welcome"
        else:
            md_url = f"{page_url}.md"
            rel_path = page_url.replace(self.base_url, "").lstrip("/")
            local_path = self.output_dir / f"{rel_path}.md"
            # Generate title from slug
            slug = rel_path.split("/")[-1]
            title = slug.replace("-", " ").title()

        resp = self.download(md_url)
        if not resp:
            return False

        try:
            content = resp.content.decode("utf-8")
            final_content = process_markdown(content, str(local_path), title, order)
            self.save_file(local_path, final_content)
            return True
        except Exception as e:
            logger.error(f"    [错误] {local_path.name}: {e}")
            return False