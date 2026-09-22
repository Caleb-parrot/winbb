package ui

import (
	"bytes"
	"io"

	"github.com/caleb-parrot/winbb/assets"
	"github.com/hajimehoshi/ebiten/v2/audio"
	"github.com/hajimehoshi/ebiten/v2/audio/wav"
)

type sounds struct {
	ctx                    *audio.Context
	playBall, cheer, groan *audio.Player
	enabled                bool
}

func loadSounds() *sounds {
	s := &sounds{enabled: true}
	s.ctx = audio.NewContext(44100)
	s.playBall = decodeWAV(s.ctx, "bb0.wav") // "Play Ball"
	s.cheer = decodeWAV(s.ctx, "bb1.wav")    // crowd cheer on a hit
	s.groan = decodeWAV(s.ctx, "bb2.wav")    // disappointed aww on an out
	return s
}

func decodeWAV(ctx *audio.Context, name string) *audio.Player {
	b, err := assets.FS.ReadFile(name)
	if err != nil {
		return nil
	}
	stream, err := wav.DecodeWithSampleRate(44100, bytes.NewReader(b))
	if err != nil {
		return nil
	}
	data, err := io.ReadAll(stream)
	if err != nil {
		return nil
	}
	return ctx.NewPlayerFromBytes(data)
}

func (s *sounds) play(p *audio.Player) {
	if s == nil || !s.enabled || p == nil {
		return
	}
	_ = p.Rewind()
	p.Play()
}

func (s *sounds) PlayBall() { s.play(s.playBall) }
func (s *sounds) Cheer()    { s.play(s.cheer) }
func (s *sounds) Groan()    { s.play(s.groan) }
