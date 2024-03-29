#!/bin/bash

set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")"

mv -vn /opt/retroarch/cores/px64k_libretro.so /opt/retroarch/cores/px64k_ibretro.so.bak

cp -v opt/retroarch/cores/px64k_libretro.so /opt/retroarch/cores/px64k_ibretro.so

clear
echo
echo
echo "CORE UPDATED SUCCESSFULLY!"

sleep 3