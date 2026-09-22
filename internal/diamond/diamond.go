package diamond

import (
	"fmt"

	"github.com/caleb-parrot/winbb/internal/quiz"
)

type Options struct {
	Sound        bool
	Fielders     bool
	Runners      bool
	OneOut       bool
	NineRun      bool
	SevenInnings bool // regulation 7; extras through 9 if tied
	Timed        bool
	OldOnly      bool
	NewOnly      bool
}

func DefaultOptions() Options {
	return Options{
		Sound:        true,
		Fielders:     true,
		Runners:      true,
		NineRun:      true,
		SevenInnings: true,
	}
}

// Match is one 9-inning game. Team 0 bats in the top (visitors), team 1 in the bottom (home).
type Match struct {
	Visitor string
	Home    string
	Opt     Options

	Inning int  // 1–9
	Bottom bool // false = top
	Outs   int
	// Score[team][inning] with inning 1–9. Index 0 unused.
	Score [2][10]int
	Hits  [2]int
	// Bases: 0=first, 1=second, 2=third.
	Bases   [3]bool
	Used    map[int]bool
	LastRef string
	Over    bool
	Result  string
}

const MaxInnings = 9

func New(visitor, home string, opt Options) *Match {
	if visitor == "" {
		visitor = "Visitors"
	}
	if home == "" {
		home = "Home"
	}
	if opt.OldOnly && opt.NewOnly {
		opt.OldOnly, opt.NewOnly = false, false
	}
	return &Match{
		Visitor: visitor,
		Home:    home,
		Opt:     opt,
		Inning:  1,
		Used:    map[int]bool{},
	}
}

func (m *Match) Batting() int {
	if m.Bottom {
		return 1
	}
	return 0
}

func (m *Match) Fielding() int { return 1 - m.Batting() }

func (m *Match) TeamName(i int) string {
	if i == 1 {
		return m.Home
	}
	return m.Visitor
}

func (m *Match) Total(team int) int {
	n := 0
	for inn := 1; inn <= MaxInnings; inn++ {
		n += m.Score[team][inn]
	}
	return n
}

func (m *Match) HalfLabel() string {
	half := "Top"
	if m.Bottom {
		half = "Bottom"
	}
	return fmt.Sprintf("%s %d", half, m.Inning)
}

func (m *Match) MaxOuts() int {
	if m.Opt.OneOut {
		return 1
	}
	return 3
}

// Regulation is 7 when that option is on, otherwise 9. Extras never go past MaxInnings.
func (m *Match) Regulation() int {
	if m.Opt.SevenInnings {
		return 7
	}
	return MaxInnings
}

func (m *Match) Prompt() string {
	if m.Over {
		return m.Result
	}
	if m.Outs == 0 && !m.Bases[0] && !m.Bases[1] && !m.Bases[2] {
		if m.Inning == 1 && !m.Bottom {
			return "First batter, select the type of hit."
		}
		return "First batter for next team, select type of hit."
	}
	return "Next batter, select type of hit."
}

// ApplyHit moves runners. halfOver is true when the half-inning (or game) ended.
func (m *Match) ApplyHit(kind quiz.Kind) (runs int, halfOver bool, msg string) {
	if m.Over {
		return 0, true, m.Result
	}
	if m.Inning < 1 {
		m.Inning = 1
	}
	if m.Inning > MaxInnings {
		m.finish()
		return 0, true, m.Result
	}
	n := kind.Bases()
	var occ [4]bool
	for i := 2; i >= 0; i-- {
		if !m.Bases[i] {
			continue
		}
		dest := (i + 1) + n
		if dest >= 4 {
			runs++
		} else {
			occ[dest] = true
		}
	}
	if n >= 4 {
		runs++
	} else {
		occ[n] = true
	}
	m.Bases = [3]bool{occ[1], occ[2], occ[3]}
	m.Hits[m.Batting()]++

	capped := false
	if m.Opt.NineRun {
		already := m.Score[m.Batting()][m.Inning]
		if already+runs > 9 {
			runs = 9 - already
			if runs < 0 {
				runs = 0
			}
			capped = true
		}
	}
	m.Score[m.Batting()][m.Inning] += runs

	word := map[quiz.Kind]string{
		quiz.Single: "single!",
		quiz.Double: "double!",
		quiz.Triple: "triple!",
		quiz.Homer:  "Home Run!",
	}[kind]
	msg = "It's a hit!     " + word
	if runs == 1 {
		msg += "  1 run scores."
	} else if runs > 1 {
		msg += fmt.Sprintf("  %d runs score.", runs)
	}
	if m.walkOff() {
		msg += "  Walk-off — game over."
		m.finish()
		return runs, true, msg
	}
	if capped || (m.Opt.NineRun && m.Score[m.Batting()][m.Inning] >= 9) {
		msg += "  Nine-run limit — side retired."
		m.endHalf()
		return runs, true, msg
	}
	return runs, false, msg
}

