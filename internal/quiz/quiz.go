package quiz

import (
	"encoding/csv"
	"fmt"
	"io"
	"math/rand/v2"
	"strconv"
	"strings"
)

// Kind is the hit the batter asked for: 1 single … 4 home run.
type Kind int

const (
	Single Kind = 1
	Double Kind = 2
	Triple Kind = 3
	Homer  Kind = 4
)

func (k Kind) String() string {
	switch k {
	case Single:
		return "Single"
	case Double:
		return "Double"
	case Triple:
		return "Triple"
	case Homer:
		return "Home Run"
	default:
		return "Hit"
	}
}

func (k Kind) Bases() int {
	if k < Single || k > Homer {
		return 1
	}
	return int(k)
}

// FieldingPlay is true for extra-base hits the defense can try to turn into an out.
// Home runs are not playable.
func (k Kind) FieldingPlay() bool {
	return k == Double || k == Triple
}

// Question is one line of BIBLE.QUS.
type Question struct {
	ID      int  // index in the bank
	Canon   int  // 1=Genesis … 66=Revelation
	Kind    Kind // 1–4
	Correct int  // 0–3
	Ref     string
	Text    string
	Choices [4]string
}

func (q Question) Testament() string {
	if q.Canon >= 40 {
		return "NT"
	}
	return "OT"
}

// Key is a stable identity across runs (IDs shift if the question file changes).
func (q Question) Key() string {
	return strings.TrimSpace(q.Text)
}

// IDsForKeys maps remembered question keys onto the current bank.
func (b *Bank) IDsForKeys(keys map[string]bool) map[int]bool {
	out := map[int]bool{}
	if b == nil || keys == nil {
		return out
	}
	for _, q := range b.All {
		if keys[q.Key()] {
			out[q.ID] = true
		}
	}
	return out
}

// Bank holds the question file.
type Bank struct {
	All []Question
}

func Parse(r io.Reader) (*Bank, error) {
	cr := csv.NewReader(r)
	cr.FieldsPerRecord = -1
	cr.LazyQuotes = true
	var all []Question
	line := 0
	for {
		rec, err := cr.Read()
		if err == io.EOF {
			break
		}
		line++
		if err != nil {
			return nil, fmt.Errorf("question file line %d: %w", line, err)
		}
		if len(rec) == 0 || (len(rec) == 1 && strings.TrimSpace(rec[0]) == "") {
			continue
		}
		if len(rec) != 9 {
			return nil, fmt.Errorf("question file line %d: want 9 fields, got %d", line, len(rec))
		}
		q, err := parseRec(rec, len(all))
		if err != nil {
			return nil, fmt.Errorf("question file line %d: %w", line, err)
		}
		all = append(all, q)
	}
	if len(all) == 0 {
		return nil, fmt.Errorf("question file is empty")
	}
	return &Bank{All: all}, nil
}

func parseRec(rec []string, id int) (Question, error) {
	canonS := strings.TrimSpace(rec[0])
	canonS = strings.TrimPrefix(strings.ToUpper(canonS), "C")
	canon, err := strconv.Atoi(canonS)
	if err != nil || canon < 1 || canon > 66 {
		return Question{}, fmt.Errorf("bad canonical number %q", rec[0])
	}
	kindN, err := strconv.Atoi(strings.TrimSpace(rec[1]))
	if err != nil || kindN < 1 || kindN > 4 {
		return Question{}, fmt.Errorf("invalid type of question %q", rec[1])
	}
	letter := strings.ToUpper(strings.TrimSpace(rec[2]))
	if len(letter) != 1 || letter[0] < 'A' || letter[0] > 'D' {
		return Question{}, fmt.Errorf("invalid correct answer %q", rec[2])
	}
	ref := strings.TrimSpace(rec[3])
	text := strings.TrimSpace(rec[4])
	if ref == "" {
		return Question{}, fmt.Errorf("invalid biblical reference")
	}
	if text == "" {
		return Question{}, fmt.Errorf("invalid question text")
	}
	var choices [4]string
	for i := 0; i < 4; i++ {
		choices[i] = strings.TrimSpace(rec[5+i])
		if choices[i] == "" {
			return Question{}, fmt.Errorf("invalid multiple choice answer")
		}
	}
	return Question{
		ID:      id,
		Canon:   canon,
		Kind:    Kind(kindN),
		Correct: int(letter[0] - 'A'),
		Ref:     ref,
		Text:    text,
		Choices: choices,
	}, nil
}

// Pick returns a random question of the given kind, preferring unused ones.
// ot/nt filter by testament; if both or neither are set, all books are used.
func (b *Bank) Pick(kind Kind, ot, nt bool, used map[int]bool) (Question, bool) {
	if !ot && !nt {
		ot, nt = true, true
	}
	if ot && nt {
		// all
	}
	pick := func(unusedOnly bool) (Question, bool) {
		var cand []Question
		for _, q := range b.All {
			if q.Kind != kind {
				continue
			}
			if q.Canon <= 39 && !ot {
				continue
			}
			if q.Canon >= 40 && !nt {
				continue
			}
			if unusedOnly && used[q.ID] {
				continue
			}
			cand = append(cand, q)
		}
		if len(cand) == 0 {
			return Question{}, false
		}
		return cand[rand.IntN(len(cand))], true
	}
	if q, ok := pick(true); ok {
		return q, true
	}
	// Original: once every question of this type is answered, they come back.
	return pick(false)
}
