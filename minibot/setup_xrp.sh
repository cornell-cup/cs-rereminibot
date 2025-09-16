#!/bin/bash

# Exit on any error
set -e

pip install mpremote

python -m mpremote mip install github:sparkfun/qwiic_rfid_py

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
base_url="https://raw.githubusercontent.com/cornell-cup/cs-rereminibot/houston-2025/minibot"

xrp_cp "$base_url/minibot.py" minibot.py
xrp_cp "$base_url/micropython_argparse.py" micropython_argparse.py
xrp_cp "$base_url/bs_repr.py" bs_repr.py

# Upload files from PestoLink repo
xrp_cp "https://raw.githubusercontent.com/AlfredoSystems/PestoLink-MicroPython/main/pestolink.py" lib/pestolink.py
xrp_cp "https://raw.githubusercontent.com/AlfredoSystems/PestoLink-MicroPython/main/examples/pestolink_example.py" pestolink_example.py

echo "Upload complete!"