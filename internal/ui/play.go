package ui

import (
	"fmt"
	"image/color"
	"math"

	"github.com/caleb-parrot/winbb/internal/quiz"
	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/inpututil"
)

type point struct{ x, y int }

func basePoints() []point {
	// Measured off LARGEFNT.BMP; y is in field pixels (add menuH when drawing).
	return []point{
		{348, 458}, // home
		{483, 389}, // first
		{347, 349}, // second
		{213, 389}, // third
		{348, 458}, // home
	}
}

func (a *App) updatePlay() error {
	if a.m == nil {
		a.scr = screenPregame
		return nil
	}
	if a.menuOpen != "" {
		return nil
	}
	if a.m.Over {
		a.alert = a.m.Result
		a.scr = screenGameOver
		return nil
	}
	if len(a.runners) > 0 {
		return nil
	}
	ctrl := ebiten.IsKeyPressed(ebiten.KeyControlLeft) || ebiten.IsKeyPressed(ebiten.KeyControlRight)
	if ctrl && inpututil.IsKeyJustPressed(ebiten.KeyS) {
		a.askHit(quiz.Single)
	}
	if ctrl && inpututil.IsKeyJustPressed(ebiten.KeyD) {
		a.askHit(quiz.Double)
	}
	if ctrl && inpututil.IsKeyJustPressed(ebiten.KeyT) {
		a.askHit(quiz.Triple)
	}
	if ctrl && inpututil.IsKeyJustPressed(ebiten.KeyH) {
		a.askHit(quiz.Homer)
	}
	if click() {
		for _, b := range a.hitButtons() {
			if b.r.contains(a.mx, a.my) {
				a.askHit(b.k)
				return nil
			}
		}
	}
	return nil
}

type hitBtn struct {
	r rect
	k quiz.Kind
	s string
}

func (a *App) hitButtons() []hitBtn {
	y := winH - 36
	return []hitBtn{
		{rect{12, y, 90, 26}, quiz.Single, "Single"},
		{rect{110, y, 90, 26}, quiz.Double, "Double"},
		{rect{208, y, 90, 26}, quiz.Triple, "Triple"},
		{rect{306, y, 110, 26}, quiz.Homer, "Home Run"},
	}
}

func (a *App) drawPlay(dst *ebiten.Image) {
	fill(dst, 0, 0, winW, winH, colFace)
	if a.field != nil {
		op := &ebiten.DrawImageOptions{}
		op.GeoM.Translate(0, float64(menuH))
		dst.DrawImage(a.field, op)
	}
	a.drawScoreboard(dst)
	a.drawMessage(dst)
	a.drawOccupants(dst)
	raised(dst, 0, winH-40, winW, 40)
	for _, b := range a.hitButtons() {
		button(dst, b.r, b.s, a.face, false, b.r.contains(a.mx, a.my))
	}
	if a.m != nil {
		info := fmt.Sprintf("Outs: %d of %d    Team batting: %s", a.m.Outs, a.m.MaxOuts(), a.m.TeamName(a.m.Batting()))
		if a.m.Opt.Sound {
			info += "    Sound is on"
		} else {
			info += "    Sound is off"
		}
		drawText(dst, info, a.small, 430, winH-30, colText)
	}
	a.drawMenu(dst)
}

func (a *App) drawScoreboard(dst *ebiten.Image) {
	if a.m == nil {
		return
	}
	x, y := 318, menuH+20
	w, h := 352, 82
	fill(dst, x, y, w, h, color.RGBA{0, 0, 0, 230})
	drawText(dst, "  1  2  3  4  5  6  7  8  9    R", a.board, x+70, y+6, colYellow)
	for team := 0; team < 2; team++ {
		yy := y + 28 + team*22
		name := clipRunes(a.m.TeamName(team), 8)
		c := colWhite
		if team == a.m.Batting() && !a.m.Over {
			c = colYellow
		}
		drawText(dst, name, a.small, x+6, yy, c)
		xx := x + 78
		for inn := 1; inn <= 9; inn++ {
			s := "-"
			if inn < a.m.Inning || (inn == a.m.Inning && (team == 0 || a.m.Bottom || a.m.Over)) {
				s = fmt.Sprintf("%d", a.m.Score[team][inn])
			}
			if inn == a.m.Inning && team == a.m.Batting() && !a.m.Over {
				drawText(dst, s, a.board, xx, yy, colYellow)
			} else {
				drawText(dst, s, a.board, xx, yy, colWhite)
			}
			xx += 22
		}
		drawText(dst, fmt.Sprintf("%2d", a.m.Total(team)), a.board, x+w-28, yy, colYellow)
	}
}

func (a *App) drawMessage(dst *ebiten.Image) {
	if a.msg == "" {
		return
	}
	x, y, w := 220, menuH+155, 360
	lines := wrapText(a.msg, a.face, w-16)
	h := 12 + 16*len(lines)
	fill(dst, x, y, w, h, colGrassMsg)
	hline(dst, x, y, w, colYellow)
	hline(dst, x, y+h-1, w, colYellow)
	yy := y + 6
	for _, ln := range lines {
		drawText(dst, ln, a.face, x+8, yy, colYellow)
		yy += 16
	}
}

