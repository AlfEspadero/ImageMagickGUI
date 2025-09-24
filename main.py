#!/usr/bin/env python3
"""
ImageMagick GUI Application

A simple GUI application that provides an interface to ImageMagick's
image conversion functionality using tkinter.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import threading
from pathlib import Path


class ImageMagickGUI:
	def __init__(self, root):
		self.root = root
		self.root.title("ImageMagick GUI Converter")
		self.root.geometry("1024x768")
		self.root.resizable(True, True)

		# Variables
		self.input_file_path = tk.StringVar()
		self.output_format = tk.StringVar(value="png")
		self.add_suffix = tk.BooleanVar(value=True)
		self.is_converting = False

		self.setup_ui()
		self.check_imagemagick()

	def setup_ui(self):
		"""Set up the user interface"""
		# Main frame
		main_frame = ttk.Frame(self.root, padding="20")
		main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

		# Configure grid weights for responsiveness
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=1)
		main_frame.columnconfigure(1, weight=1)

		# Title
		title_label = ttk.Label(
			main_frame, text="ImageMagick GUI Converter", font=("Arial", 16, "bold")
		)
		title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

		# Input file selection
		ttk.Label(main_frame, text="Input File:").grid(
			row=1, column=0, sticky=tk.W, pady=5
		)

		input_entry = ttk.Entry(
			main_frame, textvariable=self.input_file_path, state="readonly", width=50
		)
		input_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)

		browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_file)
		browse_btn.grid(row=1, column=2, padx=(5, 0), pady=5)

		# Output format selection
		ttk.Label(main_frame, text="Output Format:").grid(
			row=2, column=0, sticky=tk.W, pady=5
		)

		format_combo = ttk.Combobox(
			main_frame,
			textvariable=self.output_format,
			values=["png", "jpg", "jpeg", "bmp", "tiff", "gif", "webp", "pdf"],
			state="readonly",
			width=20,
		)
		format_combo.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)

		# Add suffix checkbox
		suffix_checkbox = ttk.Checkbutton(
			main_frame,
			text='Add "_converted" suffix to filename',
			variable=self.add_suffix,
		)
		suffix_checkbox.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=5)

		# Convert button
		self.convert_btn = ttk.Button(
			main_frame,
			text="Convert Image",
			command=self.convert_image,
			style="Accent.TButton",
		)
		self.convert_btn.grid(row=4, column=0, columnspan=3, pady=20)

		# Progress bar
		self.progress = ttk.Progressbar(main_frame, mode="indeterminate")
		self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

		# Status label
		self.status_label = ttk.Label(main_frame, text="Ready", foreground="green")
		self.status_label.grid(row=6, column=0, columnspan=3, pady=5)

		# Output info frame
		info_frame = ttk.LabelFrame(main_frame, text="Conversion Info", padding="10")
		info_frame.grid(
			row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10
		)
		info_frame.columnconfigure(0, weight=1)
		main_frame.rowconfigure(7, weight=1)

		# Output text area with scrollbar
		text_frame = ttk.Frame(info_frame)
		text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
		text_frame.columnconfigure(0, weight=1)
		text_frame.rowconfigure(0, weight=1)

		self.output_text = tk.Text(
			text_frame, height=8, width=70, wrap=tk.WORD, state=tk.DISABLED
		)
		scrollbar = ttk.Scrollbar(
			text_frame, orient=tk.VERTICAL, command=self.output_text.yview
		)
		self.output_text.configure(yscrollcommand=scrollbar.set)

		self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
		scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

	def browse_file(self):
		"""Open file browser to select input image"""
		file_types = [
			("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif *.webp *.pdf"),
			("PNG files", "*.png"),
			("JPEG files", "*.jpg *.jpeg"),
			("BMP files", "*.bmp"),
			("TIFF files", "*.tiff"),
			("GIF files", "*.gif"),
			("WebP files", "*.webp"),
			("PDF files", "*.pdf"),
			("All files", "*.*"),
		]

		filename = filedialog.askopenfilename(
			title="Select Image File", filetypes=file_types
		)

		if filename:
			self.input_file_path.set(filename)
			self.log_message(f"Selected input file: {filename}")

	def check_imagemagick(self):
		"""Check if ImageMagick is installed"""
		try:
			result = subprocess.run(
				["magick", "-version"], capture_output=True, text=True, timeout=10
			)
			if result.returncode == 0:
				version_line = result.stdout.split("\n")[0]
				self.log_message(f"ImageMagick found: {version_line}")
			else:
				raise subprocess.CalledProcessError(result.returncode, "magick")
		except (
			subprocess.CalledProcessError,
			FileNotFoundError,
			subprocess.TimeoutExpired,
		):
			# Try legacy 'convert' command
			try:
				result = subprocess.run(
					["convert", "-version"], capture_output=True, text=True, timeout=10
				)
				if result.returncode == 0:
					version_line = result.stdout.split("\n")[0]
					self.log_message(f"ImageMagick found (legacy): {version_line}")
				else:
					raise subprocess.CalledProcessError(result.returncode, "convert")
			except (
				subprocess.CalledProcessError,
				FileNotFoundError,
				subprocess.TimeoutExpired,
			):
				self.log_message("⚠️  WARNING: ImageMagick not found!")
				self.log_message("Please install ImageMagick:")
				self.log_message("  macOS: brew install imagemagick")
				self.log_message("  Ubuntu: sudo apt-get install imagemagick")
				self.log_message("  Windows: Download from imagemagick.org")
				self.status_label.config(text="ImageMagick not found", foreground="red")

	def convert_image(self):
		"""Convert the selected image to the specified format"""
		if self.is_converting:
			return

		input_path = self.input_file_path.get().strip()
		if not input_path:
			messagebox.showerror("Error", "Please select an input file")
			return

		if not os.path.exists(input_path):
			messagebox.showerror("Error", "Input file does not exist")
			return

		# Start conversion in a separate thread
		self.is_converting = True
		self.convert_btn.config(state="disabled", text="Converting...")
		self.progress.start(10)
		self.status_label.config(text="Converting...", foreground="orange")

		conversion_thread = threading.Thread(
			target=self._perform_conversion, args=(input_path,)
		)
		conversion_thread.daemon = True
		conversion_thread.start()

	def _perform_conversion(self, input_path):
		"""Perform the actual conversion (runs in separate thread)"""
		try:
			# Generate output filename
			input_file = Path(input_path)
			output_format = self.output_format.get().lower()

			if self.add_suffix.get():
				# Add "_converted" suffix
				output_path = (
					input_file.parent / f"{input_file.stem}_converted.{output_format}"
				)
			else:
				# Use original filename with new extension
				output_path = input_file.parent / f"{input_file.stem}.{output_format}"

			self.log_message(f"Converting: {input_file.name}")
			self.log_message(f"Output: {output_path.name}")
			self.log_message(f"Format: {output_format.upper()}")

			# Try modern 'magick' command first, then fallback to 'convert'
			commands_to_try = [
				["magick", str(input_path), str(output_path)],
				["convert", str(input_path), str(output_path)],
			]

			success = False
			for cmd in commands_to_try:
				try:
					result = subprocess.run(
						cmd,
						capture_output=True,
						text=True,
						timeout=60,  # 60 second timeout
					)

					if result.returncode == 0:
						success = True
						break
					else:
						error_msg = (
							result.stderr.strip() if result.stderr else "Unknown error"
						)
						self.log_message(f"Command failed: {' '.join(cmd)}")
						self.log_message(f"Error: {error_msg}")

				except subprocess.TimeoutExpired:
					self.log_message(f"Command timed out: {' '.join(cmd)}")
				except FileNotFoundError:
					self.log_message(f"Command not found: {cmd[0]}")

			# Update UI on main thread
			self.root.after(0, self._conversion_complete, success, str(output_path))

		except Exception as e:
			self.root.after(0, self._conversion_error, str(e))

	def _conversion_complete(self, success, output_path):
		"""Handle conversion completion (runs on main thread)"""
		self.progress.stop()
		self.is_converting = False
		self.convert_btn.config(state="normal", text="Convert Image")

		if success and os.path.exists(output_path):
			self.status_label.config(text="Conversion successful!", foreground="green")
			self.log_message("✅ Conversion completed successfully!")
			self.log_message(f"Output saved: {output_path}")

			# Show success dialog
			messagebox.showinfo(
				"Success",
				f"Image converted successfully!\nSaved as: {os.path.basename(output_path)}",
			)
		else:
			self.status_label.config(text="Conversion failed", foreground="red")
			self.log_message("❌ Conversion failed!")
			messagebox.showerror(
				"Error", "Image conversion failed. Check the log for details."
			)

	def _conversion_error(self, error_msg):
		"""Handle conversion error (runs on main thread)"""
		self.progress.stop()
		self.is_converting = False
		self.convert_btn.config(state="normal", text="Convert Image")
		self.status_label.config(text="Error occurred", foreground="red")

		self.log_message(f"❌ Error: {error_msg}")
		messagebox.showerror("Error", f"An error occurred: {error_msg}")

	def log_message(self, message):
		"""Add a message to the output log"""
		self.output_text.config(state=tk.NORMAL)
		self.output_text.insert(tk.END, f"{message}\n")
		self.output_text.see(tk.END)
		self.output_text.config(state=tk.DISABLED)


def main():
	"""Main function to run the application"""
	root = tk.Tk()

	# Set up the application icon and style
	try:
		# Try to use a nicer theme if available
		style = ttk.Style()
		available_themes = style.theme_names()
		if "aqua" in available_themes:  # macOS
			style.theme_use("aqua")
		elif "clam" in available_themes:  # Cross-platform
			style.theme_use("clam")
	except:
		pass  # Use default theme if styling fails

	# Create and run the application
	app = ImageMagickGUI(root)

	# Center the window on screen
	root.update_idletasks()
	width = root.winfo_width()
	height = root.winfo_height()
	x = (root.winfo_screenwidth() // 2) - (width // 2)
	y = (root.winfo_screenheight() // 2) - (height // 2)
	root.geometry(f"{width}x{height}+{x}+{y}")

	# Start the GUI event loop
	root.mainloop()


if __name__ == "__main__":
	main()
