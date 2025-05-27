import os
import fnmatch
from tkinter import Tk, filedialog, simpledialog, messagebox
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

# Maximum file size to include (in bytes) - 1MB
MAX_FILE_SIZE = 1024 * 1024

# Default patterns to ignore
DEFAULT_IGNORE_PATTERNS = [
    # Node.js
    'node_modules/',
    'npm-debug.log',
    'yarn-debug.log',
    'yarn-error.log',
    '.npm/',
    '.yarn/',
    'package-lock.json',
    'yarn.lock',
    
    # Python
    '__pycache__/',
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '*.so',
    '*.egg',
    '*.egg-info/',
    'dist/',
    'build/',
    '*.egg-info/',
    '*.egg',
    '*.manifest',
    '*.spec',
    'pip-log.txt',
    'pip-delete-this-directory.txt',
    'htmlcov/',
    '.tox/',
    '.nox/',
    '.coverage',
    '.coverage.*',
    'coverage.xml',
    '*.cover',
    '*.py,cover',
    '.hypothesis/',
    '.pytest_cache/',
    'cover/',
    '*.mo',
    '*.pot',
    '*.log',
    'local_settings.py',
    'db.sqlite3',
    'instance/',
    '.webassets-cache',
    '.env',
    '.venv',
    'env/',
    'venv/',
    'ENV/',
    'env.bak/',
    'venv.bak/',
    
    # IDEs and editors
    '.idea/',
    '.vscode/',
    '*.swp',
    '*.swo',
    '*~',
    '*.sublime-workspace',
    '*.sublime-project',
    '.project',
    '.classpath',
    '.settings/',
    '*.tmproj',
    '*.esproj',
    'nbproject/',
    '*.sublime-project',
    '*.sublime-workspace',
    '.vs/',
    '*.suo',
    '*.ntvs*',
    '*.njsproj',
    '*.sln',
    '*.sw?',
    '*.bak',
    '*.orig',
    '*.rej',
    '*.tmp',
    '*.temp',
    '*.log',
    '*.pid',
    '*.seed',
    '*.pid.lock',
    
    # OS generated files
    '.DS_Store',
    '.DS_Store?',
    '._*',
    '.Spotlight-V100',
    '.Trashes',
    'ehthumbs.db',
    'Thumbs.db',
    
    # Build and package files
    '*.7z',
    '*.dmg',
    '*.gz',
    '*.iso',
    '*.jar',
    '*.rar',
    '*.tar',
    '*.zip',
    '*.tar.gz',
    '*.tar.bz2',
    '*.tar.xz',
    '*.tgz',
    '*.tbz2',
    '*.txz',
    '*.zip',
    '*.rar',
    '*.7z',
    '*.iso',
    '*.img',
    '*.vmdk',
    '*.vhd',
    '*.vhdx',
    '*.vdi',
    '*.qcow2',
    '*.raw',
    '*.dmg',
    '*.sparseimage',
    '*.sparsebundle',
    '*.hfs',
    '*.hfsx',
    '*.udf',
    
    # Database files
    '*.sqlite',
    '*.sqlite3',
    '*.db',
    '*.db-journal',
    '*.db-shm',
    '*.db-wal',
    
    # Binary files
    '*.exe',
    '*.dll',
    '*.so',
    '*.dylib',
    '*.bin',
    '*.dat',
    '*.pid',
    '*.pid.lock',
    '*.lock',
    '*.lck',
    '*.part',
    '*.partial',
    '*.temp',
    '*.tmp',
    '*.bak',
    '*.swp',
    '*.swo',
    '*.orig',
    '*.rej',
    '*.old',
    '*.new',
    '*.diff',
    '*.patch',
    '*.log',
    
    # Git
    '.git/',
    '.gitignore',
    '.gitattributes',
    '.gitmodules',
    '.gitkeep',
    '.gitattributes',
    '.gitmodules',
    '.gitkeep',
    
    # Other
    '*.log',
    '*.tmp',
    '*.temp',
    '*.swp',
    '*.swo',
    '*.bak',
    '*.cache',
    '*.pid',
    '*.pid.lock',
    '*.lock',
    '*.lck',
    '*.part',
    '*.partial',
    '*.temp',
    '*.tmp',
    '*.bak',
    '*.swp',
    '*.swo',
    '*.orig',
    '*.rej',
    '*.old',
    '*.new',
    '*.diff',
    '*.patch',
    '*.log',
]

def find_all_gitignores(folder_path):
    """Find all .gitignore files in the directory tree."""
    gitignore_files = []
    for root, _, files in os.walk(folder_path):
        if '.gitignore' in files:
            gitignore_files.append(os.path.join(root, '.gitignore'))
    return gitignore_files

