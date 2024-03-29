#!/bin/bash

set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")"

mv -vn /opt/retroarch/cores/bluemsx_libretro.so /opt/retroarch/cores/bluemsx_libretro.so.bak

cp -v opt/retroarch/cores/bluemsx_libretro.so /opt/retroarch/cores/bluemsx_libretro.so

clear
echo
echo
echo "CORE UPDATED SUCCESSFULLY!"

sleep 3
