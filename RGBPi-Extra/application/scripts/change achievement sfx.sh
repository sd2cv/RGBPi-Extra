#!/bin/bash

set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")"

# Backup the original file if it exists
if [[ -f /opt/rgbpi/ui/raassets/sounds/unlock.ogg.bak ]]; then
    echo "A backup file already exists. Aborting."
    exit 1
fi

# Move the original file to a backup
mv -vn /opt/rgbpi/ui/raassets/sounds/unlock.ogg /opt/rgbpi/ui/raassets/sounds/unlock.ogg.bak

# Copy the new file
cp -v files/unlock.ogg /opt/rgbpi/ui/raassets/sounds/unlock.ogg

clear
echo
echo
echo "  ACHIEVEMENT SFX CHANGED SUCCESSFULLY!"