def parse_gitignore(gitignore_path):
    """Parse .gitignore file and return a list of patterns."""
    patterns = []
    try:
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if line.startswith('!'):
                        continue
                    patterns.append(line)
    except FileNotFoundError:
        pass
    return patterns

def get_all_gitignore_patterns(folder_path):
    """Get all gitignore patterns from all .gitignore files in the directory tree."""
    patterns = set(DEFAULT_IGNORE_PATTERNS)  # Start with default patterns
    gitignore_files = find_all_gitignores(folder_path)
    
    for gitignore_file in gitignore_files:
        patterns.update(parse_gitignore(gitignore_file))
    
    return list(patterns)

def get_gitignore_spec(folder_path):
    """Get PathSpec object for all .gitignore patterns in the directory tree."""
    patterns = []
    
    # Add default patterns
    patterns.extend(DEFAULT_IGNORE_PATTERNS)
    
    # Find and read all .gitignore files
    for root, _, files in os.walk(folder_path):
        if '.gitignore' in files:
            gitignore_path = os.path.join(root, '.gitignore')
            try:
                with open(gitignore_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            patterns.append(line)
            except Exception:
                continue
    
    return PathSpec.from_lines(GitWildMatchPattern, patterns)

def should_ignore(path, gitignore_spec, base_path):
    """Check if a path should be ignored based on gitignore patterns."""
    if not gitignore_spec:
        return False
    
    # Get relative path from base_path
    try:
        rel_path = os.path.relpath(path, base_path).replace('\\', '/')
        
        # Check if file is too large
        if os.path.isfile(path):
            try:
                if os.path.getsize(path) > MAX_FILE_SIZE:
                    return True
            except Exception:
                return True
        
        return gitignore_spec.match_file(rel_path)
    except Exception:
        return True  # If there's any error, better to ignore the file

def generate_folder_structure(folder_path, output_file, prefix="", gitignore_spec=None):
    """Generate a tree-like structure of the folder and save it to a file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(f"### Struktura folderu: {os.path.basename(folder_path)} ###\n\n")
            
            def write_structure(path, prefix=""):
                if gitignore_spec and should_ignore(path, gitignore_spec, folder_path):
                    return
                
                if os.path.isfile(path):
                    outfile.write(f"{prefix}├── {os.path.basename(path)}\n")
                else:
                    if prefix != "":
                        outfile.write(f"{prefix}└── {os.path.basename(path)}/\n")
                    
                    prefix += "    "
                    
                    items = sorted(os.listdir(path))
                    for i, item in enumerate(items):
                        item_path = os.path.join(path, item)
                        if gitignore_spec and should_ignore(item_path, gitignore_spec, folder_path):
                            continue
                            
                        is_last = i == len(items) - 1
                        current_prefix = prefix[:-4] + ("└── " if is_last else "├── ")
                        
                        if os.path.isdir(item_path):
                            write_structure(item_path, prefix + "    ")
                        else:
                            outfile.write(f"{current_prefix}{item}\n")
            
            write_structure(folder_path)
            
        messagebox.showinfo("Sukces", f"Struktura folderu została zapisana do: {output_file}")
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił problem podczas generowania struktury folderu: {e}")

def get_all_files(folder_path, gitignore_spec=None):
    """Get all files from a folder and its subfolders, respecting gitignore patterns."""
    all_files = []
    for root, dirs, files in os.walk(folder_path, topdown=True):
        # Filter directories in-place to prevent os.walk from entering ignored ones
        if gitignore_spec:
            dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), gitignore_spec, folder_path)]
        
        for file in files:
            file_path = os.path.join(root, file)
            if not gitignore_spec or not should_ignore(file_path, gitignore_spec, folder_path):
                all_files.append(file_path)
    return all_files

def merge_files():
    # Tworzenie okna tkinter
    root = Tk()
    root.withdraw()  # Ukryj główne okno
    root.title("Łączenie plików tekstowych")

    # Wybierz tryb działania
    mode = simpledialog.askstring("Tryb", "Wybierz tryb:\n1 - Łączenie plików\n2 - Generowanie struktury folderu\n3 - Łączenie plików i struktura folderu")
    
    if mode == "1":
        # Wybierz pliki do połączenia
        # Note: Gitignore is not applied in this mode as specific files are selected manually
        file_paths = filedialog.askopenfilenames(
            title="Wybierz pliki do połączenia",
            filetypes=[("Pliki tekstowe", "*.txt"), ("Pliki Python", "*.py"), ("Wszystkie pliki", "*.*")]
        )
        
        if not file_paths:
            messagebox.showinfo("Brak plików", "Nie wybrano żadnych plików.")
            return

        # Podaj nazwę pliku wynikowego
        output_file = filedialog.asksaveasfilename(
            title="Podaj nazwę pliku wynikowego",
            defaultextension=".txt",
            filetypes=[("Pliki tekstowe", "*.txt"), ("Pliki Python", "*.py"), ("Wszystkie pliki", "*.*")]
        )
        
        if not output_file:
            messagebox.showinfo("Anulowano", "Nie wybrano pliku wynikowego.")
            return

        # Połączenie zawartości plików
        try:
            with open(output_file, 'w', encoding='utf-8') as outfile:
                for file_path in file_paths:
                    try:
                         with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(f"### Zawartość pliku: {os.path.basename(file_path)} ###\n")
                            outfile.write(infile.read())
                            outfile.write("\n\n")
                    except Exception as e:
                         outfile.write(f"### Nie można odczytać pliku: {os.path.basename(file_path)} - {e} ###\n\n")

            messagebox.showinfo("Sukces", f"Pliki zostały połączone do: {output_file}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił problem podczas łączenia plików: {e}")
    
    elif mode == "2":
        # Wybierz folder
        folder_path = filedialog.askdirectory(title="Wybierz folder do analizy")
        if not folder_path:
            messagebox.showinfo("Anulowano", "Nie wybrano folderu.")
            return

        # Podaj nazwę pliku wynikowego
        output_file = filedialog.asksaveasfilename(
            title="Podaj nazwę pliku wynikowego",
            defaultextension=".txt",
            filetypes=[("Pliki tekstowe", "*.txt")]
        )
        
        if not output_file:
            messagebox.showinfo("Anulowano", "Nie wybrano pliku wynikowego.")
            return

        # Get gitignore patterns
        gitignore_spec = get_gitignore_spec(folder_path)
        
        generate_folder_structure(folder_path, output_file, gitignore_spec=gitignore_spec)
    
    elif mode == "3":
        # Wybierz folder
        folder_path = filedialog.askdirectory(title="Wybierz folder do analizy")
        if not folder_path:
            messagebox.showinfo("Anulowano", "Nie wybrano folderu.")
            return

        # Podaj nazwę pliku wynikowego
        output_file = filedialog.asksaveasfilename(
            title="Podaj nazwę pliku wynikowego",
            defaultextension=".txt",
            filetypes=[("Pliki tekstowe", "*.txt")]
        )
        
        if not output_file:
            messagebox.showinfo("Anulowano", "Nie wybrano pliku wynikowego.")
            return

        try:
            # Get gitignore patterns
            gitignore_spec = get_gitignore_spec(folder_path)
            
            # Najpierw generujemy strukturę folderu
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(f"### Struktura folderu: {os.path.basename(folder_path)} ###\n\n")
                
                def write_structure(path, prefix=""):
                    if gitignore_spec and should_ignore(path, gitignore_spec, folder_path):
                        return
                    
                    if os.path.isfile(path):
                        outfile.write(f"{prefix}├── {os.path.basename(path)}\n")
                    else:
                        if prefix != "":
                            outfile.write(f"{prefix}└── {os.path.basename(path)}/\n")
                        
                        prefix += "    "
                        
                        items = sorted(os.listdir(path))
                        for i, item in enumerate(items):
                            item_path = os.path.join(path, item)
                            if gitignore_spec and should_ignore(item_path, gitignore_spec, folder_path):
                                continue
                                
                            is_last = i == len(items) - 1
                            current_prefix = prefix[:-4] + ("└── " if is_last else "├── ")
                            
                            if os.path.isdir(item_path):
                                write_structure(item_path, prefix + "    ")
                            else:
                                outfile.write(f"{current_prefix}{item}\n")
                
                write_structure(folder_path)
                
                # Następnie dodajemy zawartość plików
                outfile.write("\n\n### ZAWARTOŚĆ PLIKÓW ###\n\n")
                all_files = get_all_files(folder_path, gitignore_spec)
                for file_path in all_files:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(f"### Zawartość pliku: {os.path.relpath(file_path, folder_path)} ###\n")
                            outfile.write(infile.read())
                            outfile.write("\n\n")
                    except Exception as e:
                        outfile.write(f"### Nie można odczytać pliku: {os.path.relpath(file_path, folder_path)} - {e} ###\n\n")

            messagebox.showinfo("Sukces", f"Struktura folderu i zawartość plików zostały zapisane do: {output_file}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił problem podczas przetwarzania folderu: {e}")
    
    else:
        messagebox.showinfo("Błąd", "Nieprawidłowy tryb działania.")

if __name__ == "__main__":
    merge_files()
