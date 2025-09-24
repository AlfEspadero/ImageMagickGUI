# ImageMagick GUI Application

A simple Python GUI application that provides a user-friendly interface for ImageMagick image conversion functionality.

## Features
- **File Selection**: Browse and select input image files using a file dialog
- **Format Selection**: Choose output format from a dropdown menu (JPEG, PNG, BMP, TIFF, GIF, WebP)
- **Image Conversion**: Convert images using ImageMagick CLI tool
- **Progress Feedback**: Visual feedback during conversion process
- **Error Handling**: User-friendly error messages for common issues

## Requirements
- **Python 3.x** (with tkinter support)
- **ImageMagick CLI** tool installed on your system

### Setting up Python with tkinter

The application requires Python with tkinter support. If you encounter tkinter issues:

#### Option 1: Using System Python (assumming python in PATH)
```bash
python3 main.py
```

#### Option 2: Using pyenv (if available)
```bash
pyenv install 3.13  # or another version with tkinter
pyenv local 3.13
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

## Usage

1. Run the application:
```bash
python main.py
```

2. Click "Browse" to select an input image file
3. Choose the desired output format from the dropdown
4. Click "Convert" to process the image
5. The converted file will be saved in the same directory as the input file

## File Structure
```
ImageMagickGUI/
├── main.py                 # Main GUI application
├── README.md              # Project documentation
└── .github/
    └── copilot-instructions.md
```

## License
This project is open source and available under the MIT License.