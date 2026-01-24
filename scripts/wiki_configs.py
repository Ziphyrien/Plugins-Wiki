"""
Wiki configuration loader.
"""
import json
from pathlib import Path
from typing import Any


_SCRIPT_DIR = Path(__file__).parent
_CONFIG_FILE = _SCRIPT_DIR / "wiki_configs.json"


def load_configs() -> dict[str, Any]:
    """Load wiki configurations from JSON file."""
    with _CONFIG_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


WIKI_CONFIGS = load_configs()
