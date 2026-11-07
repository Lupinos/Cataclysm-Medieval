#!/bin/bash
set -euo pipefail
# Use the existing isolated checkout; do not create a Git worktree.
setup_root=/workspace/cataclysm-env
mkdir -p "$setup_root"/{debs,sysroot,apt/lists/partial,apt/cache/archives/partial}
if [ ! -x "$setup_root/venv/bin/python" ]; then python3 -m venv "$setup_root/venv"; fi
"$setup_root/venv/bin/pip" install 'cmake==3.31.10' 'ninja==1.13.0'
cat > "$setup_root/apt/apt.conf" <<'APTCONF'
Dir::Etc::parts "-";
Dir::Etc::main "-";
Dir::Etc::sourcelist "/workspace/cataclysm-env/apt/sources.list";
Dir::Etc::sourceparts "-";
Dir::State::lists "/workspace/cataclysm-env/apt/lists";
Dir::Cache "/workspace/cataclysm-env/apt/cache";
APT::Get::List-Cleanup "false";
APTCONF
cat > "$setup_root/apt/sources.list" <<'SOURCES'
deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://deb.debian.org/debian trixie main
SOURCES
export APT_CONFIG="$setup_root/apt/apt.conf"
/usr/bin/apt-get update
(cd "$setup_root/debs" && /usr/bin/apt-get download libncurses-dev libtinfo6 libncurses6 libncursesw6 libbz2-dev)
for debfile in "$setup_root"/debs/*.deb; do dpkg-deb -x "$debfile" "$setup_root/sysroot"; done
export PATH="$setup_root/venv/bin:$PATH"
cmake -S /workspace/Cataclysm-Medieval -B "$setup_root/build" -G Ninja \
 -DCMAKE_BUILD_TYPE=Release '-DCMAKE_CXX_FLAGS_RELEASE=-O0 -DNDEBUG' \
 -DCMAKE_PREFIX_PATH="$setup_root/sysroot/usr" \
 -DCURSES_INCLUDE_PATH="$setup_root/sysroot/usr/include" \
 -DCURSES_NCURSES_LIBRARY="$setup_root/sysroot/usr/lib/x86_64-linux-gnu/libncursesw.so" \
 -DCURSES_EXTRA_LIBRARY="$setup_root/sysroot/usr/lib/x86_64-linux-gnu/libtinfo.so" \
 -DTILES=OFF -DCURSES=ON -DSOUND=OFF -DLOCALIZE=OFF -DTESTS=ON \
 -DUSE_PREFIX_DATA_DIR=OFF -DJSON_FORMAT=OFF
cmake --build "$setup_root/build" --target cataclysm cata_test --parallel 5
