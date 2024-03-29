#!/bin/bash

set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")"

mv -vn /opt/retroarch/cores/genesis_plus_gx_libretro.so /opt/retroarch/cores/genesis_plus_gx_libretro.so.bak

cp -v opt/retroarch/cores/genesis_plus_gx_libretro.so /opt/retroarch/cores/genesis_plus_gx_libretro.so

clear
echo
echo
echo "CORE UPDATED SUCCESSFULLY!"

sleep 3