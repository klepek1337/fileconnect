import os
import fnmatch
from tkinter import Tk, filedialog, simpledialog, messagebox

# Default patterns to ignore
DEFAULT_IGNORE_PATTERNS = [
    'node_modules/',
    '.git/',
    '__pycache__/',
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '.env',
    'venv/',
    '.venv/',
    'env/',
    '.idea/',
    '.vscode/',
    '*.log',
    '*.tmp',
    '*.temp',
    '*.swp',
    '*.swo',
    '*.bak',
    '*.cache',
    'dist/',
    'build/',
    '*.egg-info/',
    '*.egg',
    '*.so',
    '*.dll',
    '*.dylib',
    '*.exe',
    '*.bin',
    '*.dat',
    '*.db',
    '*.sqlite',
    '*.sqlite3',
    '*.db-journal',
    '*.db-shm',
    '*.db-wal',
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
    '*.gz',
    '*.zip',
    '*.tar',
    '*.rar',
    '*.7z',
    '*.bz2',
    '*.xz',
    '*.lzma',
    '*.tgz',
    '*.tbz2',
    '*.txz',
    '*.tlz',
    '*.tar.gz',
    '*.tar.bz2',
    '*.tar.xz',
    '*.tar.lzma',
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

def should_ignore(path, gitignore_patterns, base_path):
    """Check if a path should be ignored based on .gitignore patterns."""
    if not gitignore_patterns:
        return False
        
    rel_path = os.path.relpath(path, base_path).replace('\\', '/')
    is_dir = os.path.isdir(path)
    
    for pattern in gitignore_patterns:
        # Handle directory patterns
        if pattern.endswith('/'):
            if not is_dir:
                continue
            pattern = pattern[:-1]
            if fnmatch.fnmatch(rel_path, pattern) or rel_path.startswith(pattern + '/'):
                return True
        # Handle file patterns
        else:
            if fnmatch.fnmatch(rel_path, pattern):
                return True
            if is_dir and fnmatch.fnmatch(rel_path, pattern + '/*'):
                return True
    
    return False

def generate_folder_structure(folder_path, output_file, prefix="", gitignore_patterns=None):
    """Generate a tree-like structure of the folder and save it to a file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(f"### Struktura folderu: {os.path.basename(folder_path)} ###\n\n")
            
            def write_structure(path, prefix=""):
                # Don't process if this path should be ignored
                if gitignore_patterns and should_ignore(path, gitignore_patterns, folder_path):
                    return
                
                if os.path.isfile(path):
                    outfile.write(f"{prefix}├── {os.path.basename(path)}\n")
                else:
                    # Ensure directory itself is not skipped if the pattern was only for contents
                    # This is a simplification, full gitignore is more complex
                    if prefix != "": # Avoid skipping the root directory entry
                         outfile.write(f"{prefix}└── {os.path.basename(path)}/\n")
                    
                    prefix += "    "
                    
                    items = sorted(os.listdir(path))
                    for i, item in enumerate(items):
                        item_path = os.path.join(path, item)
                        # Check again for each item if it should be ignored
                        if gitignore_patterns and should_ignore(item_path, gitignore_patterns, folder_path):
                            continue
                            
                        is_last = i == len(items) - 1
                        current_prefix = prefix[:-4] + ("└── " if is_last else "├── ")
                        
                        if os.path.isdir(item_path):
                            # Recursive call will check should_ignore again for the directory
                            write_structure(item_path, prefix + "    ")
                        else:
                            outfile.write(f"{current_prefix}{item}\n")
            
            write_structure(folder_path)
            
        messagebox.showinfo("Sukces", f"Struktura folderu została zapisana do: {output_file}")
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił problem podczas generowania struktury folderu: {e}")

def get_all_files(folder_path, gitignore_patterns=None):
    """Get all files from a folder and its subfolders, respecting .gitignore patterns."""
    all_files = []
    # Use os.walk but filter based on gitignore
    for root, dirs, files in os.walk(folder_path, topdown=True):
        # Filter directories in-place to prevent os.walk from entering ignored ones
        if gitignore_patterns:
             # Create a list of indices to remove from dirs
            dirs_to_remove = []
            for i in range(len(dirs)):
                dir_path = os.path.join(root, dirs[i])
                if should_ignore(dir_path, gitignore_patterns, folder_path):
                    dirs_to_remove.append(i)
            
            # Remove ignored directories (iterate backwards to avoid index issues)
            for i in sorted(dirs_to_remove, reverse=True):
                del dirs[i]

        for file in files:
            file_path = os.path.join(root, file)
            if not gitignore_patterns or not should_ignore(file_path, gitignore_patterns, folder_path):
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

        # Get all gitignore patterns from all .gitignore files
        gitignore_patterns = get_all_gitignore_patterns(folder_path)
        
        generate_folder_structure(folder_path, output_file, gitignore_patterns=gitignore_patterns)
    
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
            # Get all gitignore patterns from all .gitignore files
            gitignore_patterns = get_all_gitignore_patterns(folder_path)
            
            # Najpierw generujemy strukturę folderu
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(f"### Struktura folderu: {os.path.basename(folder_path)} ###\n\n")
                
                # Use the improved write_structure function
                def write_structure(path, prefix=""):
                    if gitignore_patterns and should_ignore(path, gitignore_patterns, folder_path):
                        return
                    
                    if os.path.isfile(path):
                        outfile.write(f"{prefix}├── {os.path.basename(path)}\n")
                    else:
                        if prefix != "": # Avoid skipping the root directory entry
                            outfile.write(f"{prefix}└── {os.path.basename(path)}/\n")
                        
                        prefix += "    "
                        
                        items = sorted(os.listdir(path))
                        for i, item in enumerate(items):
                            item_path = os.path.join(path, item)
                            if gitignore_patterns and should_ignore(item_path, gitignore_patterns, folder_path):
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
                # get_all_files already uses gitignore_patterns
                all_files = get_all_files(folder_path, gitignore_patterns)
                for file_path in all_files:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(f"### Zawartość pliku: {os.path.relpath(file_path, folder_path)} ###\n")
                            outfile.write(infile.read())
                            outfile.write("\n\n")
                    except Exception as e:
                        # Add error message if file cannot be read (e.g. binary file)
                        outfile.write(f"### Nie można odczytać pliku: {os.path.relpath(file_path, folder_path)} - {e} ###\n\n")

            messagebox.showinfo("Sukces", f"Struktura folderu i zawartość plików zostały zapisane do: {output_file}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił problem podczas przetwarzania folderu: {e}")
    
    else:
        messagebox.showinfo("Błąd", "Nieprawidłowy tryb działania.")

if __name__ == "__main__":
    merge_files()
