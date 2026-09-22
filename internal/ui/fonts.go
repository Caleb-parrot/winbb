package ui

import (
	"os"

	"golang.org/x/image/font"
	"golang.org/x/image/font/basicfont"
	"golang.org/x/image/font/opentype"

	text "github.com/hajimehoshi/ebiten/v2/text/v2"
)

func loadFaces() (ui, small, title, board, qface *text.GoXFace) {
	data := readFont(
		"/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
		"/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
		"/usr/share/fonts/TTF/LiberationSans-Regular.ttf",
	)
	bold := readFont(
		"/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
		"/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
		"/usr/share/fonts/TTF/LiberationSans-Bold.ttf",
	)
	serif := readFont(
		"/usr/share/fonts/liberation/LiberationSerif-Bold.ttf",
		"/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
		"/usr/share/fonts/TTF/LiberationSerif-Bold.ttf",
	)
	if len(bold) == 0 {
		bold = data
	}
	if len(serif) == 0 {
		serif = bold
	}
	ui = mustFace(data, 13)
	small = mustFace(data, 11)
	title = mustFace(bold, 13)
	board = mustFace(serif, 12)
	qface = mustFace(data, 26)
	return
}

func readFont(paths ...string) []byte {
	for _, p := range paths {
		b, err := os.ReadFile(p)
		if err == nil && len(b) > 0 {
			return b
		}
	}
	return nil
}

func mustFace(ttf []byte, size float64) *text.GoXFace {
	if len(ttf) == 0 {
		return text.NewGoXFace(basicfont.Face7x13)
	}
	f, err := opentype.Parse(ttf)
	if err != nil {
		return text.NewGoXFace(basicfont.Face7x13)
	}
	face, err := opentype.NewFace(f, &opentype.FaceOptions{
		Size:    size,
		DPI:     72,
		Hinting: font.HintingFull,
	})
	if err != nil {
		return text.NewGoXFace(basicfont.Face7x13)
	}
	return text.NewGoXFace(face)
}
