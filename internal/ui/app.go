package ui

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"unicode/utf8"

	"github.com/caleb-parrot/winbb/assets"
	"github.com/caleb-parrot/winbb/internal/diamond"
	"github.com/caleb-parrot/winbb/internal/quiz"
	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/inpututil"
	text "github.com/hajimehoshi/ebiten/v2/text/v2"
)

const (
	winW  = 990
	menuH = 22
	winH  = menuH + 744
)

type screen int

const (
	screenPregame screen = iota
	screenPlay
	screenQuestion
	screenHelp
	screenAbout
	screenResume
	screenAlert
	screenGameOver
	screenQuitConfirm
)

type App struct {
	bank *quiz.Bank
	m    *diamond.Match
	snd  *sounds

	face, small, title, board, qface *text.GoXFace
	field                            *ebiten.Image

	scr     screen
	prevScr screen
	alert   string

	opt      diamond.Options
	visitor  string
	home     string
	focus    int // 0 visitor, 1 home
	menuOpen string
	asked    map[string]bool
	clearMem bool

	msg      string
	q        quiz.Question
	qKind    quiz.Kind
	qTicks   int
	fielding bool
	pressed  string

	saves  []diamond.Snapshot
	selSav int

	runners []runner
	bob     float64

	mx, my int
	quit   bool
}

type runner struct {
	pts    []point
	t, dur float64
	home   bool
	x, y   float64
}

func New() (*App, error) {
	qpath := findQuestions()
	f, err := os.Open(qpath)
	if err != nil {
		b, e2 := assets.FS.Open("bible.qus")
		if e2 != nil {
			return nil, fmt.Errorf("sorry there is NO question file in the current directory")
		}
		defer b.Close()
		bank, err := quiz.Parse(b)
		if err != nil {
			return nil, err
		}
		return newApp(bank)
	}
	defer f.Close()
	bank, err := quiz.Parse(f)
	if err != nil {
		return nil, err
	}
	return newApp(bank)
}

func findQuestions() string {
	cands := []string{"BIBLE.QUS", "bible.qus"}
	if exe, err := os.Executable(); err == nil {
		dir := filepath.Dir(exe)
		cands = append(cands, filepath.Join(dir, "BIBLE.QUS"), filepath.Join(dir, "bible.qus"))
	}
	for _, p := range cands {
		if _, err := os.Stat(p); err == nil {
			return p
		}
	}
	return "bible.qus"
}

func newApp(bank *quiz.Bank) (*App, error) {
	img, _, err := loadPNG("field.png")
	if err != nil {
		return nil, err
	}
	ui, small, title, board, qface := loadFaces()
	a := &App{
		bank:    bank,
		snd:     loadSounds(),
		face:    ui,
		small:   small,
		title:   title,
		board:   board,
		qface:   qface,
		field:   img,
		opt:     diamond.DefaultOptions(),
		visitor: "Visitors",
		home:    "Home",
		scr:     screenPregame,
		asked:   loadAsked(),
	}
	a.snd.enabled = a.opt.Sound
	return a, nil
}

func loadPNG(name string) (*ebiten.Image, string, error) {
	f, err := assets.FS.Open(name)
	if err != nil {
		return nil, "", err
	}
	defer f.Close()
	img, err := decodeImage(f)
	if err != nil {
		return nil, "", err
	}
	return img, name, nil
}

func (a *App) Layout(ow, oh int) (int, int) { return winW, winH }

