import json
import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Read from wiki_configs.json in the same directory
METADATA_FILE = os.path.join(SCRIPT_DIR, "wiki_configs.json")

def load_configs():
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

WIKI_CONFIGS = load_configs()
