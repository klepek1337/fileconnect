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
	w := a.NewWindow("Merge text files")
	w.Resize(fyne.NewSize(420, 220))

	title := widget.NewLabel("Select operation mode")
	title.Alignment = fyne.TextAlignCenter

	info := widget.NewLabel("1 - Merge files\n2 - Generate folder structure\n3 - Merge files and folder structure")
	info.Alignment = fyne.TextAlignCenter

	btn1 := widget.NewButton("1 - Merge files", func() {
		runMode1(w)
	})

	btn2 := widget.NewButton("2 - Generate folder structure", func() {
		runMode2(w)
	})

	btn3 := widget.NewButton("3 - Merge files and folder structure", func() {
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
			showError(w, fmt.Sprintf("A problem occurred while selecting files: %v", err))
			return
		}
		if reader == nil {
			showInfo(w, "No files selected.")
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
				showError(w, fmt.Sprintf("A problem occurred while selecting the output file: %v", err))
				return
			}
			if writer == nil {
				showInfo(w, "No output file selected.")
				return
			}

			output := writer.URI().Path()
			_ = writer.Close()

			if err := merger.MergeSelectedFiles(filePaths, output); err != nil {
				showError(w, fmt.Sprintf("A problem occurred while merging files: %v", err))
				return
			}

			showInfo(w, fmt.Sprintf("Files merged to: %s", output))
		}, w)

		save.SetFileName("output.txt")
		save.Show()
	})

	open.Show()
}

func runMode2(w fyne.Window) {
	folder := dialog.NewFolderOpen(func(uri fyne.ListableURI, err error) {
		if err != nil {
			showError(w, fmt.Sprintf("A problem occurred while selecting the folder: %v", err))
			return
		}
		if uri == nil {
			showInfo(w, "No folder selected.")
			return
		}

		folderPath := uri.Path()

		save := dialog.NewFileSave(func(writer fyne.URIWriteCloser, err error) {
			if err != nil {
				showError(w, fmt.Sprintf("A problem occurred while selecting the output file: %v", err))
				return
			}
			if writer == nil {
				showInfo(w, "No output file selected.")
				return
			}

			output := writer.URI().Path()
			_ = writer.Close()

			if !strings.HasSuffix(strings.ToLower(output), ".txt") {
				output += ".txt"
			}

			if err := merger.GenerateTreeOnly(folderPath, output); err != nil {
				showError(w, fmt.Sprintf("A problem occurred while generating the folder structure: %v", err))
				return
			}

			showInfo(w, fmt.Sprintf("Folder structure saved to: %s", output))
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
			showError(w, fmt.Sprintf("A problem occurred while selecting the folder: %v", err))
			return
		}
		if uri == nil {
			showInfo(w, "No folder selected.")
			return
		}

		folderPath := uri.Path()

		save := dialog.NewFileSave(func(writer fyne.URIWriteCloser, err error) {
			if err != nil {
				showError(w, fmt.Sprintf("A problem occurred while selecting the output file: %v", err))
				return
			}
			if writer == nil {
				showInfo(w, "No output file selected.")
				return
			}

			output := writer.URI().Path()
			_ = writer.Close()

			if !strings.HasSuffix(strings.ToLower(output), ".txt") {
				output += ".txt"
			}

			if err := merger.GenerateTreeAndContents(folderPath, output); err != nil {
				showError(w, fmt.Sprintf("A problem occurred while processing the folder: %v", err))
				return
			}

			showInfo(w, fmt.Sprintf("Folder structure and file contents saved to: %s", output))
		}, w)

		save.SetFileName("output.txt")
		save.SetFilter(storage.NewExtensionFileFilter([]string{".txt"}))
		save.Show()
	}, w)

	folder.Show()
}

func showInfo(w fyne.Window, message string) {
	dialog.ShowInformation("Success", message, w)
}

func showError(w fyne.Window, message string) {
	dialog.ShowError(fmt.Errorf(message), w)
}
