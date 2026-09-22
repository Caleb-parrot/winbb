package ui

import (
	"fmt"

	"github.com/caleb-parrot/winbb/internal/diamond"
	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/inpututil"
)

func (a *App) pregameBox() (x, y, w, h int) {
	w, h = 560, 548
	x, y = (winW-w)/2, (winH-h)/2
	return
}

func (a *App) updatePregame() error {
	if a.menuOpen != "" {
		return nil
	}
	x, y, _, _ := a.pregameBox()
	vis := rect{x + 200, y + 64, 220, 22}
	home := rect{x + 200, y + 92, 220, 22}
	if click() {
		switch {
		case vis.contains(a.mx, a.my):
			a.focus = 0
		case home.contains(a.mx, a.my):
			a.focus = 1
		default:
			for i, r := range a.optionRects() {
				if r.contains(a.mx, a.my) {
					a.toggleOpt(i)
				}
			}
			start := rect{x + 40, y + 498, 150, 28}
			res := rect{x + 205, y + 498, 180, 28}
			quit := rect{x + 400, y + 498, 90, 28}
			if start.contains(a.mx, a.my) {
				a.startNew()
			}
			if res.contains(a.mx, a.my) {
				a.saves = loadSaves()
				if len(a.saves) == 0 {
					a.popup("Sorry there are NO previously saved games!\nSelect OK to return to Pre-game screen.")
				} else {
					a.selSav = 0
					a.scr = screenResume
				}
			}
			if quit.contains(a.mx, a.my) {
				a.quit = true
			}
		}
	}
	if a.focus == 0 {
		a.typeInto(&a.visitor)
	} else {
		a.typeInto(&a.home)
	}
	if inpututil.IsKeyJustPressed(ebiten.KeyTab) {
		a.focus = 1 - a.focus
	}
	if inpututil.IsKeyJustPressed(ebiten.KeyEnter) {
		a.startNew()
	}
	return nil
}

func (a *App) optionRects() []rect {
	x, y, _, _ := a.pregameBox()
	labels := a.optionLabels()
	out := make([]rect, len(labels))
	for i := range labels {
		out[i] = rect{x + 40, y + 150 + i*28, 480, 20}
	}
	return out
}

func (a *App) optionLabels() []string {
	return []string{
		"Start game with Sound turned OFF",
		"Start game with Fielder Animation OFF",
		"Start game with Runner Animation OFF",
		"Allow only 1 out per half inning",
		"Set maximum runs per half inning to 9",
		"Set time limit for answering (15 sec.)",
		"Use only Old Testament questions",
		"Use only New Testament questions",
		a.clearMemLabel(),
	}
}

func (a *App) clearMemLabel() string {
	n := 0
	if a.asked != nil {
		n = len(a.asked)
	}
	total := 0
	if a.bank != nil {
		total = len(a.bank.All)
	}
	return fmt.Sprintf("Clear remembered questions (%d of %d)", n, total)
}

func (a *App) toggleOpt(i int) {
	switch i {
	case 0:
		a.opt.Sound = !a.opt.Sound
	case 1:
		a.opt.Fielders = !a.opt.Fielders
	case 2:
		a.opt.Runners = !a.opt.Runners
	case 3:
		a.opt.OneOut = !a.opt.OneOut
	case 4:
		a.opt.NineRun = !a.opt.NineRun
	case 5:
		a.opt.Timed = !a.opt.Timed
	case 6:
		a.opt.OldOnly = !a.opt.OldOnly
	case 7:
		a.opt.NewOnly = !a.opt.NewOnly
	case 8:
		a.clearMem = !a.clearMem
	}
	a.snd.enabled = a.opt.Sound
}

func (a *App) optOn(i int) bool {
	// Pregame checkboxes are phrased as the OFF/limit options.
	switch i {
	case 0:
		return !a.opt.Sound
	case 1:
		return !a.opt.Fielders
	case 2:
		return !a.opt.Runners
	case 3:
		return a.opt.OneOut
	case 4:
		return a.opt.NineRun
	case 5:
		return a.opt.Timed
	case 6:
		return a.opt.OldOnly
	case 7:
		return a.opt.NewOnly
	case 8:
		return a.clearMem
	}
	return false
}

