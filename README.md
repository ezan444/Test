QR Code Generator application built using Python. This application allows users to create customized QR codes with logos, different colors, and various sizes. It's useful for businesses, marketing, and personal branding where you want to create professional-looking QR codes with company logos."


Key Properties:

Data Capacity: Can store up to 4,296 alphanumeric characters
Error Correction: Can still be read even if partially damaged
Fast Scanning: Can be read from any angle


ARCHITECTURE:
Application Structure:
├── Main Window (1000x700)
│   ├── Header (Purple bar with title)
│   ├── Left Panel - Configuration
│   │   ├── Data Input
│   │   ├── Logo Selection
│   │   ├── Size Options
│   │   ├── Error Correction
│   │   ├── Logo Size Slider
│   │   ├── Color Pickers
│   │   └── Action Buttons
│   └── Right Panel - Preview
│       └── QR Code Display




1. **`__init__`**: *"Initializes the application, sets default values, and calls setup_ui"*

2. **`setup_ui`**: *"Creates all GUI elements - frames, buttons, labels, input fields"*

3. **`generate_qr`**: *"The main logic - takes user input, creates QR code object, applies colors, adds logo if selected, and displays preview"*

4. **`add_rounded_corners`**: *"Image processing function that uses PIL to create transparency masks for rounded corners"*

5. **`save_qr`**: *"Handles file saving, converts RGBA to RGB for JPEG format, shows success/error messages"*
