#!/bin/bash

set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")"

# Check if a backup exists
if [[ -f /opt/rgbpi/ui/config.ini.bak ]]; then
    mv -vf /opt/rgbpi/ui/config.ini.bak /opt/rgbpi/ui/config.ini
    echo "Backup restored successfully."
else
    echo "No backup found."
fi

clear
echo
echo
echo "  CONFIG RESTORED SUCCESSFULLY!"

reboot
