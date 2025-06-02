#!/bin/bash

# Exit on any error
set -e

pip install mpremote

# Helper function to download + push to device
xrp_cp() {
  local url="$1"
  local dest="$2"
  tmpfile=$(mktemp)
  curl -s "$url" -o "$tmpfile"
  python3 -m mpremote fs cp "$tmpfile" :"$dest"
  rm "$tmpfile"
}

# Upload files from cs-rereminibot repo (houston-2025 branch)
current_branch=$(git rev-parse --abbrev-ref HEAD)
base_url="https://raw.githubusercontent.com/cornell-cup/cs-rereminibot/${current_branch}/minibot/xrp_display"

xrp_cp "$base_url/st7789_fb_plus.py" lib/st7789_fb_plus.py
xrp_cp "$base_url/display_example.py" display_example.py
xrp_cp "$base_url/display_chuckle.py" display_chuckle.py

echo "Upload complete!"