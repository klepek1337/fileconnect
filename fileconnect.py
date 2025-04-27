import os
from tkinter import Tk, filedialog, simpledialog, messagebox

def merge_files():
    # Tworzenie okna tkinter
    root = Tk()
    root.withdraw()  # Ukryj główne okno
    root.title("Łączenie plików tekstowych")

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

if __name__ == "__main__":
    merge_files()
