#!/usr/bin/env python3
"""Makes the release zip of the Miyoo Mini port.

Usage (outside the container, after ./build_miyoomini.sh):
    python3 make_release.py VERSION LIBS

VERSION  e.g. 1.0.0
LIBS     where to take the SDL2 libraries from: a folder, or the release zip
         of another port of this series (they ship the same files):
         libSDL2-2.0.so.0, libEGL.so, libGLESv2.so, libjson-c.so.5

Writes SkiFree-Miyoo-vVERSION.zip in the current folder.
"""
import os
import sys
import zipfile

LIBS = ["libSDL2-2.0.so.0", "libEGL.so", "libGLESv2.so", "libjson-c.so.5"]
PACKAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build-miyoo", "package")
GAME_DIR = "Roms/PORTS/Games/SkiFree/"
EXECUTABLE = {GAME_DIR + "skifree", GAME_DIR + "skifree-launcher.sh", "Roms/PORTS/Shortcuts/SkiFree.port"}


def read_libs(source):
    libs = {}
    if os.path.isdir(source):
        for name in LIBS:
            path = os.path.join(source, name)
            if os.path.exists(path):
                libs[name] = open(path, "rb").read()
    else:
        with zipfile.ZipFile(source) as z:
            for info in z.infolist():
                name = info.filename.rsplit("/", 1)[-1]
                if name in LIBS and name not in libs:
                    libs[name] = z.read(info)
    missing = [n for n in LIBS if n not in libs]
    if missing:
        sys.exit("ERRO: nao achei em %s: %s" % (source, ", ".join(missing)))
    return libs


def add(z, arcname, data):
    info = zipfile.ZipInfo(arcname, date_time=(2026, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = (0o755 if arcname in EXECUTABLE or arcname.endswith("/") else 0o644) << 16
    if arcname.endswith("/"):
        info.external_attr |= 0x10
    z.writestr(info, data)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    version, source = sys.argv[1].lstrip("v"), sys.argv[2]
    if not os.path.exists(os.path.join(PACKAGE, GAME_DIR, "skifree")):
        sys.exit("ERRO: rode ./build_miyoomini.sh antes (falta build-miyoo/package)")
    libs = read_libs(source)

    out = "SkiFree-Miyoo-v%s.zip" % version
    with zipfile.ZipFile(out, "w") as z:
        dirs = set()
        entries = []
        for root, _, names in os.walk(PACKAGE):
            for name in names:
                path = os.path.join(root, name)
                entries.append((os.path.relpath(path, PACKAGE).replace(os.sep, "/"), open(path, "rb").read()))
        for name, data in libs.items():
            entries.append((GAME_DIR + name, data))
        for arcname, _ in entries:
            parts = arcname.split("/")[:-1]
            for i in range(1, len(parts) + 1):
                dirs.add("/".join(parts[:i]) + "/")
        for d in sorted(dirs):
            add(z, d, b"")
        for arcname, data in sorted(entries):
            add(z, arcname, data)
    print("OK: %s" % out)
    with zipfile.ZipFile(out) as z:
        for info in z.infolist():
            if not info.filename.endswith("/"):
                print("  %10d  %s" % (info.file_size, info.filename))


if __name__ == "__main__":
    main()