func (a *App) Update() error {
	if a.quit {
		return ebiten.Termination
	}
	a.mx, a.my = ebiten.CursorPosition()
	if a.scr == screenPlay && a.m != nil && a.m.Opt.Fielders {
		a.bob += 0.08
	}
	a.stepRunners()
	if a.updateMenu() {
		return nil
	}
	if inpututil.IsKeyJustPressed(ebiten.KeyF1) && a.scr != screenHelp {
		a.openModal(screenHelp)
		return nil
	}
	switch a.scr {
	case screenPregame:
		return a.updatePregame()
	case screenPlay:
		return a.updatePlay()
	case screenQuestion:
		return a.updateQuestion()
	case screenHelp, screenAbout:
		if click() || inpututil.IsKeyJustPressed(ebiten.KeyEscape) || inpututil.IsKeyJustPressed(ebiten.KeyEnter) {
			a.scr = a.prevScr
		}
	case screenResume:
		return a.updateResume()
	case screenAlert, screenGameOver:
		if click() || inpututil.IsKeyJustPressed(ebiten.KeyEnter) || inpututil.IsKeyJustPressed(ebiten.KeyEscape) || inpututil.IsKeyJustPressed(ebiten.KeySpace) {
			if a.scr == screenGameOver {
				a.scr = screenPregame
				a.m = nil
				a.fielding = false
			} else {
				a.scr = a.prevScr
			}
		}
	case screenQuitConfirm:
		return a.updateQuitConfirm()
	}
	return nil
}

func (a *App) Draw(scr *ebiten.Image) {
	switch a.scr {
	case screenPregame, screenResume:
		a.drawPregame(scr)
		if a.scr == screenResume {
			a.drawResume(scr)
		}
	default:
		a.drawPlay(scr)
		switch a.scr {
		case screenQuestion:
			a.drawQuestion(scr)
		case screenHelp:
			a.drawHelp(scr)
		case screenAbout:
			a.drawAbout(scr)
		case screenAlert, screenGameOver:
			a.drawAlert(scr)
		case screenQuitConfirm:
			a.drawQuitConfirm(scr)
		}
	}
}

func (a *App) popup(msg string) {
	a.alert = msg
	a.prevScr = a.scr
	if a.prevScr == screenAlert {
		a.prevScr = screenPlay
	}
	a.scr = screenAlert
}

func (a *App) openModal(s screen) {
	if a.scr != s {
		a.prevScr = a.scr
	}
	a.scr = s
	a.menuOpen = ""
}

func click() bool {
	return inpututil.IsMouseButtonJustPressed(ebiten.MouseButtonLeft)
}

func (a *App) startNew() {
	both := a.opt.OldOnly && a.opt.NewOnly
	if both {
		a.opt.OldOnly, a.opt.NewOnly = false, false
	}
	if a.clearMem {
		a.asked = map[string]bool{}
		_ = writeAsked(a.asked)
		a.clearMem = false
	}
	a.m = diamond.New(a.visitor, a.home, a.opt)
	a.m.Used = a.bank.IDsForKeys(a.asked)
	a.snd.enabled = a.opt.Sound
	a.msg = a.m.Prompt()
	a.scr = screenPlay
	a.menuOpen = ""
	a.runners = nil
	a.fielding = false
	if a.opt.Sound {
		a.snd.PlayBall()
	}
	if both {
		a.popup("You selected ONLY Old and ONLY New Testament questions!\nI'm going to assume that you want ALL questions.")
	}
}

func (a *App) askHit(k quiz.Kind) {
	if a.m == nil || a.m.Over || len(a.runners) > 0 {
		return
	}
	ot, nt := !a.m.Opt.NewOnly, !a.m.Opt.OldOnly
	q, ok := a.bank.Pick(k, ot, nt, a.m.Used)
	if !ok {
		a.popup("No questions of that type are in the question file.")
		return
	}
	a.q = q
	a.qKind = k
	a.qTicks = 0
	a.fielding = false
	a.scr = screenQuestion
	a.menuOpen = ""
}

func (a *App) answer(choice int) {
	if a.m == nil {
		return
	}
	a.m.LastRef = a.q.Ref
	correct := choice == a.q.Correct
	if a.fielding {
		a.resolveFielding(correct)
		return
	}
	if !correct {
		_, msg := a.m.ApplyOut()
		a.msg = msg
		if a.m.Opt.Sound {
			a.snd.Groan()
		}
		a.afterPlay()
		return
	}
	a.markUsed(a.q)
	if a.qKind.FieldingPlay() && a.beginFielding() {
		return
	}
	a.awardHit("")
}

func (a *App) markUsed(q quiz.Question) {
	if a.m.Used == nil {
		a.m.Used = map[int]bool{}
	}
	a.m.Used[q.ID] = true
	if a.asked == nil {
		a.asked = map[string]bool{}
	}
	a.asked[q.Key()] = true
	_ = writeAsked(a.asked)
}