func (a *App) drawPregame(dst *ebiten.Image) {
	fill(dst, 0, 0, winW, winH, colTeal)
	a.drawMenu(dst)
	x, y, w, h := a.pregameBox()
	windowFrame(dst, x, y, w, h, "Bible Baseball - Pre-game Screen", a.title)
	drawText(dst, "Enter the team names as you would like them to appear", a.face, x+24, y+26, colText)
	drawText(dst, "on the scoreboard.", a.face, x+24, y+42, colText)
	drawText(dst, "Visitor Team Name:", a.face, x+24, y+68, colText)
	drawText(dst, "Home Team Name:", a.face, x+24, y+96, colText)
	vis := rect{x + 200, y + 64, 220, 22}
	home := rect{x + 200, y + 92, 220, 22}
	textField(dst, vis, a.visitor, a.face, a.focus == 0)
	textField(dst, home, a.home, a.face, a.focus == 1)

	drawText(dst, "Bible Baseball Game Options", a.title, x+40, y+128, colNavy)
	for i, label := range a.optionLabels() {
		r := a.optionRects()[i]
		checkbox(dst, r.X, r.Y, label, a.face, a.optOn(i))
	}

	start := rect{x + 40, y + 498, 150, 28}
	res := rect{x + 205, y + 498, 180, 28}
	quit := rect{x + 400, y + 498, 90, 28}
	button(dst, start, "Start New Game", a.face, false, start.contains(a.mx, a.my))
	button(dst, res, "Resume Delayed Game", a.face, false, res.contains(a.mx, a.my))
	button(dst, quit, "Quit", a.face, false, quit.contains(a.mx, a.my))
}

func (a *App) updateResume() error {
	x, y, _, _ := a.pregameBox()
	if click() {
		for i := range a.saves {
			r := rect{x + 40, y + 50 + i*22, 480, 20}
			if r.contains(a.mx, a.my) {
				a.selSav = i
			}
		}
		ok := rect{x + 140, y + 470, 90, 28}
		cancel := rect{x + 250, y + 470, 90, 28}
		if ok.contains(a.mx, a.my) {
			a.resumeSelected()
		}
		if cancel.contains(a.mx, a.my) {
			a.scr = screenPregame
		}
	}
	if inpututil.IsKeyJustPressed(ebiten.KeyEscape) {
		a.scr = screenPregame
	}
	if inpututil.IsKeyJustPressed(ebiten.KeyEnter) {
		a.resumeSelected()
	}
	if inpututil.IsKeyJustPressed(ebiten.KeyArrowUp) && a.selSav > 0 {
		a.selSav--
	}
	if inpututil.IsKeyJustPressed(ebiten.KeyArrowDown) && a.selSav < len(a.saves)-1 {
		a.selSav++
	}
	return nil
}

func (a *App) resumeSelected() {
	if a.selSav < 0 || a.selSav >= len(a.saves) {
		a.popup("No previously saved game was selected!")
		return
	}
	a.m = diamond.FromSnapshot(a.saves[a.selSav])
	a.opt = a.m.Opt
	a.visitor, a.home = a.m.Visitor, a.m.Home
	a.snd.enabled = a.m.Opt.Sound
	if a.m.Used == nil {
		a.m.Used = map[int]bool{}
	}
	for id := range a.bank.IDsForKeys(a.asked) {
		a.m.Used[id] = true
	}
	a.msg = a.m.Prompt()
	a.scr = screenPlay
	a.fielding = false
	_ = deleteSave(a.selSav)
}

func (a *App) drawResume(dst *ebiten.Image) {
	w, h := 560, 420
	x, y := (winW-w)/2, (winH-h)/2
	windowFrame(dst, x, y, w, h, "Bible Baseball Resume Delayed Game", a.title)
	drawText(dst, "List of Previously Saved Games", a.face, x+24, y+28, colText)
	sunken(dst, x+24, y+48, w-48, 300)
	fill(dst, x+26, y+50, w-52, 296, colWhite)
	for i, s := range a.saves {
		if i > 12 {
			break
		}
		yy := y + 54 + i*22
		r := rect{x + 28, yy, w - 56, 20}
		if i == a.selSav {
			fill(dst, r.X, r.Y, r.W, r.H, colNavy)
			drawText(dst, s.Label(), a.face, r.X+6, r.Y+3, colWhite)
		} else {
			drawText(dst, s.Label(), a.face, r.X+6, r.Y+3, colText)
		}
	}
	ok := rect{x + 140, y + 370, 90, 28}
	cancel := rect{x + 250, y + 370, 90, 28}
	button(dst, ok, "OK", a.face, false, ok.contains(a.mx, a.my))
	button(dst, cancel, "Cancel", a.face, false, cancel.contains(a.mx, a.my))
}
