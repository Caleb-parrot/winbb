package main

import (
	"fmt"
	"os"

	"github.com/caleb-parrot/winbb/internal/ui"
	"github.com/hajimehoshi/ebiten/v2"
)

func main() {
	app, err := ui.New()
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	ebiten.SetWindowTitle("Bible Baseball")
	ebiten.SetWindowResizingMode(ebiten.WindowResizingModeEnabled)
	ebiten.SetWindowSize(990, 766)
	if err := ebiten.RunGame(app); err != nil && err != ebiten.Termination {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