func (a *App) beginFielding() bool {
	ot, nt := !a.m.Opt.NewOnly, !a.m.Opt.OldOnly
	q, ok := a.bank.Pick(a.qKind, ot, nt, a.m.Used)
	if !ok {
		return false
	}
	a.fielding = true
	a.q = q
	a.qTicks = 0
	a.scr = screenQuestion
	a.msg = a.m.TeamName(a.m.Fielding()) + " — chance to throw them out!"
	return true
}

func (a *App) resolveFielding(correct bool) {
	fielder := a.m.TeamName(a.m.Fielding())
	a.fielding = false
	if correct {
		a.markUsed(a.q)
		_, msg := a.m.ApplyOut()
		a.msg = fielder + " made the play! Batter is out. " + msg
		if a.m.Opt.Sound {
			a.snd.Cheer()
		}
		a.afterPlay()
		return
	}
	a.awardHit(fielder + " could not make the play. ")
}

func (a *App) awardHit(prefix string) {
	old := a.m.Bases
	_, _, msg := a.m.ApplyHit(a.qKind)
	a.msg = prefix + msg
	a.launchRunners(old, a.qKind.Bases())
	if a.m.Opt.Sound {
		a.snd.Cheer()
	}
	a.afterPlay()
}

func (a *App) afterPlay() {
	a.scr = screenPlay
	if a.m != nil && a.m.Over {
		a.msg = a.m.Result
		a.prevScr = screenPlay
		a.alert = a.m.Result + fmt.Sprintf("\n\nScore was  %s %d  %s %d", a.m.Visitor, a.m.Total(0), a.m.Home, a.m.Total(1))
		a.scr = screenGameOver
	}
}

func (a *App) launchRunners(old [3]bool, hit int) {
	if a.m == nil || !a.m.Opt.Runners {
		return
	}
	path := basePoints()
	homeTeam := a.m.Batting() == 1
	var rs []runner
	dest := hit
	if dest > 4 {
		dest = 4
	}
	rs = append(rs, newRunner(path, 0, dest, homeTeam))
	for i, on := range old {
		if !on {
			continue
		}
		from := i + 1
		to := from + hit
		if to > 4 {
			to = 4
		}
		rs = append(rs, newRunner(path, from, to, homeTeam))
	}
	a.runners = rs
}

func newRunner(path []point, from, to int, home bool) runner {
	if from < 0 {
		from = 0
	}
	if to > 4 {
		to = 4
	}
	if to <= from {
		to = from + 1
		if to > 4 {
			to = 4
		}
	}
	pts := append([]point{}, path[from:to+1]...)
	if len(pts) == 0 {
		pts = []point{path[0]}
	}
	dur := 0.28 * float64(len(pts)-1)
	if dur < 0.25 {
		dur = 0.25
	}
	return runner{
		pts: pts, dur: dur, home: home,
		x: float64(pts[0].x), y: float64(pts[0].y),
	}
}

func (a *App) stepRunners() {
	if len(a.runners) == 0 {
		return
	}
	dt := 1.0 / 60.0
	live := a.runners[:0]
	for _, r := range a.runners {
		r.t += dt
		u := r.t / r.dur
		n := len(r.pts) - 1
		if n < 1 || u >= 1 {
			continue
		}
		f := u * float64(n)
		i := int(f)
		if i >= n {
			i = n - 1
		}
		local := f - float64(i)
		p0, p1 := r.pts[i], r.pts[i+1]
		r.x = float64(p0.x) + float64(p1.x-p0.x)*local
		r.y = float64(p0.y) + float64(p1.y-p0.y)*local
		live = append(live, r)
	}
	a.runners = live
}

func (a *App) saveAndExit() error {
	if a.m != nil && !a.m.Over {
		if err := appendSave(a.m.Snapshot()); err != nil {
			a.popup("Could not save game:\n" + err.Error())
			return nil
		}
	}
	a.quit = true
	return nil
}

func clipRunes(s string, n int) string {
	if utf8.RuneCountInString(s) <= n {
		return s
	}
	r := []rune(s)
	return string(r[:n])
}

