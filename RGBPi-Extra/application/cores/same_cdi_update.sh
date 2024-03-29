#!/bin/bash

set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")"

mv -vn /opt/retroarch/cores/same_cdi_libretro.so /opt/retroarch/cores/same_cdi_ibretro.so.bak

cp -v opt/retroarch/cores/same_cdi_libretro.so /opt/retroarch/cores/same_cdi_ibretro.so

clear
echo
echo
echo "CORE UPDATED SUCCESSFULLY!"

sleep 3