func (m *Match) ApplyOut() (halfOver bool, msg string) {
	if m.Over {
		return true, m.Result
	}
	m.Outs++
	msg = "Incorrect, batter is out!"
	if m.Outs >= m.MaxOuts() {
		msg += "  End of at-bat. Side retired."
		m.endHalf()
		return true, msg
	}
	return false, msg
}

func (m *Match) walkOff() bool {
	return m.Bottom && m.Inning >= m.Regulation() && m.Total(1) > m.Total(0)
}

func (m *Match) endHalf() bool {
	m.Bases = [3]bool{}
	m.Outs = 0
	tied := m.Total(0) == m.Total(1)
	homeLeads := m.Total(1) > m.Total(0)
	if !m.Bottom {
		m.Bottom = true
		// Skip the bottom if home already leads in a game-ending inning (7th, extras, or 9th).
		if m.Inning >= m.Regulation() && homeLeads {
			m.finish()
			return true
		}
		return false
	}
	// Completed a bottom half. Always stop after 9, even if still tied.
	if m.Inning >= MaxInnings {
		m.finish()
		return true
	}
	// After regulation (or an extra), stop if the game is not tied.
	if m.Inning >= m.Regulation() && !tied {
		m.finish()
		return true
	}
	m.Bottom = false
	m.Inning++
	if m.Inning > MaxInnings {
		m.finish()
		return true
	}
	return false
}

func (m *Match) finish() {
	m.Over = true
	m.Bases = [3]bool{}
	m.Outs = 0
	v, h := m.Total(0), m.Total(1)
	inn := m.Inning
	if inn > MaxInnings {
		inn = MaxInnings
	}
	switch {
	case v > h:
		m.Result = fmt.Sprintf("%s Wins!  (%d innings)", m.Visitor, inn)
	case h > v:
		m.Result = fmt.Sprintf("%s Wins!  (%d innings)", m.Home, inn)
	default:
		m.Result = fmt.Sprintf("Game Was Tie!  (%d innings, no extras past 9)", inn)
	}
}

// Snapshot is the JSON save format.
type Snapshot struct {
	Visitor string
	Home    string
	Opt     Options
	Inning  int
	Bottom  bool
	Outs    int
	Score   [2][10]int
	Hits    [2]int
	Bases   [3]bool
	Used    []int
	LastRef string
}

func (m *Match) Snapshot() Snapshot {
	used := make([]int, 0, len(m.Used))
	for id := range m.Used {
		used = append(used, id)
	}
	return Snapshot{
		Visitor: m.Visitor,
		Home:    m.Home,
		Opt:     m.Opt,
		Inning:  m.Inning,
		Bottom:  m.Bottom,
		Outs:    m.Outs,
		Score:   m.Score,
		Hits:    m.Hits,
		Bases:   m.Bases,
		Used:    used,
		LastRef: m.LastRef,
	}
}

func FromSnapshot(s Snapshot) *Match {
	used := map[int]bool{}
	for _, id := range s.Used {
		used[id] = true
	}
	if s.Inning < 1 {
		s.Inning = 1
	}
	return &Match{
		Visitor: s.Visitor,
		Home:    s.Home,
		Opt:     s.Opt,
		Inning:  s.Inning,
		Bottom:  s.Bottom,
		Outs:    s.Outs,
		Score:   s.Score,
		Hits:    s.Hits,
		Bases:   s.Bases,
		Used:    used,
		LastRef: s.LastRef,
	}
}

func (s Snapshot) Label() string {
	v, h := 0, 0
	for i := 1; i <= 9; i++ {
		v += s.Score[0][i]
		h += s.Score[1][i]
	}
	half := "Top"
	if s.Bottom {
		half = "Bot"
	}
	return fmt.Sprintf("%s vs %s  %s %d  %d-%d", s.Visitor, s.Home, half, s.Inning, v, h)
}