func (a *App) typeInto(dst *string) {
	if inpututil.IsKeyJustPressed(ebiten.KeyBackspace) || repeating(ebiten.KeyBackspace) {
		if *dst != "" {
			r := []rune(*dst)
			*dst = string(r[:len(r)-1])
		}
	}
	var chars []rune
	chars = ebiten.AppendInputChars(chars)
	for _, ch := range chars {
		if ch < 32 {
			continue
		}
		*dst = clipRunes(*dst+string(ch), 16)
	}
}

func repeating(k ebiten.Key) bool {
	d := inpututil.KeyPressDuration(k)
	return d > 30 && d%6 == 0
}

func (a *App) drawMenu(dst *ebiten.Image) {
	raised(dst, 0, 0, winW, menuH)
	items := []struct{ id, label string }{
		{"file", "  File  "},
		{"opt", "  Options  "},
		{"help", "  Help  "},
	}
	x := 0
	for _, it := range items {
		w := textWidth(it.label, a.face) + 4
		r := rect{x, 0, w, menuH}
		if a.menuOpen == it.id {
			fill(dst, r.X, r.Y, r.W, r.H, colNavy)
			drawText(dst, it.label, a.face, r.X+2, r.Y+4, colWhite)
		} else {
			drawText(dst, it.label, a.face, r.X+2, r.Y+4, colText)
		}
		x += w
	}
	title := "Bible Baseball"
	if a.m != nil {
		title += "  —  " + a.m.HalfLabel()
	}
	drawText(dst, title, a.small, winW-textWidth(title, a.small)-12, 5, colShadow)

	if a.menuOpen == "" {
		return
	}
	var entries []string
	switch a.menuOpen {
	case "file":
		entries = []string{"New Game", "Save Game and Exit", "Exit"}
	case "opt":
		on := func(b bool, on, off string) string {
			if b {
				return off
			}
			return on
		}
		if a.m != nil {
			entries = []string{
				on(a.m.Opt.Sound, "Turn Sound On", "Turn Sound Off"),
				on(a.m.Opt.Fielders, "Turn Fielder Animation On", "Turn Fielder Animation Off"),
				on(a.m.Opt.Runners, "Turn Runner Animation On", "Turn Runner Animation Off"),
				on(a.m.Opt.OneOut, "Turn 1 Out Limit On", "Turn 1 Out Limit Off"),
				on(a.m.Opt.NineRun, "Turn 9 Run Limit On", "Turn 9 Run Limit Off"),
				on(a.m.Opt.SevenInnings, "Play 7 innings (extras to 9 if tied)", "Play 9 innings"),
				on(a.m.Opt.Timed, "Turn Answer Time Limit On", "Turn Answer Time Limit Off"),
			}
		} else {
			entries = []string{"Options apply after you start a game"}
		}
	case "help":
		entries = []string{"Instructions", "Last Reference", "About"}
	}
	maxW := 80
	for _, e := range entries {
		if w := textWidth(e, a.face) + 24; w > maxW {
			maxW = w
		}
	}
	left := 0
	if a.menuOpen == "opt" {
		left = textWidth("  File  ", a.face) + 4
	}
	if a.menuOpen == "help" {
		left = textWidth("  File  ", a.face) + 4 + textWidth("  Options  ", a.face) + 4
	}
	box := rect{left, menuH, maxW, 4 + 20*len(entries)}
	raised(dst, box.X, box.Y, box.W, box.H)
	for i, e := range entries {
		ir := rect{box.X + 2, box.Y + 2 + i*20, box.W - 4, 20}
		hover := ir.contains(a.mx, a.my)
		if hover {
			fill(dst, ir.X, ir.Y, ir.W, ir.H, colNavy)
			drawText(dst, e, a.face, ir.X+8, ir.Y+3, colWhite)
		} else {
			drawText(dst, e, a.face, ir.X+8, ir.Y+3, colText)
		}
	}
}

