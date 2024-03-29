#!/bin/bash

set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")"

mv -vn /opt/retroarch/cores/fbneo_libretro.so /opt/retroarch/cores/fbneo_libretro.so.bak

cp -v opt/retroarch/cores/fbneo_libretro.so /opt/retroarch/cores/fbneo_libretro.so

clear
echo
echo
echo "CORE UPDATED SUCCESSFULLY!"

sleep 3