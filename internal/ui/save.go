package ui

import (
	"encoding/json"
	"os"
	"path/filepath"

	"github.com/caleb-parrot/winbb/internal/diamond"
)

func stateDir() string {
	if d := os.Getenv("XDG_STATE_HOME"); d != "" {
		return filepath.Join(d, "winbb")
	}
	home, err := os.UserHomeDir()
	if err != nil {
		return "."
	}
	return filepath.Join(home, ".local", "state", "winbb")
}

func savePath() string { return filepath.Join(stateDir(), "games.json") }

func loadSaves() []diamond.Snapshot {
	b, err := os.ReadFile(savePath())
	if err != nil {
		return nil
	}
	var games []diamond.Snapshot
	if json.Unmarshal(b, &games) != nil {
		return nil
	}
	return games
}

func writeSaves(games []diamond.Snapshot) error {
	if err := os.MkdirAll(stateDir(), 0o755); err != nil {
		return err
	}
	b, err := json.MarshalIndent(games, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(savePath(), b, 0o644)
}

func appendSave(s diamond.Snapshot) error {
	games := loadSaves()
	games = append([]diamond.Snapshot{s}, games...)
	if len(games) > 20 {
		games = games[:20]
	}
	return writeSaves(games)
}

func deleteSave(i int) error {
	games := loadSaves()
	if i < 0 || i >= len(games) {
		return nil
	}
	games = append(games[:i], games[i+1:]...)
	return writeSaves(games)
}

func askedPath() string { return filepath.Join(stateDir(), "asked.json") }

func loadAsked() map[string]bool {
	b, err := os.ReadFile(askedPath())
	if err != nil {
		return map[string]bool{}
	}
	var keys []string
	if json.Unmarshal(b, &keys) != nil {
		return map[string]bool{}
	}
	out := make(map[string]bool, len(keys))
	for _, k := range keys {
		if k != "" {
			out[k] = true
		}
	}
	return out
}

func writeAsked(keys map[string]bool) error {
	if err := os.MkdirAll(stateDir(), 0o755); err != nil {
		return err
	}
	list := make([]string, 0, len(keys))
	for k := range keys {
		if k != "" {
			list = append(list, k)
		}
	}
	b, err := json.MarshalIndent(list, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(askedPath(), b, 0o644)
}
