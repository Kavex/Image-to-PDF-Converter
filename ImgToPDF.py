import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
from PIL import Image
import os

class PDFImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")

        self.image_list = []

        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.listbox = Listbox(self.frame, width=60, height=10)
        self.listbox.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        tk.Button(self.frame, text="Add Images", command=self.add_images).grid(row=1, column=0, sticky="ew")
        tk.Button(self.frame, text="Remove Selected", command=self.remove_selected).grid(row=1, column=1, sticky="ew")
        tk.Button(self.frame, text="Move Up", command=self.move_up).grid(row=1, column=2, sticky="ew")
        tk.Button(self.frame, text="Move Down", command=self.move_down).grid(row=1, column=3, sticky="ew")
        tk.Button(self.frame, text="Export to PDF", command=self.export_to_pdf, bg="lightgreen").grid(row=2, column=0, columnspan=4, sticky="ew", pady=(10, 0))

    def add_images(self):
        files = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")])
        for f in files:
            self.image_list.append(f)
            self.listbox.insert(tk.END, os.path.basename(f))

    def remove_selected(self):
        selected = self.listbox.curselection()
        for index in reversed(selected):
            del self.image_list[index]
            self.listbox.delete(index)

    def move_up(self):
        selected = self.listbox.curselection()
        if selected and selected[0] > 0:
            idx = selected[0]
            self.image_list[idx-1], self.image_list[idx] = self.image_list[idx], self.image_list[idx-1]
            self.refresh_listbox()
            self.listbox.select_set(idx-1)

    def move_down(self):
        selected = self.listbox.curselection()
        if selected and selected[0] < len(self.image_list)-1:
            idx = selected[0]
            self.image_list[idx+1], self.image_list[idx] = self.image_list[idx], self.image_list[idx+1]
            self.refresh_listbox()
            self.listbox.select_set(idx+1)

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for img in self.image_list:
            self.listbox.insert(tk.END, os.path.basename(img))

    def export_to_pdf(self):
        if not self.image_list:
            messagebox.showwarning("No images", "Add images before exporting.")
            return

        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not pdf_path:
            return

        images = []
        try:
            for file in self.image_list:
                img = Image.open(file).convert("RGB")
                images.append(img)
            images[0].save(pdf_path, save_all=True, append_images=images[1:])
            messagebox.showinfo("Success", f"PDF saved to:\n{pdf_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFImageConverterApp(root)
    root.mainloop()
