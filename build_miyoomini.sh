#!/bin/sh
# Build for the Miyoo Mini (Plus) / OnionOS.
# Run inside the union-miyoomini-toolchain container, with this repository and
# the steward-fu/sdl2 build (in a folder named sdl2-miyoo) side by side in the
# workspace. Other locations: WS=... SDL2_DIR=... CMAKE=... ./build_miyoomini.sh
# Result: build-miyoo/package/Roms/... (copy over the SD card's Roms folder;
# make_release.py adds the SDL2 libraries and makes the release zip).
set -e
cd "$(dirname "$0")"
WS=${WS:-/root/workspace}
CMAKE=${CMAKE:-$WS/cmake-3.22.1-linux-x86_64/bin/cmake}
[ -x "$CMAKE" ] || CMAKE=cmake
SDL2_DIR=${SDL2_DIR:-$WS/sdl2-miyoo/sdl2}
SDL2_LIB=$SDL2_DIR/build/.libs/libSDL2.so

for f in "$SDL2_DIR/include/SDL.h" "$SDL2_LIB"; do
    if [ ! -e "$f" ]; then
        echo "ERRO: arquivo nao encontrado: '$f'"
        exit 1
    fi
done
if [ ! -e resources/ski32_1.bmp ]; then
    echo "ERRO: faltam os graficos do jogo em resources/ (veja o README)"
    exit 1
fi

OUT=build-miyoo
rm -rf $OUT
mkdir -p $OUT/inc/SDL2
cp $SDL2_DIR/include/*.h $OUT/inc/SDL2/

# game bitmaps inside the program (embedded_resources.h); the two signs of
# the title screen come from miyoo/ (they name the Miyoo buttons)
mkdir -p $OUT/src/resources
cp resources/ski32_*.bmp $OUT/src/resources/
cp miyoo/ski32_55.bmp miyoo/ski32_56.bmp $OUT/src/resources/
(cd $OUT && $CMAKE -DSOURCE_DIR="$(pwd)/src" -DRESOURCES_GLOB='resources/ski32_*.bmp' -P ../cmake/EmbedResources.cmake > /dev/null 2>&1) || { echo "ERRO ao embutir os graficos"; exit 1; }

arm-linux-gnueabihf-gcc -Os -g -marm -mtune=cortex-a7 -mfpu=neon-vfpv4 -mfloat-abi=hard -march=armv7ve+simd \
    -fsigned-char -fno-strict-aliasing -Wall \
    -I$OUT/inc -I$OUT/inc/SDL2 -I$OUT -Isrc \
    src/skifree_decomp.c -o $OUT/skifree.sym \
    "$SDL2_LIB" -Wl,--allow-shlib-undefined -lm
arm-linux-gnueabihf-strip -o $OUT/skifree $OUT/skifree.sym

G=$OUT/package/Roms/PORTS/Games/SkiFree
mkdir -p $G $OUT/package/Roms/PORTS/Shortcuts $OUT/package/Roms/PORTS/Imgs
cp $OUT/skifree miyoo/skifree-launcher.sh miyoo/README.txt $G/
cp miyoo/SkiFree.port $OUT/package/Roms/PORTS/Shortcuts/
cp miyoo/SkiFree.png $OUT/package/Roms/PORTS/Imgs/
chmod +x $G/skifree $G/skifree-launcher.sh
echo
echo "OK: $OUT/package"
md5sum $G/skifree
