#!/bin/bash

set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")"

# Check if a backup already exists
if [[ -f /opt/rgbpi/ui/config.ini.bak ]]; then
    echo "A backup file already exists. Aborting."
    exit 1
fi

# Backup the original config.ini if it exists
if [[ -f /opt/rgbpi/ui/config.ini ]]; then
    mv -v /opt/rgbpi/ui/config.ini /opt/rgbpi/ui/config.ini.bak
fi

# Copy the new config.ini
cp -v files/config.ini /opt/rgbpi/ui/config.ini

clear
echo
echo
echo "  CONFIG LOADED SUCCESSFULLY!"

reboot
