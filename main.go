package main

import (
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func main() {
	myApp := app.New()
	myWindow := myApp.NewWindow("Hello")

	label := widget.NewLabel("Hello, Fyne!")
	button := widget.NewButton("Click Me", func() {
		label.SetText("You clicked!")
	})

	myWindow.SetContent(container.NewVBox(
		label,
		button,
	))

	myWindow.ShowAndRun()
}
