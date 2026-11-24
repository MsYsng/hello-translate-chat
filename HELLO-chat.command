#!/bin/bash
# Double-click to start HELLO chat on a Mac. The admin screen opens in your browser.
cd "$(dirname "$0")" || exit 1
python3 hello_chat.py --open
echo
read -n 1 -s -r -p "Press any key to close this window."
