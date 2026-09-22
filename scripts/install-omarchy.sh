#!/bin/bash
# Build Bible Baseball and add it to Super+Space on Omarchy.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LIB="$HOME/.local/lib/winbb"
BIN="$HOME/.local/bin"
ICON_DIR="$HOME/.local/share/icons"
APP_DIR="$HOME/.local/share/applications"

if ! command -v go >/dev/null 2>&1; then
	echo "Go is not on PATH. On Omarchy: omarchy install dev-env go" >&2
	exit 1
fi

mkdir -p "$LIB" "$BIN" "$ICON_DIR" "$APP_DIR"
(cd "$ROOT" && go build -o "$LIB/winbb" .)
install -m 755 "$ROOT/scripts/winbb" "$BIN/winbb"
cp "$ROOT/assets/icon.png" "$ICON_DIR/bible-baseball.png"

cat > "$APP_DIR/bible-baseball.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Bible Baseball
Comment=Bible trivia baseball (1994 WinBB remake)
Exec=$HOME/.local/bin/winbb
Icon=$HOME/.local/share/icons/bible-baseball.png
Terminal=false
Categories=Game;Education;
StartupNotify=true
StartupWMClass=gamescope
EOF

echo "Installed. Open Super+Space and search Bible Baseball, or run: winbb"
echo
echo "Optional Super-menu row — add this to ~/.config/omarchy/extensions/omarchy-menu.jsonc:"
echo
cat <<'EOF'
  "winbb": {
    "icon": "󰐊",
    "label": "Bible Baseball",
    "description": "1994 Bible trivia baseball",
    "action": "uwsm-app -- winbb"
  }
EOF
