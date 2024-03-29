#!/bin/bash

set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")"

mv -vn /opt/retroarch/cores/stella_libretro.so /opt/retroarch/cores/stella_libretro.so.bak

cp -v opt/retroarch/cores/stella_libretro.so /opt/retroarch/cores/stella_libretro.so

clear
echo
echo
echo "CORE UPDATED SUCCESSFULLY!"

sleep 3