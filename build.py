#!/usr/bin/env python3
"""
Build script for ImageMagick GUI

This script helps build and package the ImageMagick GUI application
for distribution.
"""

import subprocess
import sys
import shutil
from pathlib import Path


def run_command(cmd, description):
	"""Run a shell command and handle errors."""
	print(f"🔨 {description}...")
	try:
		if isinstance(cmd, str):
			cmd = cmd.split()
		result = subprocess.run(
			cmd, shell=False, check=True, capture_output=True, text=True
		)
		print(f"✅ {description} completed successfully")
		if result.stdout:
			print(f"   Output: {result.stdout.strip()}")
		return True
	except subprocess.CalledProcessError as e:
		print(f"❌ {description} failed")
		print(f"   Error: {e.stderr.strip() if e.stderr else str(e)}")
		return False


def check_prerequisites():
	"""Check if build tools are available."""
	print("🔍 Checking prerequisites...")

	# Check Python version
	if sys.version_info < (3, 8):
		print("❌ Python 3.8+ required")
		return False
	print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} found")

	# Check build tools
	try:
		import build

		print("✅ build module found")
	except ImportError:
		print("⚠️  build module not found. Installing...")
		if not run_command(
			f"{sys.executable} -m pip install build", "Installing build"
		):
			return False

	return True


def clean_build():
	"""Clean previous build artifacts."""
	print("🧹 Cleaning build artifacts...")

	dirs_to_clean = ["build", "dist", "*.egg-info"]
	for pattern in dirs_to_clean:
		for path in Path(".").glob(pattern):
			if path.is_dir():
				shutil.rmtree(path)
				print(f"   Removed {path}")
			elif path.is_file():
				path.unlink()
				print(f"   Removed {path}")


def build_package():
	"""Build the package."""
	if not run_command(f"{sys.executable} -m build", "Building package"):
		return False

	# List built files
	dist_dir = Path("dist")
	if dist_dir.exists():
		print("\n📦 Built packages:")
		for file in dist_dir.iterdir():
			if file.is_file():
				size = file.stat().st_size
				print(f"   {file.name} ({size:,} bytes)")

	return True


def test_package():
	"""Test the built package."""
	print("\n🧪 Testing package...")

	# Test import
	if not run_command(
		f"{sys.executable} -c 'import main; print(\"✅ Module imports successfully\")'",
		"Testing module import",
	):
		return False

	# Check if wheel can be installed (dry run)
	wheel_files = list(Path("dist").glob("*.whl"))
	if wheel_files:
		wheel_file = wheel_files[0]
		if not run_command(
			f"{sys.executable} -m pip install --dry-run {wheel_file}",
			"Testing wheel installation (dry run)",
		):
			return False

	return True


def main():
	"""Main build process."""
	print("🚀 ImageMagick GUI - Build Process")
	print("=" * 50)

	if not check_prerequisites():
		sys.exit(1)

	clean_build()

	if not build_package():
		sys.exit(1)

	if not test_package():
		print("⚠️  Package tests failed, but build completed")

	print("\n🎉 Build completed successfully!")
	print("\n📁 Distribution files created in 'dist/' directory")
	print("   - Source distribution (.tar.gz)")
	print("   - Wheel distribution (.whl)")

	print("\n🚀 Next steps:")
	print("   - Test installation: pip install dist/*.whl")
	print("   - Create GitHub release with these files")
	print("   - Optionally upload to PyPI: python -m twine upload dist/*")


if __name__ == "__main__":
	main()
