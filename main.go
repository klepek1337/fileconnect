package main

import (
	"bufio"
	"fileconnect/merger"
	"fmt"
	"os"
	"strings"

	"github.com/sqweek/dialog"
)

func main() {
	mode := askMode()
	if mode == "" {
		fmt.Println("Invalid mode.")
		return
	}

	switch mode {
	case "1":
		runMode1()
	case "2":
		runMode2()
	case "3":
		runMode3()
	}
}

func askMode() string {
	reader := bufio.NewReader(os.Stdin)

	fmt.Println("Select mode:")
	fmt.Println("1 - Merge files")
	fmt.Println("2 - Generate folder structure")
	fmt.Println("3 - Merge files and folder structure")
	fmt.Print("> ")

	mode, _ := reader.ReadString('\n')
	mode = strings.TrimSpace(mode)

	switch mode {
	case "1", "2", "3":
		return mode
	default:
		return ""
	}
}

func runMode1() {
	reader := bufio.NewReader(os.Stdin)
	files := make([]string, 0)

	for {
		file, err := dialog.File().
			Title("Select file to merge").
			Filter("Text files", "txt").
			Filter("Python files", "py").
			Filter("All files", "*").
			Load()

		if err != nil || file == "" {
			break
		}

		files = append(files, file)

		fmt.Print("Add another file? (y/n): ")
		answer, _ := reader.ReadString('\n')
		answer = strings.TrimSpace(strings.ToLower(answer))

		if answer != "y" {
			break
		}
	}

	if len(files) == 0 {
		fmt.Println("No files selected.")
		return
	}

	output, err := dialog.File().
		Title("Enter output filename").
		Filter("Text files", "txt").
		Filter("Python files", "py").
		Filter("All files", "*").
		Save()

	if err != nil || output == "" {
		fmt.Println("No output file selected.")
		return
	}

	if err := merger.MergeSelectedFiles(files, output); err != nil {
		fmt.Println("Error:", err)
		return
	}

	fmt.Println("Files merged to:", output)
}

func runMode2() {
	folder, err := dialog.Directory().
		Title("Select folder to analyze").
		Browse()

	if err != nil || folder == "" {
		fmt.Println("No folder selected.")
		return
	}

	output, err := dialog.File().
		Title("Enter output filename").
		Filter("Text files", "txt").
		Save()

	if err != nil || output == "" {
		fmt.Println("No output file selected.")
		return
	}

	if !hasTxtExtension(output) {
		output += ".txt"
	}

	if err := merger.GenerateTreeOnly(folder, output); err != nil {
		fmt.Println("Error:", err)
		return
	}

	fmt.Println("Folder structure saved to:", output)
}

func runMode3() {
	folder, err := dialog.Directory().
		Title("Select folder to analyze").
		Browse()

	if err != nil || folder == "" {
		fmt.Println("No folder selected.")
		return
	}

	output, err := dialog.File().
		Title("Enter output filename").
		Filter("Text files", "txt").
		Save()

	if err != nil || output == "" {
		fmt.Println("No output file selected.")
		return
	}

	if !hasTxtExtension(output) {
		output += ".txt"
	}

	if err := merger.GenerateTreeAndContents(folder, output); err != nil {
		fmt.Println("Error:", err)
		return
	}

	fmt.Println("Folder structure and file contents saved to:", output)
}

func hasTxtExtension(path string) bool {
	return strings.HasSuffix(strings.ToLower(path), ".txt")
}
