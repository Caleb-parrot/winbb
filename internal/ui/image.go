package ui

import (
	"image"
	_ "image/png"
	"io"

	"github.com/hajimehoshi/ebiten/v2"
)

func decodeImage(r io.Reader) (*ebiten.Image, error) {
	img, _, err := image.Decode(r)
	if err != nil {
		return nil, err
	}
	return ebiten.NewImageFromImage(img), nil
}
