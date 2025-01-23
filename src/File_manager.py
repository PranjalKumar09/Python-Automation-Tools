import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

class AdvancedFileManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced File Manager")
        self.root.geometry("800x500")

        # Default Settings
        self.bg_color = "#1e1e1e"  # Dark Mode
        self.fg_color = "#ffffff"
        self.button_bg = "#3a3a3a"
        self.button_fg = "#ffffff"
        self.font_style = ("Arial", 12)

        # Apply Theme
        self.root.configure(bg=self.bg_color)

        # Top Frame (Directory Selection)
        self.top_frame = tk.Frame(self.root, bg=self.bg_color)
        self.top_frame.pack(fill=tk.X, padx=5, pady=5)

        self.path_entry = tk.Entry(self.top_frame, width=60, font=self.font_style, bg=self.button_bg, fg=self.fg_color)
        self.path_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.browse_button = tk.Button(self.top_frame, text="Browse", command=self.browse_directory, bg=self.button_bg, fg=self.button_fg)
        self.browse_button.pack(side=tk.LEFT, padx=5)

        # File Listbox
        self.file_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, font=self.font_style, bg=self.bg_color, fg=self.fg_color)
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.file_listbox.bind("<Double-Button-1>", self.open_item)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.file_listbox)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.file_listbox.yview)

        # Buttons Frame
        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.button_frame.pack(fill=tk.X, padx=5, pady=5)

        self.add_buttons()

        # Load Directory
        self.current_directory = os.getcwd()
        self.clipboard = None
        self.load_directory(self.current_directory)

    def add_buttons(self):
        """Creates styled buttons dynamically."""
        buttons = [
            ("Copy", self.copy_to_clipboard),
            ("Cut", self.cut_to_clipboard),
            ("Paste", self.paste_from_clipboard),
            ("Rename", self.bulk_rename),
            ("Delete", self.batch_delete),
            ("New Folders", self.create_x_folders),
            ("Customize", self.customize_ui)
        ]
        for text, command in buttons:
            tk.Button(self.button_frame, text=text, command=command, bg=self.button_bg, fg=self.button_fg, font=self.font_style).pack(side=tk.LEFT, padx=5, pady=2)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.load_directory(directory)

    def load_directory(self, directory):
        self.current_directory = directory
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, directory)

        self.file_listbox.delete(0, tk.END)
        try:
            for item in os.listdir(directory):
                self.file_listbox.insert(tk.END, item)
        except PermissionError:
            messagebox.showerror("Error", "Permission Denied")

    def get_selected_files(self):
        selected_files = [self.file_listbox.get(i) for i in self.file_listbox.curselection()]
        return [os.path.join(self.current_directory, file) for file in selected_files]

    def copy_to_clipboard(self):
        self.clipboard = ("copy", self.get_selected_files())

    def cut_to_clipboard(self):
        self.clipboard = ("move", self.get_selected_files())

    def paste_from_clipboard(self):
        if self.clipboard:
            operation, files = self.clipboard
            for file in files:
                destination = self.current_directory
                try:
                    if operation == "copy":
                        shutil.copy(file, destination)
                    elif operation == "move":
                        shutil.move(file, destination)
                    self.load_directory(self.current_directory)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Clipboard is empty")

    def batch_delete(self):
        files = self.get_selected_files()
        if files:
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete {len(files)} items?")
            if confirm:
                for file in files:
                    try:
                        if os.path.isfile(file):
                            os.remove(file)
                        else:
                            shutil.rmtree(file)
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
                self.load_directory(self.current_directory)

    def bulk_rename(self):
        files = self.get_selected_files()
        if not files:
            messagebox.showerror("Error", "No files selected")
            return

        pattern = simpledialog.askstring("Rename", "Enter base name (e.g., 'file_'):")
        if not pattern:
            return

        for i, file in enumerate(files):
            ext = os.path.splitext(file)[1]
            new_name = f"{pattern}{i}{ext}"
            new_path = os.path.join(self.current_directory, new_name)
            try:
                os.rename(file, new_path)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        self.load_directory(self.current_directory)

    def create_x_folders(self):
        x = simpledialog.askinteger("Create Folders", "How many folders?")
        if not x:
            return
        
        folder_name = simpledialog.askstring("Folder Name", "Enter base folder name:")
        if not folder_name:
            return

        def create_folders():
            for i in range(x):
                folder_path = os.path.join(self.current_directory, f"{folder_name}_{i}")
                os.makedirs(folder_path, exist_ok=True)
            self.load_directory(self.current_directory)

        threading.Thread(target=create_folders).start()

    def customize_ui(self):
        """Allows the user to customize the UI appearance."""
        color = simpledialog.askstring("Theme Color", "Enter background color (e.g., #282828 or 'white'):")
        if color:
            self.bg_color = color
            self.root.configure(bg=self.bg_color)
            self.top_frame.configure(bg=self.bg_color)
            self.button_frame.configure(bg=self.bg_color)
            self.file_listbox.configure(bg=self.bg_color)

        font_size = simpledialog.askinteger("Font Size", "Enter new font size:")
        if font_size:
            self.font_style = ("Arial", font_size)
            self.path_entry.configure(font=self.font_style)
            self.file_listbox.configure(font=self.font_style)

        messagebox.showinfo("Success", "Restart the app to apply changes.")

    def open_item(self, event):
        file_path = self.get_selected_files()[0] if self.get_selected_files() else None
        if file_path and os.path.isdir(file_path):
            self.load_directory(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedFileManager(root)
    root.mainloop()
