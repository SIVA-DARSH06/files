import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
from PIL import Image
import os


class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.image_paths = []
        self.output_pdf_name = tk.StringVar()
        self.selected_image_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)

        self.initialize_ui()

    def initialize_ui(self):
        title_label = tk.Label(self.root, text="Image to PDF Converter", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        select_images_button = tk.Button(self.root, text="Select Images", command=self.select_images)
        select_images_button.pack(pady=(0, 10))

        self.selected_image_listbox.pack(pady=(0, 10), fill=tk.BOTH, expand=True)

        label = tk.Label(self.root, text="Enter output PDF name:")
        label.pack()

        pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width=40, justify="center")
        pdf_name_entry.pack()

        convert_button = tk.Button(self.root, text="Convert to PDF", command=self.convert_images_to_pdf)
        convert_button.pack(pady=(20, 40))

    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.update_selected_images_listbox()

    def update_selected_images_listbox(self):
        self.selected_image_listbox.delete(0, tk.END)
        for image_path in self.image_paths:
            image_name = os.path.split(image_path)[1]
            self.selected_image_listbox.insert(tk.END, image_name)

    def convert_images_to_pdf(self):
        if not self.image_paths:
            messagebox.showwarning("No Images Selected", "Please select images to convert.")
            return
        
        output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "output.pdf"
        
        pdf = canvas.Canvas(output_pdf_path, pagesize=(400, 400))

        for image_path in self.image_paths:
            img = Image.open(image_path)
            available_width = 350
            available_height = 350
            scale_factor = min(available_width / img.width, available_height / img.height)
            new_width = img.width * scale_factor
            new_height = img.height * scale_factor
            x_centred = (400 - new_width) / 2
            y_centred = (400 - new_height) / 2

            pdf.setFillColorRGB(1, 1, 1)
            pdf.rect(0, 0, 400, 400, fill=True)
            pdf.drawInlineImage(img, x_centred, y_centred, width=new_width, height=new_height)
            pdf.showPage()
        
        pdf.save()
        messagebox.showinfo("Conversion Complete", f"PDF saved as {output_pdf_path}")


def main():
    root = tk.Tk()
    root.title("Image to PDF")
    converter = ImageToPDFConverter(root)
    root.geometry("500x500")
    root.mainloop()


if __name__ == "__main__":
    main()
