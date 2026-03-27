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
		fmt.Println("Nieprawidłowy tryb działania.")
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

	fmt.Println("Wybierz tryb:")
	fmt.Println("1 - Łączenie plików")
	fmt.Println("2 - Generowanie struktury folderu")
	fmt.Println("3 - Łączenie plików i struktura folderu")
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
			Title("Wybierz plik do połączenia").
			Filter("Pliki tekstowe", "txt").
			Filter("Pliki Python", "py").
			Filter("Wszystkie pliki", "*").
			Load()

		if err != nil || file == "" {
			break
		}

		files = append(files, file)

		fmt.Print("Dodać kolejny plik? (t/n): ")
		answer, _ := reader.ReadString('\n')
		answer = strings.TrimSpace(strings.ToLower(answer))

		if answer != "t" {
			break
		}
	}

	if len(files) == 0 {
		fmt.Println("Nie wybrano żadnych plików.")
		return
	}

	output, err := dialog.File().
		Title("Podaj nazwę pliku wynikowego").
		Filter("Pliki tekstowe", "txt").
		Filter("Pliki Python", "py").
		Filter("Wszystkie pliki", "*").
		Save()

	if err != nil || output == "" {
		fmt.Println("Nie wybrano pliku wynikowego.")
		return
	}

	if err := merger.MergeSelectedFiles(files, output); err != nil {
		fmt.Println("Błąd:", err)
		return
	}

	fmt.Println("Pliki zostały połączone do:", output)
}

func runMode2() {
	folder, err := dialog.Directory().
		Title("Wybierz folder do analizy").
		Browse()

	if err != nil || folder == "" {
		fmt.Println("Nie wybrano folderu.")
		return
	}

	output, err := dialog.File().
		Title("Podaj nazwę pliku wynikowego").
		Filter("Pliki tekstowe", "txt").
		Save()

	if err != nil || output == "" {
		fmt.Println("Nie wybrano pliku wynikowego.")
		return
	}

	if !hasTxtExtension(output) {
		output += ".txt"
	}

	if err := merger.GenerateTreeOnly(folder, output); err != nil {
		fmt.Println("Błąd:", err)
		return
	}

	fmt.Println("Struktura folderu została zapisana do:", output)
}

func runMode3() {
	folder, err := dialog.Directory().
		Title("Wybierz folder do analizy").
		Browse()

	if err != nil || folder == "" {
		fmt.Println("Nie wybrano folderu.")
		return
	}

	output, err := dialog.File().
		Title("Podaj nazwę pliku wynikowego").
		Filter("Pliki tekstowe", "txt").
		Save()

	if err != nil || output == "" {
		fmt.Println("Nie wybrano pliku wynikowego.")
		return
	}

	if !hasTxtExtension(output) {
		output += ".txt"
	}

	if err := merger.GenerateTreeAndContents(folder, output); err != nil {
		fmt.Println("Błąd:", err)
		return
	}

	fmt.Println("Struktura folderu i zawartość plików zostały zapisane do:", output)
}

func hasTxtExtension(path string) bool {
	return strings.HasSuffix(strings.ToLower(path), ".txt")
}