func (a *App) drawOccupants(dst *ebiten.Image) {
	if a.m == nil {
		return
	}
	homeTeam := a.m.Batting() == 1
	pts := basePoints()
	if len(a.runners) > 0 {
		for _, r := range a.runners {
			drawPlayer(dst, int(r.x), menuH+int(r.y), r.home, 0)
		}
		return
	}
	// Batter in the box.
	drawPlayer(dst, pts[0].x+10, menuH+pts[0].y+8, homeTeam, 0)
	for i, on := range a.m.Bases {
		if on {
			drawPlayer(dst, pts[i+1].x, menuH+pts[i+1].y-6, homeTeam, 0)
		}
	}
	if a.m.Opt.Fielders {
		// Idle bob on the three drawn-in fielder spots.
		off := int(math.Sin(a.bob) * 2)
		drawPlayer(dst, 348, menuH+400+off, !homeTeam, 1)
	}
}

func drawPlayer(dst *ebiten.Image, x, y int, homeTeam bool, kind int) {
	body := colBlue
	if homeTeam {
		body = colRed
	}
	if kind == 1 {
		body = color.RGBA{0x20, 0x20, 0x20, 0xFF}
	}
	fill(dst, x-4, y-10, 8, 8, colSkin) // head
	fill(dst, x-5, y-2, 10, 12, body)   // body
	fill(dst, x-5, y+10, 4, 8, colDark) // legs
	fill(dst, x+1, y+10, 4, 8, colDark)
}

func (a *App) updateQuestion() error {
	if a.m != nil && a.m.Opt.Timed {
		a.qTicks++
		if a.qTicks > 15*60 {
			a.m.LastRef = a.q.Ref
			if a.fielding {
				a.resolveFielding(false)
				return nil
			}
			_, msg := a.m.ApplyOut()
			a.msg = "Umpire's Delay of Game Warning\n" + msg
			a.afterPlay()
			return nil
		}
	}
	if inpututil.IsKeyJustPressed(ebiten.KeyR) {
		a.showRef = true
	}
	keys := []ebiten.Key{ebiten.Key1, ebiten.Key2, ebiten.Key3, ebiten.Key4,
		ebiten.KeyA, ebiten.KeyB, ebiten.KeyC, ebiten.KeyD}
	for i, k := range keys {
		if inpututil.IsKeyJustPressed(k) {
			a.answer(i % 4)
			return nil
		}
	}
	if click() {
		x, y, w, _ := a.questionBox()
		ref := rect{x + 16, y + 268, 100, 24}
		if ref.contains(a.mx, a.my) {
			a.showRef = true
		}
		for i := 0; i < 4; i++ {
			r := rect{x + 24, y + 118 + i*34, w - 48, 30}
			if r.contains(a.mx, a.my) {
				a.answer(i)
				return nil
			}
		}
	}
	if inpututil.IsKeyJustPressed(ebiten.KeyEscape) {
		if a.fielding {
			a.resolveFielding(false)
			return nil
		}
		a.scr = screenPlay
	}
	return nil
}

func (a *App) questionBox() (x, y, w, h int) {
	w, h = 560, 320
	x, y = (winW-w)/2, (winH-h)/2
	return
}

func (a *App) drawQuestion(dst *ebiten.Image) {
	x, y, w, h := a.questionBox()
	title := a.qKind.String() + " Question"
	if a.fielding && a.m != nil {
		title = a.m.TeamName(a.m.Fielding()) + " — put them out!"
	}
	windowFrame(dst, x, y, w, h, title, a.title)
	yy := y + 28
	if a.fielding {
		drawText(dst, a.qKind.String()+" is in play. Answer right for an out.", a.small, x+20, yy, colNavy)
		yy += 16
	}
	for _, ln := range wrapText(a.q.Text, a.face, w-40) {
		drawText(dst, ln, a.face, x+20, yy, colText)
		yy += 16
	}
	letters := []string{"A", "B", "C", "D"}
	for i := 0; i < 4; i++ {
		r := rect{x + 24, y + 118 + i*34, w - 48, 30}
		hover := r.contains(a.mx, a.my)
		raised(dst, r.X, r.Y, r.W, r.H)
		if hover {
			fill(dst, r.X+2, r.Y+2, r.W-4, r.H-4, color.RGBA{0xD8, 0xD8, 0xE8, 0xFF})
		}
		label := letters[i] + ")  " + a.q.Choices[i]
		drawText(dst, label, a.face, r.X+10, r.Y+8, colText)
	}
	ref := rect{x + 16, y + 268, 100, 24}
	button(dst, ref, "Reference", a.small, false, ref.contains(a.mx, a.my))
	if a.showRef {
		drawText(dst, a.q.Ref, a.face, x+130, y+272, colNavy)
		drawText(dst, "(look it up in your Bible!)", a.small, x+130, y+288, colShadow)
	} else if a.m != nil && a.m.Opt.Timed {
		left := 15 - a.qTicks/60
		if left < 0 {
			left = 0
		}
		drawText(dst, fmt.Sprintf("Time: %d", left), a.face, x+w-100, y+272, colRed)
	}
}
