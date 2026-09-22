package ui

import (
	"image/color"
	"strings"

	"github.com/hajimehoshi/ebiten/v2"
	text "github.com/hajimehoshi/ebiten/v2/text/v2"
)

var (
	colFace     = color.RGBA{0xC0, 0xC0, 0xC0, 0xFF}
	colLight    = color.RGBA{0xFF, 0xFF, 0xFF, 0xFF}
	colShadow   = color.RGBA{0x80, 0x80, 0x80, 0xFF}
	colDark     = color.RGBA{0x00, 0x00, 0x00, 0xFF}
	colNavy     = color.RGBA{0x00, 0x00, 0x80, 0xFF}
	colNavyHi   = color.RGBA{0x00, 0x00, 0xA8, 0xFF}
	colTeal     = color.RGBA{0x00, 0x80, 0x80, 0xFF}
	colText     = color.RGBA{0x00, 0x00, 0x00, 0xFF}
	colWhite    = color.RGBA{0xFF, 0xFF, 0xFF, 0xFF}
	colYellow   = color.RGBA{0xFF, 0xFF, 0x00, 0xFF}
	colRed      = color.RGBA{0xC0, 0x00, 0x00, 0xFF}
	colBlue     = color.RGBA{0x00, 0x00, 0xC0, 0xFF}
	colSkin     = color.RGBA{0xF0, 0xC8, 0x90, 0xFF}
	colGrassMsg = color.RGBA{0x00, 0x40, 0x00, 0xC0}
)

var pixel *ebiten.Image

func init() {
	pixel = ebiten.NewImage(1, 1)
	pixel.Fill(color.White)
}

func fill(dst *ebiten.Image, x, y, w, h int, c color.Color) {
	if w <= 0 || h <= 0 {
		return
	}
	op := &ebiten.DrawImageOptions{}
	op.GeoM.Scale(float64(w), float64(h))
	op.GeoM.Translate(float64(x), float64(y))
	op.ColorScale.ScaleWithColor(c)
	dst.DrawImage(pixel, op)
}

func hline(dst *ebiten.Image, x, y, w int, c color.Color) { fill(dst, x, y, w, 1, c) }
func vline(dst *ebiten.Image, x, y, h int, c color.Color) { fill(dst, x, y, 1, h, c) }

func raised(dst *ebiten.Image, x, y, w, h int) {
	fill(dst, x, y, w, h, colFace)
	hline(dst, x, y, w, colLight)
	vline(dst, x, y, h, colLight)
	hline(dst, x, y+h-1, w, colDark)
	vline(dst, x+w-1, y, h, colDark)
	hline(dst, x+1, y+h-2, w-2, colShadow)
	vline(dst, x+w-2, y+1, h-2, colShadow)
}

func sunken(dst *ebiten.Image, x, y, w, h int) {
	fill(dst, x, y, w, h, colFace)
	hline(dst, x, y, w, colShadow)
	vline(dst, x, y, h, colShadow)
	hline(dst, x, y+h-1, w, colLight)
	vline(dst, x+w-1, y, h, colLight)
	hline(dst, x+1, y+1, w-2, colDark)
	vline(dst, x+1, y+1, h-2, colDark)
}

func windowFrame(dst *ebiten.Image, x, y, w, h int, title string, face *text.GoXFace) {
	raised(dst, x, y, w, h)
	fill(dst, x+3, y+3, w-6, 18, colNavy)
	drawText(dst, title, face, x+8, y+5, colWhite)
}

func drawText(dst *ebiten.Image, s string, face *text.GoXFace, x, y int, c color.Color) {
	if s == "" || face == nil {
		return
	}
	op := &text.DrawOptions{}
	op.GeoM.Translate(float64(x), float64(y))
	op.ColorScale.ScaleWithColor(c)
	text.Draw(dst, s, face, op)
}

func textWidth(s string, face *text.GoXFace) int {
	if face == nil {
		return len(s) * 7
	}
	w, _ := text.Measure(s, face, 0)
	return int(w)
}

func wrapText(s string, face *text.GoXFace, maxW int) []string {
	words := strings.Fields(s)
	if len(words) == 0 {
		return nil
	}
	var lines []string
	cur := words[0]
	for _, w := range words[1:] {
		trial := cur + " " + w
		if textWidth(trial, face) <= maxW {
			cur = trial
			continue
		}
		lines = append(lines, cur)
		cur = w
	}
	return append(lines, cur)
}

type rect struct{ X, Y, W, H int }

func (r rect) contains(x, y int) bool {
	return x >= r.X && y >= r.Y && x < r.X+r.W && y < r.Y+r.H
}

func button(dst *ebiten.Image, r rect, label string, face *text.GoXFace, pressed, hover bool) {
	if pressed {
		sunken(dst, r.X, r.Y, r.W, r.H)
	} else {
		raised(dst, r.X, r.Y, r.W, r.H)
		if hover {
			fill(dst, r.X+2, r.Y+2, r.W-4, r.H-4, color.RGBA{0xD8, 0xD8, 0xE8, 0xFF})
		}
	}
	tw := textWidth(label, face)
	tx := r.X + (r.W-tw)/2
	ty := r.Y + (r.H-14)/2
	if pressed {
		tx++
		ty++
	}
	drawText(dst, label, face, tx, ty, colText)
}

func checkbox(dst *ebiten.Image, x, y int, label string, face *text.GoXFace, on bool) rect {
	sunken(dst, x, y, 13, 13)
	fill(dst, x+2, y+2, 9, 9, colWhite)
	if on {
		fill(dst, x+3, y+3, 7, 7, colNavy)
	}
	drawText(dst, label, face, x+18, y-1, colText)
	w := 18 + textWidth(label, face) + 8
	return rect{x, y, w, 16}
}

func textField(dst *ebiten.Image, r rect, value string, face *text.GoXFace, focus bool) {
	sunken(dst, r.X, r.Y, r.W, r.H)
	fill(dst, r.X+2, r.Y+2, r.W-4, r.H-4, colWhite)
	s := value
	if focus {
		s += "_"
	}
	drawText(dst, s, face, r.X+6, r.Y+4, colText)
}
