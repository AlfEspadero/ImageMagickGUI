# GitHub Workflows Documentation

This document explains the GitHub Actions workflows set up for the ImageMagick GUI project.

## 🔄 **Available Workflows**

### 1. **CI - Test and Lint** (`ci.yml`)
**Triggers:** Push to main/develop, Pull Requests to main

**What it does:**
- Tests the application on Windows, macOS, and Linux
- Tests with Python 3.8, 3.9, 3.10, 3.11, 3.12
- Installs ImageMagick on each platform
- Runs code linting with flake8
- Verifies package installation
- Checks if ImageMagick is available

**Status Badge:**
```markdown
![CI](https://github.com/AlfEspadero/ImageMagickGUI/workflows/CI%20-%20Test%20and%20Lint/badge.svg)
```

### 2. **Build Executables** (`build.yml`)
**Triggers:** Version tags (v*), Manual dispatch

**What it does:**
- Builds standalone executables for Windows, macOS, and Linux
- Creates release packages with documentation
- Uploads artifacts for download
- Automatically attaches to releases when tagged

**Outputs:**
- `ImageMagick-GUI-Windows.zip`
- `ImageMagick-GUI-macOS.zip`  
- `ImageMagick-GUI-Linux.tar.gz`

### 3. **Release** (`release.yml`)
**Triggers:** Version tags (v*)

**What it does:**
- Creates GitHub releases automatically
- Builds and uploads executables for all platforms
- Generates release notes with download instructions
- Includes ImageMagick installation instructions

### 4. **Code Quality** (`code-quality.yml`)
**Triggers:** Push to main, Pull Requests

**What it does:**
- Checks code formatting with Black
- Checks import sorting with isort
- Advanced linting with flake8
- Validates package metadata
- Checks version consistency

## 🚀 **How to Use**

### **For Development:**
1. **Push code** → CI workflow runs automatically
2. **Open PR** → CI + Code Quality workflows run
3. **Merge PR** → All workflows run on main branch

### **For Releases:**
1. **Update version** in `setup.py` and `pyproject.toml`
2. **Commit changes** and push to main
3. **Create and push tag:**
   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```
4. **Automatic magic happens:**
   - Release workflow creates GitHub release
   - Build workflow creates executables for all platforms
   - Release gets populated with download links

### **Manual Building:**
You can trigger builds manually from GitHub Actions tab:
- Go to Actions → "Build Executables" → "Run workflow"

## 📊 **Status Badges**

Add these to your README.md:

```markdown
![CI](https://github.com/AlfEspadero/ImageMagickGUI/workflows/CI%20-%20Test%20and%20Lint/badge.svg)
![Code Quality](https://github.com/AlfEspadero/ImageMagickGUI/workflows/Code%20Quality/badge.svg)
![Build](https://github.com/AlfEspadero/ImageMagickGUI/workflows/Build%20Executables/badge.svg)
```

## 🔧 **Configuration**

### **Supported Platforms:**
- **Windows**: Creates `.exe` with PyInstaller
- **macOS**: Creates `.app` bundle  
- **Linux**: Creates standalone executable

### **Python Versions Tested:**
- Python 3.8, 3.9, 3.10, 3.11, 3.12
- Primary build uses Python 3.11

### **Dependencies:**
- All workflows install ImageMagick automatically
- PyInstaller for executable creation
- Code quality tools (black, flake8, isort)

## 🐛 **Troubleshooting**

### **Common Issues:**

1. **Build fails on tkinter import:**
   - Ubuntu workflow installs `python3-tk`
   - Windows/macOS should have tkinter by default

2. **ImageMagick not found:**
   - Workflows install ImageMagick on all platforms
   - Check the installation commands in workflow files

3. **Version tag not triggering release:**
   - Ensure tag follows `v*` format (e.g., `v1.0.0`)
   - Check that tag is pushed: `git push origin v1.0.0`

4. **Executable too large:**
   - PyInstaller bundles Python runtime (~10MB normal)
   - Use `--exclude-module` if needed to reduce size

## 📝 **Maintenance**

### **Updating Workflows:**
- Modify `.github/workflows/*.yml` files
- Test with manual triggers before tagging releases
- Check GitHub Actions logs for any issues

### **Adding New Platforms:**
- Add new matrix entries in `build.yml`
- Update platform-specific installation commands
- Test the build process manually first

---

**Note**: These workflows provide complete automation for testing, building, and releasing your ImageMagick GUI application across all major platforms!