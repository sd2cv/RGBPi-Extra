#!/bin/bash
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
script_url="https://raw.githubusercontent.com/sd2cv/RGBPi-Extra/master/RGBPi-Extra/application/installer.py"
wget -q -O "$script_dir/installer.py" "$script_url"
python3 "$script_dir/installer.py"
rm "$0"
