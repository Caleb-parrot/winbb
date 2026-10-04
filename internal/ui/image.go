package ui

import (
	"image"
	_ "image/png"
	"io"

	"github.com/caleb-parrot/winbb/assets"
	"github.com/hajimehoshi/ebiten/v2"
)

func SetWindowIcon() {
	f, err := assets.FS.Open("icon.png")
	if err != nil {
		return
	}
	defer f.Close()
	img, _, err := image.Decode(f)
	if err != nil {
		return
	}
	ebiten.SetWindowIcon([]image.Image{img})
}

func decodeImage(r io.Reader) (*ebiten.Image, error) {
	img, _, err := image.Decode(r)
	if err != nil {
		return nil, err
	}
	return ebiten.NewImageFromImage(img), nil
}
