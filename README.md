# ImageMagick GUI Application

[![CI](https://github.com/AlfEspadero/ImageMagickGUI/actions/workflows/ci.yml/badge.svg)](https://github.com/AlfEspadero/ImageMagickGUI/actions/workflows/ci.yml)
[![Code Quality](https://github.com/AlfEspadero/ImageMagickGUI/workflows/Code%20Quality/badge.svg)](https://github.com/AlfEspadero/ImageMagickGUI/actions)
[![Build](https://github.com/AlfEspadero/ImageMagickGUI/workflows/Build%20Executables/badge.svg)](https://github.com/AlfEspadero/ImageMagickGUI/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
4. Run `python main.py`

### Method 2: Install from PyPI
```bash
pip install imagemagick-gui
imagemagick-gui  # Run the application
```

### Method 3: Install from Source
```bash
git clone https://github.com/AlfEspadero/ImageMagickGUI.git
cd ImageMagickGUI
python main.py
```

### Method 4: Install as Package
```bash
git clone https://github.com/AlfEspadero/ImageMagickGUI.git
cd ImageMagickGUI
pip install .
imagemagick-gui  # Run the installed application
```

## 🔧 **System Requirements**
- **Python 3.8+** (with tkinter support)
- **ImageMagick CLI** tool installed on your system

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

### Setting up Python with tkinter

The application requires Python with tkinter support. If you encounter tkinter issues:

#### Option 1: Using System Python (macOS)
```bash
/usr/bin/python3 main.py
```

#### Option 2: Using pyenv with tkinter (if available)
```bash
# Install Python with tkinter support via pyenv
pyenv install 3.11.6  # or another version with tkinter
pyenv local 3.11.6
python main.py
```

#### Option 3: Using conda
```bash
conda create -n imagemagick-gui python=3.11 tk
conda activate imagemagick-gui
python main.py
```

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
   ```bash
   python main.py
   # or if installed as package
   imagemagick-gui
   ```

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

## 🔨 **Development**

### Building from Source
```bash
git clone https://github.com/AlfEspadero/ImageMagickGUI.git
cd ImageMagickGUI

# Install in development mode
pip install -e .

# Run tests (if available)
python -m pytest

# Build distribution
python -m build
```

### Creating a Release
```bash
# Build the package
python -m build

# The built files will be in dist/
# - imagemagick-gui-1.0.0.tar.gz (source distribution)
# - imagemagick_gui-1.0.0-py3-none-any.whl (wheel)
```

## 🐛 **Troubleshooting**

### Common Issues
- **tkinter not found**: Install Python with tkinter support or use system Python
- **ImageMagick not found**: Install ImageMagick CLI tools for your OS
- **Permission errors**: Ensure write access to the output directory
- **Conversion fails**: Check that the input file format is supported by ImageMagick

## 📄 **License**
This project is open source and available under the MIT License.

## 🤝 **Contributing**
Contributions are welcome! Please feel free to submit a Pull Request.