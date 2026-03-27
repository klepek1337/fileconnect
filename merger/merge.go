package merger

import (
	"fileconnect/ignore"
	"fileconnect/tree"
	"fmt"
	"os"
	"path/filepath"
	"unicode/utf8"
)

func MergeSelectedFiles(filePaths []string, outputFile string) error {
	out, err := os.Create(outputFile)
	if err != nil {
		return err
	}
	defer out.Close()

	for _, filePath := range filePaths {
		text, err := readUTF8TextFile(filePath)
		if err != nil {
			_, _ = fmt.Fprintf(out, "### Nie można odczytać pliku: %s - %v ###\n\n", filepath.Base(filePath), err)
			continue
		}

		_, err = fmt.Fprintf(out, "### Zawartość pliku: %s ###\n", filepath.Base(filePath))
		if err != nil {
			return err
		}

		_, err = out.WriteString(text)
		if err != nil {
			return err
		}

		_, err = out.WriteString("\n\n")
		if err != nil {
			return err
		}
	}

	return nil
}

func GenerateTreeOnly(folderPath string, outputFile string) error {
	out, err := os.Create(outputFile)
	if err != nil {
		return err
	}
	defer out.Close()

	matcher, err := ignore.NewMatcher(folderPath)
	if err != nil {
		return err
	}

	return tree.WriteFolderStructure(out, folderPath, matcher)
}

func GenerateTreeAndContents(folderPath string, outputFile string) error {
	out, err := os.Create(outputFile)
	if err != nil {
		return err
	}
	defer out.Close()

	matcher, err := ignore.NewMatcher(folderPath)
	if err != nil {
		return err
	}

	if err := tree.WriteFolderStructure(out, folderPath, matcher); err != nil {
		return err
	}

	if _, err := out.WriteString("\n\n### ZAWARTOŚĆ PLIKÓW ###\n\n"); err != nil {
		return err
	}

	allFiles, err := tree.GetAllFiles(folderPath, matcher)
	if err != nil {
		return err
	}

	for _, filePath := range allFiles {
		relPath, relErr := filepath.Rel(folderPath, filePath)
		if relErr != nil {
			relPath = filePath
		}

		text, err := readUTF8TextFile(filePath)
		if err != nil {
			_, _ = fmt.Fprintf(out, "### Nie można odczytać pliku: %s - %v ###\n\n", relPath, err)
			continue
		}

		_, err = fmt.Fprintf(out, "### Zawartość pliku: %s ###\n", relPath)
		if err != nil {
			return err
		}

		_, err = out.WriteString(text)
		if err != nil {
			return err
		}

		_, err = out.WriteString("\n\n")
		if err != nil {
			return err
		}
	}

	return nil
}

func readUTF8TextFile(path string) (string, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return "", err
	}

	if !utf8.Valid(data) {
		return "", fmt.Errorf("plik nie jest poprawnym UTF-8")
	}

	return string(data), nil
}
