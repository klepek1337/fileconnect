package ui

import (
	"fileconnect/merger"
	"fmt"
	"strings"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/storage"
	"fyne.io/fyne/v2/widget"
)

func Run() {
	a := app.New()
	w := a.NewWindow("Łączenie plików tekstowych")
	w.Resize(fyne.NewSize(420, 220))

	title := widget.NewLabel("Wybierz tryb działania")
	title.Alignment = fyne.TextAlignCenter

	info := widget.NewLabel("1 - Łączenie plików\n2 - Generowanie struktury folderu\n3 - Łączenie plików i struktura folderu")
	info.Alignment = fyne.TextAlignCenter

	btn1 := widget.NewButton("1 - Łączenie plików", func() {
		runMode1(w)
	})

	btn2 := widget.NewButton("2 - Generowanie struktury folderu", func() {
		runMode2(w)
	})

	btn3 := widget.NewButton("3 - Łączenie plików i struktura folderu", func() {
		runMode3(w)
	})

	w.SetContent(container.NewVBox(
		title,
		info,
		btn1,
		btn2,
		btn3,
	))

	w.ShowAndRun()
}

func runMode1(w fyne.Window) {
	open := dialog.NewFileOpen(func(reader fyne.URIReadCloser, err error) {
		if err != nil {
			showError(w, fmt.Sprintf("Wystąpił problem podczas wyboru plików: %v", err))
			return
		}
		if reader == nil {
			showInfo(w, "Nie wybrano żadnych plików.")
			return
		}
	}, w)

	open.SetMultiSelection(true)

	filter := storage.NewExtensionFileFilter([]string{".txt", ".py"})
	open.SetFilter(filter)

	open.SetOnClosed(func() {
		uris := open.Selected()
		if len(uris) == 0 {
			return
		}

		filePaths := make([]string, 0, len(uris))
		for _, u := range uris {
			filePaths = append(filePaths, u.Path())
		}

		save := dialog.NewFileSave(func(writer fyne.URIWriteCloser, err error) {
			if err != nil {
				showError(w, fmt.Sprintf("Wystąpił problem podczas wyboru pliku wynikowego: %v", err))
				return
			}
			if writer == nil {
				showInfo(w, "Nie wybrano pliku wynikowego.")
				return
			}

			output := writer.URI().Path()
			_ = writer.Close()

			if err := merger.MergeSelectedFiles(filePaths, output); err != nil {
				showError(w, fmt.Sprintf("Wystąpił problem podczas łączenia plików: %v", err))
				return
			}

			showInfo(w, fmt.Sprintf("Pliki zostały połączone do: %s", output))
		}, w)

		save.SetFileName("output.txt")
		save.Show()
	})

	open.Show()
}

func runMode2(w fyne.Window) {
	folder := dialog.NewFolderOpen(func(uri fyne.ListableURI, err error) {
		if err != nil {
			showError(w, fmt.Sprintf("Wystąpił problem podczas wyboru folderu: %v", err))
			return
		}
		if uri == nil {
			showInfo(w, "Nie wybrano folderu.")
			return
		}

		folderPath := uri.Path()

		save := dialog.NewFileSave(func(writer fyne.URIWriteCloser, err error) {
			if err != nil {
				showError(w, fmt.Sprintf("Wystąpił problem podczas wyboru pliku wynikowego: %v", err))
				return
			}
			if writer == nil {
				showInfo(w, "Nie wybrano pliku wynikowego.")
				return
			}

			output := writer.URI().Path()
			_ = writer.Close()

			if !strings.HasSuffix(strings.ToLower(output), ".txt") {
				output += ".txt"
			}

			if err := merger.GenerateTreeOnly(folderPath, output); err != nil {
				showError(w, fmt.Sprintf("Wystąpił problem podczas generowania struktury folderu: %v", err))
				return
			}

			showInfo(w, fmt.Sprintf("Struktura folderu została zapisana do: %s", output))
		}, w)

		save.SetFileName("output.txt")
		save.SetFilter(storage.NewExtensionFileFilter([]string{".txt"}))
		save.Show()
	}, w)

	folder.Show()
}

func runMode3(w fyne.Window) {
	folder := dialog.NewFolderOpen(func(uri fyne.ListableURI, err error) {
		if err != nil {
			showError(w, fmt.Sprintf("Wystąpił problem podczas wyboru folderu: %v", err))
			return
		}
		if uri == nil {
			showInfo(w, "Nie wybrano folderu.")
			return
		}

		folderPath := uri.Path()

		save := dialog.NewFileSave(func(writer fyne.URIWriteCloser, err error) {
			if err != nil {
				showError(w, fmt.Sprintf("Wystąpił problem podczas wyboru pliku wynikowego: %v", err))
				return
			}
			if writer == nil {
				showInfo(w, "Nie wybrano pliku wynikowego.")
				return
			}

			output := writer.URI().Path()
			_ = writer.Close()

			if !strings.HasSuffix(strings.ToLower(output), ".txt") {
				output += ".txt"
			}

			if err := merger.GenerateTreeAndContents(folderPath, output); err != nil {
				showError(w, fmt.Sprintf("Wystąpił problem podczas przetwarzania folderu: %v", err))
				return
			}

			showInfo(w, fmt.Sprintf("Struktura folderu i zawartość plików zostały zapisane do: %s", output))
		}, w)

		save.SetFileName("output.txt")
		save.SetFilter(storage.NewExtensionFileFilter([]string{".txt"}))
		save.Show()
	}, w)

	folder.Show()
}

func showInfo(w fyne.Window, message string) {
	dialog.ShowInformation("Sukces", message, w)
}

func showError(w fyne.Window, message string) {
	dialog.ShowError(fmt.Errorf(message), w)
}
