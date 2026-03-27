package ignore

const MaxFileSize int64 = 1024 * 1024

var DefaultIgnorePatterns = []string{
	"node_modules/", "npm-debug.log", "yarn-debug.log", "yarn-error.log", ".npm/", ".yarn/", "package-lock.json", "yarn.lock",
	"__pycache__/", "*.pyc", "*.pyo", "*.pyd", "*.so", "*.egg", "*.egg-info/", "dist/", "build/", "*.egg-info/", "*.egg", "*.manifest", "*.spec", "pip-log.txt", "pip-delete-this-directory.txt", "htmlcov/", ".tox/", ".nox/", ".coverage", ".coverage.*", "coverage.xml", "*.cover", "*.py,cover", ".hypothesis/", ".pytest_cache/", "cover/", "*.mo", "*.pot", "*.log", "local_settings.py", "db.sqlite3", "instance/", ".webassets-cache", ".env", ".venv", "env/", "venv/", "ENV/", "env.bak/", "venv.bak/",
	".idea/", ".vscode/", "*.swp", "*.swo", "*~", "*.sublime-workspace", "*.sublime-project", ".project", ".classpath", ".settings/", "*.tmproj", "*.esproj", "nbproject/", "*.sublime-project", "*.sublime-workspace", ".vs/", "*.suo", "*.ntvs*", "*.njsproj", "*.sln", "*.sw?", "*.bak", "*.orig", "*.rej", "*.tmp", "*.temp", "*.log", "*.pid", "*.seed", "*.pid.lock",
	".DS_Store", ".DS_Store?", "._*", ".Spotlight-V100", ".Trashes", "ehthumbs.db", "Thumbs.db",
	"*.7z", "*.dmg", "*.gz", "*.iso", "*.jar", "*.rar", "*.tar", "*.zip", "*.tar.gz", "*.tar.bz2", "*.tar.xz", "*.tgz", "*.tbz2", "*.txz", "*.zip", "*.rar", "*.7z", "*.iso", "*.img", "*.vmdk", "*.vhd", "*.vhdx", "*.vdi", "*.qcow2", "*.raw", "*.dmg", "*.sparseimage", "*.sparsebundle", "*.hfs", "*.hfsx", "*.udf",
	"*.sqlite", "*.sqlite3", "*.db", "*.db-journal", "*.db-shm", "*.db-wal",
	"*.exe", "*.dll", "*.so", "*.dylib", "*.bin", "*.dat", "*.lock", "*.lck", "*.part", "*.partial", "*.temp", "*.tmp", "*.bak", "*.swp", "*.swo", "*.orig", "*.rej", "*.old", "*.new", "*.diff", "*.patch", "*.log",
	".git/", ".gitignore", ".gitattributes", ".gitmodules", ".gitkeep", ".gitattributes", ".gitmodules", ".gitkeep",
	"*.log", "*.tmp", "*.temp", "*.swp", "*.swo", "*.bak", "*.cache", "*.pid", "*.pid.lock", "*.lock", "*.lck", "*.part", "*.partial", "*.temp", "*.tmp", "*.bak", "*.swp", "*.swo", "*.orig", "*.rej", "*.old", "*.new", "*.diff", "*.patch", "*.log",
}