func (a *App) updateMenu() bool {
	if !click() {
		return a.menuOpen != "" && a.scr != screenPregame && a.scr != screenPlay
	}
	items := []struct {
		id    string
		label string
	}{
		{"file", "  File  "},
		{"opt", "  Options  "},
		{"help", "  Help  "},
	}
	x := 0
	for _, it := range items {
		w := textWidth(it.label, a.face) + 4
		r := rect{x, 0, w, menuH}
		if r.contains(a.mx, a.my) {
			if a.menuOpen == it.id {
				a.menuOpen = ""
			} else {
				a.menuOpen = it.id
			}
			return true
		}
		x += w
	}
	if a.menuOpen == "" {
		return false
	}
	n := 0
	switch a.menuOpen {
	case "file":
		n = 3
	case "opt":
		if a.m != nil {
			n = 7
		} else {
			n = 1
		}
	case "help":
		n = 3
	}
	maxW := 280
	left := 0
	if a.menuOpen == "opt" {
		left = textWidth("  File  ", a.face) + 4
	}
	if a.menuOpen == "help" {
		left = textWidth("  File  ", a.face) + 4 + textWidth("  Options  ", a.face) + 4
	}
	box := rect{left, menuH, maxW, 4 + 20*n}
	for i := 0; i < n; i++ {
		ir := rect{box.X + 2, box.Y + 2 + i*20, box.W - 4, 20}
		if ir.contains(a.mx, a.my) {
			a.menuClick(a.menuOpen, i)
			a.menuOpen = ""
			return true
		}
	}
	a.menuOpen = ""
	return true
}

func (a *App) menuClick(menu string, i int) {
	switch menu {
	case "file":
		switch i {
		case 0:
			a.scr = screenPregame
			a.m = nil
			a.fielding = false
		case 1:
			_ = a.saveAndExit()
		case 2:
			if a.m != nil && !a.m.Over {
				a.openModal(screenQuitConfirm)
			} else {
				a.quit = true
			}
		}
	case "opt":
		if a.m == nil {
			return
		}
		switch i {
		case 0:
			a.m.Opt.Sound = !a.m.Opt.Sound
			a.snd.enabled = a.m.Opt.Sound
		case 1:
			a.m.Opt.Fielders = !a.m.Opt.Fielders
		case 2:
			a.m.Opt.Runners = !a.m.Opt.Runners
		case 3:
			a.m.Opt.OneOut = !a.m.Opt.OneOut
		case 4:
			a.m.Opt.NineRun = !a.m.Opt.NineRun
		case 5:
			a.m.Opt.SevenInnings = !a.m.Opt.SevenInnings
		case 6:
			a.m.Opt.Timed = !a.m.Opt.Timed
		}
	case "help":
		switch i {
		case 0:
			a.openModal(screenHelp)
		case 1:
			ref := a.lastRef()
			if ref == "" {
				ref = "No reference yet. Answer a question first."
			} else {
				ref = "Last Reference:  " + ref
			}
			a.popup(ref)
		case 2:
			a.openModal(screenAbout)
		}
	}
}

func (a *App) lastRef() string {
	if a.m != nil {
		return a.m.LastRef
	}
	return ""
}

func (a *App) updateQuitConfirm() error {
	ok := rect{(winW - 260) / 2, 360, 70, 24}
	no := rect{(winW-260)/2 + 90, 360, 70, 24}
	cancel := rect{(winW-260)/2 + 180, 360, 70, 24}
	if click() {
		if ok.contains(a.mx, a.my) {
			return a.saveAndExit()
		}
		if no.contains(a.mx, a.my) {
			a.quit = true
			return nil
		}
		if cancel.contains(a.mx, a.my) {
			a.scr = a.prevScr
		}
	}
	if inpututil.IsKeyJustPressed(ebiten.KeyEscape) {
		a.scr = a.prevScr
	}
	return nil
}

func (a *App) drawQuitConfirm(dst *ebiten.Image) {
	x, y, w, h := (winW-360)/2, 250, 360, 150
	windowFrame(dst, x, y, w, h, "Game Postponed?", a.title)
	drawText(dst, "Do you want to save this game?", a.face, x+24, y+40, colText)
	ok := rect{x + 50, y + 110, 70, 24}
	no := rect{x + 140, y + 110, 70, 24}
	cancel := rect{x + 230, y + 110, 70, 24}
	button(dst, ok, "Yes", a.face, false, ok.contains(a.mx, a.my))
	button(dst, no, "No", a.face, false, no.contains(a.mx, a.my))
	button(dst, cancel, "Cancel", a.face, false, cancel.contains(a.mx, a.my))
}

