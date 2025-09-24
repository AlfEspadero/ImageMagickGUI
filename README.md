# ImageMagick GUI Application

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build and Release](https://github.com/AlfEspadero/ImageMagickGUI/actions/workflows/simple.yml/badge.svg)](https://github.com/AlfEspadero/ImageMagickGUI/actions/workflows/simple.yml)

A simple Python GUI application that provides a user-friendly interface for ImageMagick image conversion functionality.

## 🚀 **Features**
- **File Selection**: Browse and select input image files using a file dialog
- **Format Selection**: Choose output format from a dropdown menu (JPEG, PNG, BMP, TIFF, GIF, WebP, PDF)
- **Suffix Toggle**: Option to add "_converted" suffix to output filenames
- **Image Conversion**: Convert images using ImageMagick CLI tool
- **Progress Feedback**: Visual feedback during conversion process
- **Error Handling**: User-friendly error messages for common issues
- **Cross-Platform**: Works on macOS, Linux, and Windows

## 📦 **Installation**

### Method 1: Download Release (Recommended)
1. Go to the [Releases](https://github.com/AlfEspadero/ImageMagickGUI/releases) page
2. Download the latest release
3. Extract the files
4. Run the executable for your OS:
   - **macOS/Linux**: `./imagemagick-gui`
   - **Windows**: `imagemagick-gui.exe`

### Method 2: Install from Source
```bash
git clone https://github.com/AlfEspadero/ImageMagickGUI.git
cd ImageMagickGUI
python main.py
```

## 🔧 **System Requirements**
- **Python 3.8+** (with tkinter support)
- **ImageMagick** tool installed on your system

### Installing ImageMagick

#### macOS (using Homebrew)
```bash
brew install imagemagick
```

#### Ubuntu/Debian
```bash
sudo apt-get install imagemagick
```

#### Windows
Download and install from [ImageMagick official website](https://imagemagick.org/script/download.php#windows)

## 🎯 **Usage**

1. **Launch the application**:
   Run the executable for your OS:
   - **macOS/Linux**: `./imagemagick-gui`
   - **Windows**: `imagemagick-gui.exe`

2. **Convert images**:
   - Click "Browse" to select an input image file
   - Choose the desired output format from the dropdown
   - Toggle the "_converted" suffix option if desired
   - Click "Convert" to process the image
   - The converted file will be saved in the same directory as the input file

## 📁 **File Structure**
```
ImageMagickGUI/
├── main.py                     # Main GUI application
├── README.md                   # Project documentation
├── pyproject.toml             # Package configuration
├── requirements.txt           # Dependencies (none for runtime)
├── .gitignore                # Git ignore file
└── .github/
    └── copilot-instructions.md
```

## 🐛 **Troubleshooting**

### Common Issues
- **ImageMagick not found**: Install ImageMagick CLI tools for your OS
- **Invalid file format**: Ensure the input file is a supported image format
- **Not launching**: Verify executable permissions (`chmod +x imagemagick-gui` on macOS/Linux)
- **Permission errors**: Ensure write access to the output directory

## 📄 **License**
This project is open source and available under the MIT License.

## 🤝 **Contributing**
Contributions are welcome! Please feel free to submit a Pull Request.