"""
Retype crawler implementation.
"""
import json
import re
from pathlib import Path
from urllib.parse import urljoin
import logging

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

from .base_crawler import BaseCrawler
from .markdown_utils import process_markdown


logger = logging.getLogger(__name__)


def retype_language_callback(el):
    """Extract code language from Retype's class conventions."""
    code_elem = el.find("code")
    if code_elem and code_elem.get("class"):
        for c in code_elem.get("class"):
            if c.startswith("language-"):
                return c.replace("language-", "")
    if el.get("class"):
        for c in el.get("class"):
            if c.startswith("language-"):
                return c.replace("language-", "")
    return None


class RetypeConverter(MarkdownConverter):
    """Custom Markdown converter for Retype HTML."""

    def __init__(self, crawler: "RetypeCrawler", page_url: str, current_file_path: str, **options):
        super().__init__(**options)
        self.crawler = crawler
        self.page_url = page_url
        self.current_file_path = current_file_path

    def convert_a(self, el, text, parent_tags):
        href = el.get("href", "")
        href = self.crawler.resolve_link(href, self.page_url, self.current_file_path)
        return f"[{text.strip()}]({href})"

    def convert_svg(self, el, text, parent_tags):
        return ""  # Suppress inline SVGs

    def convert_i(self, el, text, parent_tags):
        return ""  # Suppress icon fonts

    def convert_div(self, el, text, parent_tags):
        classes = el.get("class", []) or []

        if "doc-callout" in classes:
            alert_type = "NOTE"
            icon_div = el.find("div", recursive=False)
            if icon_div:
                svg = icon_div.find("svg")
                if svg:
                    svg_classes = svg.get("class", [])
                    type_map = {
                        "warning": "WARNING",
                        "danger": "CAUTION",
                        "success": "TIP",
                        "primary": "NOTE",
                    }
                    for c in svg_classes:
                        if c.startswith("text-callout-"):
                            t = c.replace("text-callout-", "")
                            alert_type = type_map.get(t, "NOTE")
                            break

            content_divs = el.find_all("div", recursive=False)
            if content_divs:
                content_div = content_divs[-1]
                inner_md = self.convert_soup(content_div)
                lines = inner_md.strip().split("\n")
                quoted_lines = [f"> {line}" for line in lines]
                return f"\n> [!{alert_type}]\n" + "\n".join(quoted_lines) + "\n\n"

        return text

    def convert_span(self, el, text, parent_tags):
        classes = el.get("class", []) or []
        if any("badge-" in c for c in classes):
            return f"`{el.get_text().strip()}`"
        return text

    def convert_img(self, el, text, parent_tags):
        alt = el.get("alt", "")
        src = el.get("src", "")
        return f"![{alt}]({src})"


class RetypeCrawler(BaseCrawler):
    """Crawler for Retype-based documentation sites."""

    def __init__(self, name: str, config: dict, content_root: Path):
        super().__init__(name, config, content_root)
        self.config_url = config["config_url"]

    def fetch_pages(self) -> list[dict]:
        """Fetch pages from Retype's config.js."""
        logger.info(f"正在获取站点配置: {self.config_url}")
        resp = self.download(self.config_url)
        if not resp:
            return []

        content = resp.text
        match = re.search(r"var __DOCS_CONFIG__ = ({.*})", content)
        if not match:
            logger.error("未找到配置对象")
            return []

        config_json = match.group(1)
        # Fix trailing commas
        config_json = re.sub(r",\s*}", "}", config_json)
        config_json = re.sub(r",\s*]", "]", config_json)

        try:
            config = json.loads(config_json)
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析错误: {e}")
            return []

        if "sidebar" not in config:
            logger.error("配置中缺少 sidebar")
            return []

        return self._parse_sidebar(config["sidebar"])

    def _parse_sidebar(self, sidebar: list, parent_path: str = "") -> list[dict]:
        """Recursively parse Retype sidebar structure."""
        pages = []
        for item in sidebar:
            n = item.get("n", "")
            if n.startswith("/"):
                path = n.lstrip("/")
            else:
                path = f"{parent_path}/{n}".strip("/") if parent_path else n

            has_children = "i" in item
            if has_children:
                pages.extend(self._parse_sidebar(item["i"], path))

            # Skip link-only items
            if not n and "l" in item:
                continue

            if path == "":
                url = self.config["base_url"]
                file_path = "welcome.md"
            else:
                url = f"{self.base_url}/{path}/"
                file_path = f"{path}.md"

            pages.append({
                "url": url,
                "rel_path": file_path,
                "has_children": has_children,
            })

        return pages

    def process_page(self, page: dict, order: int) -> bool:
        """Download and convert a Retype page to Markdown."""
        url = page["url"]
        rel_path = page["rel_path"]
        has_children = page.get("has_children", False)

        resp = self.download(url)
        if not resp:
            # Silently skip parent-only pages that return 403/404
            if has_children:
                return True
            return False

        try:
            soup = BeautifulSoup(resp.content, "html.parser")
            content_div = soup.find("div", id="retype-content")

            if not content_div:
                logger.warning(f"    [警告] {rel_path}: 未找到内容区域")
                return False

            # Clean up unwanted elements
            for tag in content_div.find_all([
                "doc-anchor-trigger",
                "doc-sidebar-right",
                "doc-toolbar-member-filter-no-results",
            ]):
                tag.decompose()
            toggle = content_div.find(id="retype-sidebar-right-toggle")
            if toggle:
                toggle.decompose()

            converter = RetypeConverter(
                crawler=self,
                page_url=url,
                current_file_path=rel_path,
                heading_style="ATX",
                code_language_callback=retype_language_callback,
            )
            md_content = converter.convert_soup(content_div)

            # Extract title
            h1 = content_div.find("h1")
            if h1:
                title = h1.get_text().strip()
            else:
                base = Path(rel_path).stem
                title = base.replace("-", " ").title()

            local_path = self.output_dir / rel_path
            final_content = process_markdown(md_content, str(local_path), title, order)
            self.save_file(local_path, final_content)
            return True

        except Exception as e:
            logger.error(f"    [错误] {rel_path}: {e}")
            return False

    def resolve_link(self, href: str, page_url: str, current_file_path: str) -> str:
        """Convert internal links to relative Markdown links."""
        if not href or href.startswith("#"):
            return href

        full_url = urljoin(page_url, href)
        if not full_url.startswith(self.base_url):
            return href

        rel_url = full_url[len(self.base_url):]
        anchor = ""
        if "#" in rel_url:
            rel_url, anchor = rel_url.split("#", 1)
            anchor = "#" + anchor

        if rel_url in ("", "/"):
            target_file_path = "welcome"
        else:
            target_file_path = rel_url.strip("/")

        start_dir = Path(current_file_path).parent

        from os.path import relpath
        rel_link = relpath(target_file_path, start_dir).replace("\\", "/")
        return rel_link + anchor