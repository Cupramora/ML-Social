# === copilot_sync.py ===
# Author: Dane & Copilot
# Purpose: Extract code context and create a portable memory bundle for AI initialization.
# Usage: Run this script from your project root to generate a structured `.zip` of relevant files,
#         plus a contextual summary for easy reinjection into Copilot sessions.
# Future Expansion:
#   - Parse line-1 annotations as module mnemonics
#   - Include emotional/contextual tags
#   - Tie into local API or Codespace bootstrapping

import os
import json
import zipfile

# === CONFIGURATION ===
PROJECT_ROOT = './'  # Root of your project folder
INCLUDE_EXT = ['.py', '.json', '.md', '.sh']  # File types to include
SUMMARY_FILE = 'context_summary.json'
BUNDLE_FILE = 'copilot_bundle.zip'

# === FUNCTION: Crawl directory and summarize file metadata ===
def walk_and_index(path):
    summary = {}
    for root, _, files in os.walk(path):
        for fname in files:
            ext = os.path.splitext(fname)[1]
            if ext in INCLUDE_EXT:
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    first_line = content.splitlines()[0] if content else ''
                    summary[fpath] = {
                        "lines": len(content.splitlines()),
                        "preview": content[:300],
                        "mnemonic": first_line.strip() if first_line.startswith('#') else ""
                    }
                except Exception as e:
                    summary[fpath] = {"error": str(e)}
    return summary

# === FUNCTION: Write JSON summary to disk ===
def write_summary(summary, out_path):
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

# === FUNCTION: Create zip archive of files ===
def zip_payload(files, output):
    with zipfile.ZipFile(output, 'w') as z:
        for f in files:
            try:
                z.write(f)
            except Exception as e:
                print(f"Could not zip file: {f} — {e}")

# === MAIN PROCESS ===
if __name__ == '__main__':
    print(" Scanning project for Copilot sync...")
    index = walk_and_index(PROJECT_ROOT)
    write_summary(index, SUMMARY_FILE)
    files = list(index.keys()) + [SUMMARY_FILE]
    zip_payload(files, BUNDLE_FILE)
    print(f" Copilot bundle created: {BUNDLE_FILE}")
