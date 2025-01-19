# About

## Development

- Required to run Fyne on linux:
`sudo apt-get install libxcursor-dev libxrandr-dev libxinerama-dev libxi-dev libgl1-mesa-dev xorg-dev`

- if you get an error like this after running `go run main.go`,
```bash
# go run main.go
2025/01/19 13:45:19 Fyne error:  Error parsing user locale C
2025/01/19 13:45:19   Cause: language: tag is not well-formed
2025/01/19 13:45:19   At: /home/brian/go/pkg/mod/fyne.io/fyne/v2@v2.5.3/lang/locale.go:35
```

Set your local language, which in my case is English.
To fix this, you can:
Set a proper locale environment variable before running your application. For example:
```bash
export LANG=en_US.UTF-8
go run main.go
```
Then it should run fine.