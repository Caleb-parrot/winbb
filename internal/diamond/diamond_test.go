package diamond

import (
	"strings"
	"testing"

	"github.com/caleb-parrot/winbb/internal/quiz"
)

func TestDefaultNineRun(t *testing.T) {
	if !DefaultOptions().NineRun {
		t.Fatal("nine-run limit should be on by default")
	}
}

func TestDefaultSevenInnings(t *testing.T) {
	if !DefaultOptions().SevenInnings {
		t.Fatal("7-inning games should be on by default")
	}
}

func TestAdvanceEmptySingle(t *testing.T) {
	m := New("V", "H", DefaultOptions())
	runs, half, _ := m.ApplyHit(quiz.Single)
	if runs != 0 || half || !m.Bases[0] || m.Bases[1] || m.Bases[2] {
		t.Fatalf("bases=%v runs=%d half=%v", m.Bases, runs, half)
	}
}

func TestBasesLoadedHomer(t *testing.T) {
	m := New("V", "H", DefaultOptions())
	m.Bases = [3]bool{true, true, true}
	runs, half, _ := m.ApplyHit(quiz.Homer)
	if runs != 4 || half {
		t.Fatalf("runs=%d half=%v", runs, half)
	}
	if m.Bases != [3]bool{} {
		t.Fatalf("bases %v", m.Bases)
	}
	if m.Total(0) != 4 {
		t.Fatalf("score %d", m.Total(0))
	}
}

func TestRunnerOnFirstDouble(t *testing.T) {
	m := New("V", "H", DefaultOptions())
	m.Bases = [3]bool{true, false, false}
	runs, _, _ := m.ApplyHit(quiz.Double)
	// runner 1st -> 3rd, batter to 2nd
	if runs != 0 || m.Bases != [3]bool{false, true, true} {
		t.Fatalf("bases=%v runs=%d", m.Bases, runs)
	}
}

func TestThreeOutsSwitch(t *testing.T) {
	m := New("V", "H", DefaultOptions())
	for i := 0; i < 2; i++ {
		over, _ := m.ApplyOut()
		if over {
			t.Fatalf("half ended early at out %d", i+1)
		}
	}
	over, _ := m.ApplyOut()
	if !over && m.Bottom && m.Outs == 0 && m.Inning == 1 {
		// endHalf returns false (game not over) but sets Bottom
	}
	if !m.Bottom || m.Outs != 0 || m.Inning != 1 {
		t.Fatalf("after 3 outs: inn=%d bottom=%v outs=%d overHalfReturned=%v", m.Inning, m.Bottom, m.Outs, over)
	}
}

func TestNineInningsTie(t *testing.T) {
	m := New("V", "H", DefaultOptions())
	m.Inning = 9
	m.Bottom = true
	m.ApplyOut()
	m.ApplyOut()
	m.ApplyOut()
	if !m.Over || !strings.Contains(m.Result, "Tie") {
		t.Fatalf("over=%v result=%q", m.Over, m.Result)
	}
}

func TestHomeLeadsSkipsBottomNinth(t *testing.T) {
	m := New("V", "H", DefaultOptions())
	m.Inning = 9
	m.Score[1][1] = 1
	for i := 0; i < 3; i++ {
		m.ApplyOut()
	}
	if !m.Over || !strings.Contains(m.Result, "H Wins") {
		t.Fatalf("over=%v result=%q bottom=%v inn=%d", m.Over, m.Result, m.Bottom, m.Inning)
	}
}

func TestFullNineInningsEnds(t *testing.T) {
	m := New("V", "H", DefaultOptions())
	for i := 0; i < 60; i++ {
		m.ApplyOut()
		if m.Over {
			break
		}
	}
	if !m.Over {
		t.Fatalf("still going after many outs inn=%d bottom=%v", m.Inning, m.Bottom)
	}
	if m.Inning > MaxInnings {
		t.Fatalf("played extra innings: %d", m.Inning)
	}
}

func TestWalkOffInNinth(t *testing.T) {
	m := New("V", "H", DefaultOptions())
	m.Inning = 9
	m.Bottom = true
	m.Score[0][1] = 3
	m.Score[1][1] = 3
	_, half, _ := m.ApplyHit(quiz.Homer)
	if !half || !m.Over || !strings.Contains(m.Result, "H Wins") {
		t.Fatalf("walk-off: over=%v half=%v result=%q %d-%d", m.Over, half, m.Result, m.Total(0), m.Total(1))
	}
}

func TestNoTenthInning(t *testing.T) {
	m := New("V", "H", DefaultOptions())
	m.Inning = 9
	m.Bottom = true
	m.ApplyOut()
	m.ApplyOut()
	m.ApplyOut()
	if !m.Over || m.Inning != 9 {
		t.Fatalf("over=%v inn=%d", m.Over, m.Inning)
	}
	_, half, _ := m.ApplyHit(quiz.Single)
	if !half || !m.Over {
		t.Fatal("should refuse to play after 9 innings")
	}
}