func (a *App) drawAlert(dst *ebiten.Image) {
	lines := strings.Split(a.alert, "\n")
	w := 420
	for _, ln := range lines {
		if tw := textWidth(ln, a.face) + 48; tw > w {
			w = tw
		}
	}
	if w > 700 {
		w = 700
	}
	h := 90 + 18*len(lines)
	x, y := (winW-w)/2, (winH-h)/2
	title := "Bible Baseball"
	if a.scr == screenGameOver {
		title = "End of Game"
	}
	windowFrame(dst, x, y, w, h, title, a.title)
	yy := y + 32
	for _, ln := range lines {
		drawText(dst, ln, a.face, x+24, yy, colText)
		yy += 18
	}
	br := rect{x + w - 90, y + h - 34, 70, 24}
	button(dst, br, "OK", a.face, false, br.contains(a.mx, a.my))
}

func (a *App) drawHelp(dst *ebiten.Image) {
	w, h := 640, 460
	x, y := (winW-w)/2, (winH-h)/2
	windowFrame(dst, x, y, w, h, "Bible Baseball for Windows - Instructions", a.title)
	paras := []string{
		"It is really rather simple to play. You select the team names that you want to show on the scoreboard along with any of the other game options, and then each team takes turns batting (just like real baseball). Each batter must answer a question correctly to get on base. The difficulty of the question is determined by the type of hit the batter asks for. A missed question counts as an out!",
		"1. A batter can select the type of hit by pressing the appropriate button, or using the hot-keys (Ctrl-S, Ctrl-D, Ctrl-T, Ctrl-H).",
		"2. After you answer, Help → Last Reference shows the verse for the question you just finished. The current question does not show its reference.",
		"3. Once a question is answered correctly, it will no longer show up during the current game (unless you run out of questions). Missed questions will continue to show up.",
		"4. After a double or a triple, the fielding team gets a question of the same difficulty. A right answer is an out; a miss lets the hit stand. Home runs cannot be played.",
		"5. Correct answers are remembered across games so they do not come back. Check Clear remembered questions on the pre-game screen to start over.",
		"The game is nine innings by default. Check 7 innings on the pre-game screen to play seven, then extras through nine only if tied. The game always ends by the bottom of the ninth — no tenth. If home is already ahead after the top of a game-ending inning, or takes the lead in the bottom, the game ends.",
		"The game is a remake of the 1994 Windows 3.1 Bible trivia game Robert L. Barbor used to play in Sunday School as a child.",
	}
	yy := y + 28
	for _, p := range paras {
		for _, ln := range wrapText(p, a.small, w-40) {
			drawText(dst, ln, a.small, x+20, yy, colText)
			yy += 14
		}
		yy += 8
	}
	br := rect{x + w - 90, y + h - 34, 70, 24}
	button(dst, br, "OK", a.face, false, br.contains(a.mx, a.my))
}

func (a *App) drawAbout(dst *ebiten.Image) {
	w, h := 520, 300
	x, y := (winW-w)/2, (winH-h)/2
	windowFrame(dst, x, y, w, h, "About Bible Baseball", a.title)
	lines := []string{
		"Bible Baseball for Windows version 2.4",
		"Go remake of Robert L. Barbor's 1994 Visual Basic game.",
		"",
		"Original: written by Robert L. Barbor",
		"Graphics by Robert L. Barbor (with advice from his son)",
		"PlayBall wav file by Steven F. Trandahl",
		"",
		"This remake uses the original BIBLE.QUS question file,",
		"stadium bitmap, and crowd wavs. Drop a BIBLE.QUS next",
		"to the binary to use your own questions.",
		"",
		fmt.Sprintf("%d questions loaded.", len(a.bank.All)),
	}
	yy := y + 32
	for _, ln := range lines {
		drawText(dst, ln, a.face, x+24, yy, colText)
		yy += 16
	}
	br := rect{x + w - 90, y + h - 34, 70, 24}
	button(dst, br, "OK", a.face, false, br.contains(a.mx, a.my))
}
