#!/bin/sh
# Build and install winbb on GhostBSD / FreeBSD.
# Run from the repository root: sh freebsd-port/install.sh

set -eu

cd "$(dirname "$0")/.."

if ! command -v go >/dev/null 2>&1; then
	echo "Go is not installed. On GhostBSD run:" >&2
	echo "  sudo pkg install go git" >&2
	echo "  sudo pkg install libX11 libglvnd mesa-libs mesa-dri libXcursor libXi libXinerama libXrandr libXrender libXext alsa-lib" >&2
	exit 1
fi

# Ebitengine v2.10 desktop builds are pure Go. Skip cgo so GhostBSD
# does not need C headers (stddef.h) from GhostBSD*-dev.
echo "Building winbb..."
CGO_ENABLED=0 go build -o winbb .

DESTDIR="${DESTDIR:-}"
PREFIX="${PREFIX:-/usr/local}"
echo "Installing to ${PREFIX} (needs root)..."
install -d "${DESTDIR}${PREFIX}/bin"
install -d "${DESTDIR}${PREFIX}/share/applications"
install -d "${DESTDIR}${PREFIX}/share/icons/hicolor/128x128/apps"
install -d "${DESTDIR}${PREFIX}/share/pixmaps"
install -m 755 winbb "${DESTDIR}${PREFIX}/bin/winbb"
install -m 644 winbb.desktop "${DESTDIR}${PREFIX}/share/applications/winbb.desktop"
install -m 644 assets/icon.png "${DESTDIR}${PREFIX}/share/icons/hicolor/128x128/apps/bible-baseball.png"
install -m 644 assets/icon.png "${DESTDIR}${PREFIX}/share/pixmaps/bible-baseball.png"

echo "Installed ${PREFIX}/bin/winbb"
echo "Open it from the menu as Bible Baseball, or run: winbb"