func TestSevenInningsEndsIfNotTied(t *testing.T) {
	opt := DefaultOptions()
	opt.SevenInnings = true
	m := New("V", "H", opt)
	m.Score[0][1] = 1
	for i := 0; i < 50; i++ {
		m.ApplyOut()
		if m.Over {
			break
		}
	}
	if !m.Over || m.Inning != 7 {
		t.Fatalf("over=%v inn=%d result=%q", m.Over, m.Inning, m.Result)
	}
}

func TestSevenInningsExtrasIfTied(t *testing.T) {
	opt := DefaultOptions()
	opt.SevenInnings = true
	m := New("V", "H", opt)
	for i := 0; i < 42; i++ {
		m.ApplyOut()
		if m.Over {
			t.Fatalf("ended while tied after out %d inn=%d", i+1, m.Inning)
		}
	}
	if m.Over || m.Inning != 8 || m.Bottom {
		t.Fatalf("expected top 8, inn=%d bottom=%v over=%v", m.Inning, m.Bottom, m.Over)
	}
}

func TestSevenInningsHardStopAtNine(t *testing.T) {
	opt := DefaultOptions()
	opt.SevenInnings = true
	m := New("V", "H", opt)
	for i := 0; i < 80; i++ {
		m.ApplyOut()
		if m.Over {
			break
		}
	}
	if !m.Over || m.Inning != 9 {
		t.Fatalf("over=%v inn=%d", m.Over, m.Inning)
	}
	if !strings.Contains(m.Result, "Tie") {
		t.Fatalf("result %q", m.Result)
	}
}

func TestWalkOffInSeventh(t *testing.T) {
	opt := DefaultOptions()
	opt.SevenInnings = true
	m := New("V", "H", opt)
	m.Inning = 7
	m.Bottom = true
	m.Score[0][1] = 2
	m.Score[1][1] = 2
	m.ApplyHit(quiz.Homer)
	if !m.Over || !strings.Contains(m.Result, "H Wins") {
		t.Fatalf("over=%v result=%q", m.Over, m.Result)
	}
}

func TestSevenSkipBottomIfHomeLeads(t *testing.T) {
	opt := DefaultOptions()
	opt.SevenInnings = true
	m := New("V", "H", opt)
	m.Inning = 7
	m.Score[1][1] = 1
	m.ApplyOut()
	m.ApplyOut()
	m.ApplyOut()
	if !m.Over || !strings.Contains(m.Result, "H Wins") {
		t.Fatalf("over=%v inn=%d bottom=%v result=%q", m.Over, m.Inning, m.Bottom, m.Result)
	}
}

func TestNineModeContinuesPastSeven(t *testing.T) {
	opt := DefaultOptions()
	opt.SevenInnings = false
	m := New("V", "H", opt)
	m.Score[0][1] = 1
	m.Inning = 7
	m.Bottom = true
	m.ApplyOut()
	m.ApplyOut()
	m.ApplyOut()
	if m.Over || m.Inning != 8 {
		t.Fatalf("over=%v inn=%d", m.Over, m.Inning)
	}
}

func TestOneOutOption(t *testing.T) {
	opt := DefaultOptions()
	opt.OneOut = true
	m := New("V", "H", opt)
	over, _ := m.ApplyOut()
	if !m.Bottom || m.Outs != 0 {
		t.Fatalf("one-out should retire the side: bottom=%v outs=%d halfOver=%v", m.Bottom, m.Outs, over)
	}
}

func TestNineRunCap(t *testing.T) {
	opt := DefaultOptions()
	opt.NineRun = true
	m := New("V", "H", opt)
	m.Bases = [3]bool{true, true, true}
	m.Score[0][1] = 7
	runs, half, _ := m.ApplyHit(quiz.Homer)
	if runs != 2 || !half {
		t.Fatalf("cap runs=%d half=%v score=%d", runs, half, m.Score[0][1])
	}
	if m.Score[0][1] != 9 {
		t.Fatalf("inning score %d", m.Score[0][1])
	}
	if !m.Bottom {
		t.Fatal("side should be retired")
	}
}

func TestSnapshotRoundTrip(t *testing.T) {
	m := New("A", "B", DefaultOptions())
	m.ApplyHit(quiz.Triple)
	m.Used[3] = true
	m.LastRef = "John 3:16"
	got := FromSnapshot(m.Snapshot())
	if got.Visitor != "A" || got.Bases != m.Bases || !got.Used[3] || got.LastRef != "John 3:16" {
		t.Fatalf("%+v", got)
	}
}
