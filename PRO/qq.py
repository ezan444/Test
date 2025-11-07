import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from PIL import Image, ImageTk, ImageDraw

# Global variables
logo_path = None
qr_image = None

# Add rounded corners to image
def add_rounded_corners(img, radius):
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
    result = Image.new('RGBA', img.size)
    result.paste(img, (0, 0))
    result.putalpha(mask)
    return result

# Select logo file
def select_logo():
    global logo_path
    file = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
    if file:
        logo_path = file
        logo_btn.config(text=file.split('/')[-1])

# Clear logo
def clear_logo():
    global logo_path
    logo_path = None
    logo_btn.config(text="Browse image")

# Generate QR code
def generate_qr():
    global qr_image
    
    data = text_box.get("1.0", "end-1c").strip()
    if not data:
        messagebox.showwarning("Error", "Please enter data!")
        return
    
    # Get selected size
    size = 300 if size_var.get() == 1 else 500 if size_var.get() == 2 else 700
    
    # Create QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=4,
                       error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')
    qr_img = qr_img.resize((size, size), Image.Resampling.LANCZOS)
    
    # Add logo if selected
    if logo_path:
        try:
            logo = Image.open(logo_path).convert('RGBA')
            logo_size = int(size * 0.24)
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            logo = add_rounded_corners(logo, logo_size // 8)
            
            bg_size = int(logo_size * 1.15)
            bg = Image.new('RGBA', (bg_size, bg_size), (255, 255, 255, 255))
            bg = add_rounded_corners(bg, logo_size // 8 + 5)
            
            qr_img.paste(bg, ((size - bg_size) // 2, (size - bg_size) // 2), bg)
            qr_img.paste(logo, ((size - logo_size) // 2, (size - logo_size) // 2), logo)
        except:
            messagebox.showerror("Error", "Failed to add logo!")
            return
    
    qr_image = qr_img
    
    # Show preview
    display = qr_img.copy()
    display.thumbnail((400, 400), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(display)
    preview.config(image=photo)
    preview.image = photo
    messagebox.showinfo("Success", "QR Code generated!")

# Save QR code
def save_qr():
    if qr_image is None:
        messagebox.showwarning("Error", "Generate QR code first!")
        return
    
    file = filedialog.asksaveasfilename(defaultextension=".png",
                                        filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
    if file:
        if file.endswith('.jpg') or file.endswith('.jpeg'):
            rgb = Image.new('RGB', qr_image.size, (255, 255, 255))
            rgb.paste(qr_image, mask=qr_image.split()[3])
            rgb.save(file, quality=95)
        else:
            qr_image.save(file)
        messagebox.showinfo("Success", "QR Code saved!")

# Create main window
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("1000x700")
root.config(bg="#f0f0f0")

# Header
header = tk.Frame(root, bg="#6B46C1", height=70)
header.pack(fill="x")
tk.Label(header, text="QR Code Generator", font=("Arial", 22, "bold"),
         bg="#6B46C1", fg="white").pack(pady=15)

# Main container
main = tk.Frame(root, bg="#f0f0f0")
main.pack(fill="both", expand=True, padx=20, pady=20)

# Left side
left = tk.Frame(main, bg="white", padx=20, pady=20, width=400)
left.pack(side="left", fill="both", padx=(0, 10),pady=(0,40))

tk.Label(left, text="Configuration", font=("Arial", 13, "bold"),
         bg="white").pack(anchor="w", pady=(0, 10))

# Data input
tk.Label(left, text="Enter Data/URL:", font=("Arial", 9), bg="white").pack(anchor="w")
text_box = tk.Text(left, height=4, width=40, font=("Arial", 10))
text_box.pack(pady=(5, 15))

# Logo buttons
tk.Label(left, text="Logo/Image:", font=("Arial", 9), bg="white").pack(anchor="w")
logo_frame = tk.Frame(left, bg="white")
logo_frame.pack(fill="x", pady=(5, 15))
logo_btn = tk.Button(logo_frame, text="Browse Image", command=select_logo,
                     bg="#E0E0E0", font=("Arial", 9), relief="flat", padx=15, pady=5)
logo_btn.pack(side="left", padx=(0, 5))
tk.Button(logo_frame, text="Clear", command=clear_logo,
          bg="#E0E0E0", font=("Arial", 9), relief="flat", padx=15, pady=5).pack(side="left")

# Size selection
tk.Label(left, text="QR Code Size:", font=("Arial", 9), bg="white").pack(anchor="w")
size_var = tk.IntVar(value=2)
size_frame = tk.Frame(left, bg="white")
size_frame.pack(fill="x", pady=(5, 15))
tk.Radiobutton(size_frame, text="Small", variable=size_var, value=1,
               bg="white", font=("Arial", 9)).pack(side="left", padx=(0, 10))
tk.Radiobutton(size_frame, text="Medium", variable=size_var, value=2,
               bg="white", font=("Arial", 9)).pack(side="left", padx=(0, 10))
tk.Radiobutton(size_frame, text="Large", variable=size_var, value=3,
               bg="white", font=("Arial", 9)).pack(side="left")

# Action buttons
btn_frame = tk.Frame(left, bg="white")
btn_frame.pack(fill="x", pady=(20, 0))
tk.Button(btn_frame, text="Generate QR Code", command=generate_qr,
          bg="#00BCD4", fg="white", font=("Arial", 10, "bold"),
          relief="flat", padx=15, pady=10).pack(side="left", fill="x", expand=True, padx=(0, 5))
tk.Button(btn_frame, text="Save QR Code", command=save_qr,
          bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
          relief="flat", padx=15, pady=10).pack(side="left", fill="x", expand=True)

# Right side - Preview
right = tk.Frame(main, bg="white", padx=60, pady=20)
right.pack(side="right", fill="both", expand=True,padx=(90,0),pady=(0,40))

tk.Label(right, text="Preview", font=("Arial", 13, "bold"),
         bg="white").pack(anchor="w", pady=(0, 10))

preview_box = tk.Frame(right, bg="#E0E0E0", relief="solid", bd=1)
preview_box.pack(fill="both", expand=True)

preview = tk.Label(preview_box, text="QR code will appear here",
                   bg="white", fg="#999", font=("Arial", 10))
preview.pack(fill="both", expand=True, padx=20, pady=20)

# Footer
tk.Label(root, text="QR Code Generator - Minor Project", font=("Arial", 8),
         bg="#f0f0f0", fg="#888").pack(pady=10)

root.mainloop()