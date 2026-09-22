package quiz

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

const sample = `"C01","4","C","Gen. 9:28-29","How old was Noah when he died?","90","120","950","620"
"C01","1","B","Gen. 2:2","What did God do on the 7th day?","He made man","He rested","He made light","He watched TV"
"C40","1","A","Matt. 2:1","Who was king when Jesus was born?","Herod","Pilate","Caesar ","Paul"
`

func TestParse(t *testing.T) {
	b, err := Parse(strings.NewReader(sample))
	if err != nil {
		t.Fatal(err)
	}
	if len(b.All) != 3 {
		t.Fatalf("got %d questions", len(b.All))
	}
	q := b.All[0]
	if q.Canon != 1 || q.Kind != Homer || q.Correct != 2 {
		t.Fatalf("first question: %+v", q)
	}
	if q.Choices[2] != "950" {
		t.Fatalf("choice C: %q", q.Choices[2])
	}
	if b.All[2].Testament() != "NT" {
		t.Fatalf("Matthew should be NT")
	}
}

func TestParseRejectsShort(t *testing.T) {
	_, err := Parse(strings.NewReader(`"C01","1","A","Gen. 1:1","Hi","only"`))
	if err == nil {
		t.Fatal("expected error")
	}
}

func TestIDsForKeys(t *testing.T) {
	b, err := Parse(strings.NewReader(sample))
	if err != nil {
		t.Fatal(err)
	}
	keys := map[string]bool{b.All[1].Key(): true}
	ids := b.IDsForKeys(keys)
	if !ids[1] || ids[0] || ids[2] {
		t.Fatalf("ids=%v", ids)
	}
}

func TestFieldingPlay(t *testing.T) {
	if Single.FieldingPlay() || Homer.FieldingPlay() {
		t.Fatal("single and home run should skip the fielding play")
	}
	if !Double.FieldingPlay() || !Triple.FieldingPlay() {
		t.Fatal("double and triple should allow a fielding play")
	}
}

func TestPickRespectsKindAndUsed(t *testing.T) {
	b, err := Parse(strings.NewReader(sample))
	if err != nil {
		t.Fatal(err)
	}
	used := map[int]bool{}
	q, ok := b.Pick(Single, true, true, used)
	if !ok || q.Kind != Single {
		t.Fatalf("pick single: %+v ok=%v", q, ok)
	}
	used[q.ID] = true
	q2, ok := b.Pick(Single, true, true, used)
	if !ok {
		t.Fatal("should recycle after all singles used")
	}
	if q2.Kind != Single {
		t.Fatalf("recycled kind %v", q2.Kind)
	}
}

func TestPickTestament(t *testing.T) {
	b, err := Parse(strings.NewReader(sample))
	if err != nil {
		t.Fatal(err)
	}
	q, ok := b.Pick(Single, true, false, nil)
	if !ok || q.Canon >= 40 {
		t.Fatalf("wanted OT single, got %+v ok=%v", q, ok)
	}
	q, ok = b.Pick(Single, false, true, nil)
	if !ok || q.Canon < 40 {
		t.Fatalf("wanted NT single, got %+v ok=%v", q, ok)
	}
	_, ok = b.Pick(Homer, false, true, nil)
	if ok {
		t.Fatal("no NT home-run in sample")
	}
}

func TestBundledQuestionFile(t *testing.T) {
	f, err := os.Open(filepath.Join("..", "..", "assets", "bible.qus"))
	if err != nil {
		t.Skip(err)
	}
	defer f.Close()
	b, err := Parse(f)
	if err != nil {
		t.Fatal(err)
	}
	if len(b.All) != 834 {
		t.Fatalf("got %d questions, want 834", len(b.All))
	}
	var kinds [5]int
	for _, q := range b.All {
		if q.Kind < Single || q.Kind > Homer {
			t.Fatalf("bad kind %+v", q)
		}
		kinds[q.Kind]++
	}
	if kinds[Single] == 0 || kinds[Double] == 0 || kinds[Triple] == 0 || kinds[Homer] == 0 {
		t.Fatalf("missing a hit type: %+v", kinds)
	}
}
