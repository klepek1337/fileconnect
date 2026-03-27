package tree

import (
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sort"

	"fileconnect/ignore"
)

func WriteFolderStructure(w io.Writer, folderPath string, matcher *ignore.Matcher) error {
	_, err := fmt.Fprintf(w, "### Folder structure: %s ###\n\n", filepath.Base(folderPath))
	if err != nil {
		return err
	}

	var writeStructure func(string, string) error
	writeStructure = func(path string, prefix string) error {
		if matcher != nil && matcher.ShouldIgnore(path) {
			return nil
		}

		info, err := os.Stat(path)
		if err != nil {
			return nil
		}

		if !info.IsDir() {
			_, err = fmt.Fprintf(w, "%s├── %s\n", prefix, filepath.Base(path))
			return err
		}

		if prefix != "" {
			_, err = fmt.Fprintf(w, "%s└── %s/\n", prefix, filepath.Base(path))
			if err != nil {
				return err
			}
		}

		prefix += "    "

		items, err := os.ReadDir(path)
		if err != nil {
			return nil
		}

		sort.Slice(items, func(i, j int) bool { return items[i].Name() < items[j].Name() })

		visible := make([]os.DirEntry, 0, len(items))
		for _, item := range items {
			itemPath := filepath.Join(path, item.Name())
			if matcher != nil && matcher.ShouldIgnore(itemPath) {
				continue
			}
			visible = append(visible, item)
		}

		for i, item := range visible {
			itemPath := filepath.Join(path, item.Name())
			isLast := i == len(visible)-1

			currentPrefix := prefix[:len(prefix)-4]
			if isLast {
				currentPrefix += "└── "
			} else {
				currentPrefix += "├── "
			}

			if item.IsDir() {
				if err := writeStructure(itemPath, prefix+"    "); err != nil {
					return err
				}
			} else {
				_, err := fmt.Fprintf(w, "%s%s\n", currentPrefix, item.Name())
				if err != nil {
					return err
				}
			}
		}

		return nil
	}

	return writeStructure(folderPath, "")
}

func GetAllFiles(folderPath string, matcher *ignore.Matcher) ([]string, error) {
	allFiles := make([]string, 0)

	err := filepath.WalkDir(folderPath, func(path string, d os.DirEntry, walkErr error) error {
		if walkErr != nil {
			return nil
		}

		if path == folderPath {
			return nil
		}

		if matcher != nil && matcher.ShouldIgnore(path) {
			if d != nil && d.IsDir() {
				return filepath.SkipDir
			}
			return nil
		}

		if d != nil && !d.IsDir() {
			allFiles = append(allFiles, path)
		}

		return nil
	})

	return allFiles, err
}
