package ignore

import (
	"bufio"
	"os"
	"path/filepath"
	"strings"

	gitignore "git.sr.ht/~jamesponddotco/gitignore-go"
)

type Matcher struct {
	baseDir string
	rules   *gitignore.File
}

func NewMatcher(baseDir string) (*Matcher, error) {
	lines := make([]string, 0, 512)
	lines = append(lines, DefaultIgnorePatterns...)

	err := filepath.WalkDir(baseDir, func(path string, d os.DirEntry, walkErr error) error {
		if walkErr != nil {
			return nil
		}
		if d == nil || d.IsDir() || d.Name() != ".gitignore" {
			return nil
		}

		f, err := os.Open(path)
		if err != nil {
			return nil
		}
		defer f.Close()

		scanner := bufio.NewScanner(f)
		for scanner.Scan() {
			line := strings.TrimSpace(scanner.Text())
			if line == "" || strings.HasPrefix(line, "#") {
				continue
			}
			// Legacy nie filtruje linii zaczynających się od "!" w get_gitignore_spec(),
			// więc tutaj też ich nie odrzucamy.
			lines = append(lines, line)
		}

		return nil
	})
	if err != nil {
		return nil, err
	}

	rules, err := gitignore.NewFromLines(lines)
	if err != nil {
		return nil, err
	}

	return &Matcher{
		baseDir: baseDir,
		rules:   rules,
	}, nil
}

func (m *Matcher) ShouldIgnore(path string) bool {
	if m == nil || m.rules == nil {
		return false
	}

	rel, err := filepath.Rel(m.baseDir, path)
	if err != nil {
		return true
	}

	info, err := os.Stat(path)
	if err != nil {
		return true
	}

	if !info.IsDir() && info.Size() > MaxFileSize {
		return true
	}

	rel = filepath.ToSlash(rel)
	return m.rules.Match(rel)
}
