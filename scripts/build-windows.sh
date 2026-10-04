#!/bin/sh
# Cross-compile a double-clickable Windows exe (no console window).
set -eu

cd "$(dirname "$0")/.."

PATH="$(go env GOBIN):$(go env GOPATH)/bin:$PATH"
export PATH
if ! command -v go-winres >/dev/null 2>&1; then
	go install github.com/tc-hib/go-winres@latest
fi

# Explorer icon + DPI-aware GUI manifest. Named so Linux builds ignore it.
rm -f rsrc_windows_amd64.syso
go-winres simply \
	--icon assets/icon.png \
	--manifest gui \
	--arch amd64 \
	--product-name "Bible Baseball" \
	--product-version 0.1.0 \
	--file-version 0.1.0 \
	--file-description "Bible trivia baseball" \
	--original-filename BibleBaseball.exe

mkdir -p dist
rm -f dist/BibleBaseball.exe dist/BibleBaseball-windows.zip dist/"How to play.txt"

CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build \
	-ldflags="-s -w -H windowsgui" \
	-o dist/BibleBaseball.exe .

printf '%s\n' "Double-click BibleBaseball.exe to play." > dist/"How to play.txt"
(
	cd dist
	zip -9 -q BibleBaseball-windows.zip BibleBaseball.exe "How to play.txt"
)

echo "Built dist/BibleBaseball.exe"
ls -lh dist/BibleBaseball.exe dist/BibleBaseball-windows.zip
