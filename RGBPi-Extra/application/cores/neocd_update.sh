#!/bin/bash

set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")"

mv -vn /opt/retroarch/cores/neocd_libretro.so /opt/retroarch/cores/neocd_libretro.so.bak

cp -v opt/retroarch/cores/neocd_libretro.so /opt/retroarch/cores/neocd_libretro.so

clear
echo
echo
echo "CORE UPDATED SUCCESSFULLY!"

sleep 3