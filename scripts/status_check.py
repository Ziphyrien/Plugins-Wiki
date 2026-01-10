import os
import subprocess
import sys
import datetime
import json
import argparse

# Default paths suitable for the worktree structure
# Assuming script is run from main/scripts/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
# Default to ../content if not provided
CONTENT_ROOT = os.path.join(os.path.dirname(PROJECT_ROOT), "content")

# Starlight assets path for local dev sync
STARLIGHT_ASSETS = os.path.join(os.path.dirname(PROJECT_ROOT), "starlight", "src", "assets")

EN_DIR = os.path.join(CONTENT_ROOT, "en")
ZH_DIR = os.path.join(CONTENT_ROOT, "zh")

def get_git_timestamp(filepath, cwd):
    try:
        # returns timestamp of Last Committed Date
        # relative path from cwd
        rel_path = os.path.relpath(filepath, cwd)
        # Use ISO format for JS compatibility later, but here we need int, so %ct is good for comparison
        # For output we want ISO 8601
        
        # Determine last commit date for the file
        output = subprocess.check_output(['git', 'log', '-1', '--format=%ct', rel_path], cwd=cwd).decode().strip()
        if not output:
            return 0
        return int(output)
    except Exception as e:
        # If file is new and not committed
        return 0

def get_git_iso_date(filepath, cwd):
    try:
        rel_path = os.path.relpath(filepath, cwd)
        output = subprocess.check_output(['git', 'log', '-1', '--format=%cI', rel_path], cwd=cwd).decode().strip()
        if not output:
            return None
        return output
    except Exception:
        return None

def generate_metadata(output_path=None):
    if not os.path.exists(EN_DIR):
        print(f"Error: Content directory not found at {CONTENT_ROOT}")
        return

    print(f"Generating metadata from Git history in {CONTENT_ROOT}...")
    
    metadata = {"files": {}}
    
    # Walk EN files
    for root, dirs, files in os.walk(EN_DIR):
        for file in files:
            if not file.endswith('.md'):
                continue
                
            en_path = os.path.join(root, file)
            # key relative to 'docs/' conceptually, but here we construct based on file location
            # Structure matches: content/en/plugin/... -> docs/plugin/...
            
            # calculate relative path from content root
            # rel_from_content = en/plugin/file.md
            rel_from_en = os.path.relpath(en_path, EN_DIR)
            
            # Starlight Key: docs/plugin/file.md
            # PageTitle.astro logic suggests key is docs/<path_without_lang>.md
            # e.g. en/coinsengine/welcome.md -> rel "coinsengine/welcome" -> key "docs/coinsengine/welcome.md"
            
            key = f"docs/{rel_from_en.replace(os.sep, '/')}"
            
            # Get EN Timestamp
            crawled_at = get_git_iso_date(en_path, CONTENT_ROOT)
            
            # Check ZH
            zh_path = os.path.join(ZH_DIR, rel_from_en)
            translated_at = None
            translated_status = "missing"
            
            if os.path.exists(zh_path):
                translated_at = get_git_iso_date(zh_path, CONTENT_ROOT)
                
                # Check status
                en_ts = get_git_timestamp(en_path, CONTENT_ROOT)
                zh_ts = get_git_timestamp(zh_path, CONTENT_ROOT)
                
                if zh_ts >= en_ts:
                    translated_status = "completed"
                else:
                    translated_status = "outdated"
            
            metadata["files"][key] = {
                "crawled_at": crawled_at,
                "translated_at": translated_at,
                "translation_status": translated_status
            }

    # Output
    if not output_path:
        # Default to local Starlight assets if exists
        if os.path.exists(os.path.dirname(STARLIGHT_ASSETS)):
             output_path = os.path.join(STARLIGHT_ASSETS, "version_metadata.json")
        else:
             output_path = "version_metadata.json"

    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        print(f"Metadata saved to {output_path}")
    except Exception as e:
        print(f"Failed to save metadata to {output_path}: {e}")

def scan_files():
    # ... existing scan logic optimized ...
    if not os.path.exists(EN_DIR):
        print(f"Error: Content directory not found at {CONTENT_ROOT}")
        return

    print(f"Scanning content in {CONTENT_ROOT}...")
    report = []
    
    for root, dirs, files in os.walk(EN_DIR):
        for file in files:
            if not file.endswith('.md'):
                continue
                
            en_path = os.path.join(root, file)
            rel_path = os.path.relpath(en_path, EN_DIR)
            zh_path = os.path.join(ZH_DIR, rel_path)
            
            en_time = get_git_timestamp(en_path, CONTENT_ROOT)
            zh_time = 0
            status = "missing"
            
            if os.path.exists(zh_path):
                zh_time = get_git_timestamp(zh_path, CONTENT_ROOT)
                if zh_time >= en_time:
                    status = "completed"
                else:
                    status = "outdated"
            
            if status != "completed":
                report.append({
                    "file": rel_path,
                    "status": status,
                    "en_time": en_time,
                    "zh_time": zh_time
                })

    if not report:
        print("All translations are up to date!")
    else:
        print(f"Found {len(report)} issues:")
        print(f"{'Status':<12} | {'File'}")
        print("-" * 60)
        for item in report:
            print(f"{item['status']:<12} | {item['file']}")
            # Date display logic...

def main():
    parser = argparse.ArgumentParser(description="Git-based Version Management")
    parser.add_argument("action", choices=["scan", "gen-meta"], nargs="?", default="scan", help="Action to perform")
    parser.add_argument("--output", help="Output path for version_metadata.json")
    
    args = parser.parse_args()
    
    if args.action == "scan":
        scan_files()
    elif args.action == "gen-meta":
        generate_metadata(args.output)

if __name__ == "__main__":
    main()
