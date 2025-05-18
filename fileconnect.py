import os
from tkinter import Tk, filedialog, simpledialog, messagebox

def generate_folder_structure(folder_path, output_file, prefix=""):
    """Generate a tree-like structure of the folder and save it to a file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(f"### Struktura folderu: {os.path.basename(folder_path)} ###\n\n")
            
            def write_structure(path, prefix=""):
                if os.path.isfile(path):
                    outfile.write(f"{prefix}├── {os.path.basename(path)}\n")
                else:
                    outfile.write(f"{prefix}└── {os.path.basename(path)}/\n")
                    prefix += "    "
                    
                    items = sorted(os.listdir(path))
                    for i, item in enumerate(items):
                        item_path = os.path.join(path, item)
                        is_last = i == len(items) - 1
                        current_prefix = prefix[:-4] + ("└── " if is_last else "├── ")
                        
                        if os.path.isdir(item_path):
                            outfile.write(f"{current_prefix}{item}/\n")
                            write_structure(item_path, prefix + "    ")
                        else:
                            outfile.write(f"{current_prefix}{item}\n")
            
            write_structure(folder_path)
            
        messagebox.showinfo("Sukces", f"Struktura folderu została zapisana do: {output_file}")
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił problem podczas generowania struktury folderu: {e}")

def merge_files():
    # Tworzenie okna tkinter
    root = Tk()
    root.withdraw()  # Ukryj główne okno
    root.title("Łączenie plików tekstowych")

    # Wybierz tryb działania
    mode = simpledialog.askstring("Tryb", "Wybierz tryb:\n1 - Łączenie plików\n2 - Generowanie struktury folderu")
    
    if mode == "1":
        # Wybierz pliki do połączenia
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
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(f"### Zawartość pliku: {os.path.basename(file_path)} ###\n")
                        outfile.write(infile.read())
                        outfile.write("\n\n")
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

        generate_folder_structure(folder_path, output_file)
    
    else:
        messagebox.showinfo("Błąd", "Nieprawidłowy tryb działania.")

if __name__ == "__main__":
    merge_files()
