import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from PIL import Image, ImageTk, ImageDraw
import os

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator with Logo")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        self.logo_path = None
        self.qr_image = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container with two columns
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Title
        title_frame = tk.Frame(self.root, bg="#6B46C1", height=80)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        title_frame.grid_propagate(False)
        
        title_label = tk.Label(title_frame, text="QR Code Generator", 
                              font=("Segoe UI", 24, "bold"), 
                              bg="#6B46C1", fg="white")
        title_label.pack(expand=True)
        
        # Left Panel - Configuration
        left_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=20)
        
        config_label = tk.Label(left_frame, text="Configuration", 
                               font=("Segoe UI", 14, "bold"), 
                               bg="white", fg="#333")
        config_label.pack(anchor="w", pady=(0, 15))
        
        # Data input
        tk.Label(left_frame, text="Enter Data/URL:", 
                font=("Segoe UI", 10), bg="white", fg="#555").pack(anchor="w")
        self.data_entry = tk.Text(left_frame, height=4, width=35, 
                                 font=("Segoe UI", 10), relief="solid", 
                                 borderwidth=1, wrap="word")
        self.data_entry.pack(fill="x", pady=(5, 15))
        
        # Logo selection
        tk.Label(left_frame, text="Logo/Image:", 
                font=("Segoe UI", 10,"bold"), bg="white", fg="#555", ).pack(anchor="w")
        
        logo_frame = tk.Frame(left_frame, bg="white")
        logo_frame.pack(fill="x", pady=(5, 15))
        
        self.logo_label = tk.Label(logo_frame, text="unnamed.png", 
                                   font=("Segoe UI", 9), bg="white", 
                                   fg="#888", anchor="w")
        self.logo_label.pack(side="left", fill="x", expand=True)
        
        browse_btn = tk.Button(logo_frame, text="Browse Image", 
                              command=self.select_logo,
                              bg="#E0E0E0", fg="#333", 
                              font=("Segoe UI", 9),
                              relief="flat", padx=15, pady=5,
                              cursor="hand2")
        browse_btn.pack(side="left", padx=5)
        
        clear_btn = tk.Button(logo_frame, text="Clear", 
                             command=self.clear_logo,
                             bg="#E0E0E0", fg="#333", 
                             font=("Segoe UI", 9),
                             relief="flat", padx=15, pady=5,
                             cursor="hand2")
        clear_btn.pack(side="left")
        
        # QR Code Size
        tk.Label(left_frame, text="QR Code Size:", 
                font=("Segoe UI", 10), bg="white", fg="#555").pack(anchor="w", pady=(5, 5))
        
        size_frame = tk.Frame(left_frame, bg="white")
        size_frame.pack(fill="x", pady=(0, 15))
        
        self.size_var = tk.StringVar(value="Medium")
        
        sizes = [("Small", "Small"), ("Medium", "Medium"), ("Large", "Large")]
        for text, value in sizes:
            rb = tk.Radiobutton(size_frame, text=text, variable=self.size_var,
                               value=value, bg="white", fg="#333",
                               font=("Segoe UI", 9), selectcolor="#E0E0E0",
                               activebackground="white", cursor="hand2")
            rb.pack(side="left", padx=(0, 15))
        
        # Error Correction
        tk.Label(left_frame, text="Error Correction:", 
                font=("Segoe UI", 10), bg="white", fg="#555").pack(anchor="w", pady=(5, 5))
        
        self.error_var = tk.StringVar(value="High (Recommended)")
        error_combo = ttk.Combobox(left_frame, textvariable=self.error_var,
                                   values=["Low", "Medium", "High (Recommended)"],
                                   state="readonly", font=("Segoe UI", 9))
        error_combo.pack(fill="x", pady=(0, 15))
        
        # Logo Size Slider
        tk.Label(left_frame, text="Logo Size:", 
                font=("Segoe UI", 10), bg="white", fg="#555").pack(anchor="w", pady=(5, 5))
        
        slider_frame = tk.Frame(left_frame, bg="white")
        slider_frame.pack(fill="x", pady=(0, 15))
        
        self.logo_size_var = tk.IntVar(value=24)
        logo_slider = tk.Scale(slider_frame, from_=10, to=40, 
                              orient="horizontal", variable=self.logo_size_var,
                              bg="white", fg="#333", 
                              troughcolor="#E0E0E0",
                              highlightthickness=0, 
                              font=("Segoe UI", 8))
        logo_slider.pack(side="left", fill="x", expand=True)
        
        self.logo_size_label = tk.Label(slider_frame, text="24%", 
                                       font=("Segoe UI", 9), 
                                       bg="white", fg="#333", width=5)
        self.logo_size_label.pack(side="left", padx=5)
        self.logo_size_var.trace('w', self.update_logo_size_label)
        
        # Buttons
        button_frame = tk.Frame(left_frame, bg="white")
        button_frame.pack(fill="x", pady=(10, 0))
        
        generate_btn = tk.Button(button_frame, text="Generate QR Code",
                                command=self.generate_qr,
                                bg="#00BCD4", fg="white",
                                font=("Segoe UI", 11, "bold"),
                                relief="flat", padx=20, pady=12,
                                cursor="hand2")
        generate_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        save_btn = tk.Button(button_frame, text="Save QR Code",
                           command=self.save_qr,
                           bg="#4CAF50", fg="white",
                           font=("Segoe UI", 11, "bold"),
                           relief="flat", padx=20, pady=12,
                           cursor="hand2")
        save_btn.pack(side="left", fill="x", expand=True)
        
        # Right Panel - Preview
        right_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=20)
        
        preview_label = tk.Label(right_frame, text="Preview", 
                                font=("Segoe UI", 14, "bold"), 
                                bg="white", fg="#333")
        preview_label.pack(anchor="w", pady=(0, 15))
        
        # Preview canvas with border
        preview_container = tk.Frame(right_frame, bg="#E0E0E0", 
                                    relief="solid", borderwidth=1)
        preview_container.pack(fill="both", expand=True)
        
        self.preview_label = tk.Label(preview_container, 
                                     text="QR code will appear here",
                                     bg="white", fg="#999",
                                     font=("Segoe UI", 11))
        self.preview_label.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Footer
        footer = tk.Label(self.root, text="QR Code Generator v1.0 - Minor Project",
                         font=("Segoe UI", 8), bg="#f0f0f0", fg="#888")
        footer.grid(row=2, column=0, columnspan=2, pady=10)
    
    def update_logo_size_label(self, *args):
        self.logo_size_label.config(text=f"{self.logo_size_var.get()}%")
    
    def select_logo(self):
        file_path = filedialog.askopenfilename(
            title="Select Logo Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), 
                      ("All files", "*.*")]
        )
        if file_path:
            self.logo_path = file_path
            filename = os.path.basename(file_path)
            self.logo_label.config(text=filename, fg="#333")
    
    def clear_logo(self):
        self.logo_path = None
        self.logo_label.config(text="No file chosen", fg="#888")
    
    def add_rounded_corners(self, img, radius):
        """Add rounded corners to an image"""
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
        
        result = Image.new('RGBA', img.size)
        result.paste(img, (0, 0))
        result.putalpha(mask)
        return result
    
    def generate_qr(self):
        data = self.data_entry.get("1.0", "end-1c").strip()
        
        if not data:
            messagebox.showwarning("Input Required", "Please enter data or URL!")
            return
        
        # Get error correction level
        error_map = {
            "Low": qrcode.constants.ERROR_CORRECT_L,
            "Medium": qrcode.constants.ERROR_CORRECT_M,
            "High (Recommended)": qrcode.constants.ERROR_CORRECT_H
        }
        error_level = error_map[self.error_var.get()]
        
        # Get size
        size_map = {"Small": 300, "Medium": 500, "Large": 700}
        target_size = size_map[self.size_var.get()]
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=error_level,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Generate QR code image with colors
        qr_img = qr.make_image(fill_color="black", 
                              back_color="white").convert('RGBA')
        
        # Resize QR code to target size
        qr_img = qr_img.resize((target_size, target_size), Image.Resampling.LANCZOS)
        
        # Add logo if selected
        if self.logo_path:
            try:
                logo = Image.open(self.logo_path).convert('RGBA')
                
                # Calculate logo size based on slider
                qr_width, qr_height = qr_img.size
                logo_percentage = self.logo_size_var.get() / 100
                logo_size = int(min(qr_width, qr_height) * logo_percentage)
                
                # Resize logo
                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                
                # Add rounded corners to logo
                corner_radius = logo_size // 8
                logo = self.add_rounded_corners(logo, corner_radius)
                
                # Add white background behind logo
                bg_size = int(logo_size * 1.15)
                background = Image.new('RGBA', (bg_size, bg_size), (255, 255, 255, 255))
                background = self.add_rounded_corners(background, corner_radius + 5)
                
                # Calculate position to center
                bg_pos = ((qr_width - bg_size) // 2, (qr_height - bg_size) // 2)
                logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                
                # Paste background and logo
                qr_img.paste(background, bg_pos, background)
                qr_img.paste(logo, logo_pos, logo)
                
            except Exception as e:
                messagebox.showerror("Logo Error", f"Error adding logo: {str(e)}")
        
        # Store the final image
        self.qr_image = qr_img
        
        # Display preview
        display_size = 400
        display_img = qr_img.copy()
        display_img.thumbnail((display_size, display_size), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(display_img)
        self.preview_label.config(image=photo, text="")
        self.preview_label.image = photo
        
        messagebox.showinfo("Success", "QR Code generated successfully!")
    
    def save_qr(self):
        if self.qr_image is None:
            messagebox.showwarning("No QR Code", "Please generate a QR code first!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), 
                      ("JPEG files", "*.jpg"), 
                      ("All files", "*.*")]
        )
        
        if file_path:
            try:
                if file_path.lower().endswith(('.jpg', '.jpeg')):
                    rgb_img = Image.new('RGB', self.qr_image.size, (255, 255, 255))
                    rgb_img.paste(self.qr_image, mask=self.qr_image.split()[3] if self.qr_image.mode == 'RGBA' else None)
                    rgb_img.save(file_path, quality=95)
                else:
                    self.qr_image.save(file_path)
                
                messagebox.showinfo("Success", f"QR Code saved successfully!")
            except Exception as e:
                messagebox.showerror("Save Error", f"Error saving file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()
