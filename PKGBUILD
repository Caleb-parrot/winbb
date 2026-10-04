# Maintainer: Caleb-parrot <288791519+Caleb-parrot@users.noreply.github.com>
pkgname=winbb
pkgver=0.1.0
pkgrel=1
pkgdesc='Bible trivia baseball (1994 WinBB remake)'
arch=('x86_64')
url='https://github.com/Caleb-parrot/winbb'
license=('PolyForm-Noncommercial-1.0.0')
depends=('glibc' 'libx11' 'libglvnd' 'mesa' 'libxcursor' 'libxi' 'libxinerama' 'libxrandr' 'libxrender' 'libxext')
optdepends=(
  'gamescope: integer-scale the 990x766 window'
  'alsa-lib: ALSA audio fallback'
)
makedepends=('go' 'git')
options=('!debug')
source=("git+$url.git")
sha256sums=('SKIP')

prepare() {
  cd winbb
  export GOPATH="${srcdir}"
  go mod download -modcacherw
}

build() {
  cd winbb
  export CGO_CPPFLAGS="${CPPFLAGS}"
  export CGO_CFLAGS="${CFLAGS}"
  export CGO_CXXFLAGS="${CXXFLAGS}"
  export CGO_LDFLAGS="${LDFLAGS}"
  export GOPATH="${srcdir}"
  export GOFLAGS="-buildmode=pie -trimpath -ldflags=-linkmode=external -mod=readonly -modcacherw"
  go build -o winbb .
}

check() {
  cd winbb
  export GOPATH="${srcdir}"
  go test ./...
}

package() {
  cd winbb
  install -Dm755 winbb "$pkgdir/usr/lib/winbb/winbb"
  install -Dm755 scripts/winbb "$pkgdir/usr/bin/winbb"
  install -Dm644 winbb.omarchy.desktop "$pkgdir/usr/share/applications/winbb.desktop"
  install -Dm644 assets/icon.png "$pkgdir/usr/share/icons/hicolor/128x128/apps/bible-baseball.png"
  install -Dm644 assets/icon.png "$pkgdir/usr/share/pixmaps/bible-baseball.png"
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
