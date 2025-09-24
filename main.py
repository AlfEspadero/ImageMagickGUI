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
		self.root.geometry("1200x900")
		self.root.resizable(True, True)

		# Variables
		self.input_file_path = tk.StringVar()
		self.output_format = tk.StringVar(value="png")
		self.add_suffix = tk.BooleanVar(value=True)
		self.output_directory = tk.StringVar()
		self.use_custom_output_dir = tk.BooleanVar(value=False)
		self.is_converting = False
		self.file_list = []  # List of files for batch conversion
		self.current_preview_file = None

		self.setup_ui()
		self.check_imagemagick()

	def setup_ui(self):
		"""Set up the user interface"""
		# Create a notebook for tabs
		notebook = ttk.Notebook(self.root)
		notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

		# Single conversion tab
		single_frame = ttk.Frame(notebook, padding="20")
		notebook.add(single_frame, text="Single Conversion")

		# Batch conversion tab
		batch_frame = ttk.Frame(notebook, padding="20")
		notebook.add(batch_frame, text="Batch Conversion")

		self.setup_single_conversion_tab(single_frame)
		self.setup_batch_conversion_tab(batch_frame)

		# Bind common quit shortcuts
		self.root.bind_all("<Control-q>", lambda e: self._on_quit())
		self.root.bind_all("<Control-Q>", lambda e: self._on_quit())
		self.root.bind_all("<Command-q>", lambda e: self._on_quit())
		self.root.bind_all("<Command-Q>", lambda e: self._on_quit())

	def setup_single_conversion_tab(self, parent):
		"""Set up the single conversion tab"""
		# Configure grid weights
		parent.columnconfigure(1, weight=1)
		parent.rowconfigure(7, weight=1)

		# Title
		title_label = ttk.Label(
			parent, text="Single Image Converter", font=("Arial", 16, "bold")
		)
		title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

		# Input file selection
		ttk.Label(parent, text="Input File:").grid(row=1, column=0, sticky=tk.W, pady=5)
		input_entry = ttk.Entry(
			parent, textvariable=self.input_file_path, state="readonly", width=50
		)
		input_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
		browse_btn = ttk.Button(parent, text="Browse", command=self.browse_file)
		browse_btn.grid(row=1, column=2, padx=(5, 0), pady=5)

		# Output format selection
		ttk.Label(parent, text="Output Format:").grid(
			row=2, column=0, sticky=tk.W, pady=5
		)
		format_combo = ttk.Combobox(
			parent,
			textvariable=self.output_format,
			values=["png", "jpg", "jpeg", "bmp", "tiff", "gif", "webp", "pdf"],
			state="readonly",
			width=20,
		)
		format_combo.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)

		# Output directory selection
		output_dir_frame = ttk.Frame(parent)
		output_dir_frame.grid(
			row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5
		)
		output_dir_frame.columnconfigure(1, weight=1)

		ttk.Checkbutton(
			output_dir_frame,
			text="Custom output directory:",
			variable=self.use_custom_output_dir,
			command=self.toggle_output_directory,
		).grid(row=0, column=0, sticky=tk.W)

		self.output_dir_entry = ttk.Entry(
			output_dir_frame, textvariable=self.output_directory, state="disabled"
		)
		self.output_dir_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5))

		self.output_dir_btn = ttk.Button(
			output_dir_frame,
			text="Browse",
			command=self.browse_output_directory,
			state="disabled",
		)
		self.output_dir_btn.grid(row=0, column=2, padx=(5, 0))

		# Add suffix checkbox
		suffix_checkbox = ttk.Checkbutton(
			parent,
			text='Add "_converted" suffix to filename',
			variable=self.add_suffix,
		)
		suffix_checkbox.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=5)

		# Convert button
		self.convert_btn = ttk.Button(
			parent,
			text="Convert Image",
			command=self.convert_image,
			style="Accent.TButton",
		)
		self.convert_btn.grid(row=5, column=0, columnspan=3, pady=20)

		# Progress bar
		self.progress = ttk.Progressbar(parent, mode="indeterminate")
		self.progress.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

		# Status label
		self.status_label = ttk.Label(parent, text="Ready", foreground="green")
		self.status_label.grid(row=7, column=0, columnspan=3, pady=5, sticky=tk.N)

		# Output info frame
		info_frame = ttk.LabelFrame(parent, text="Conversion Info", padding="10")
		info_frame.grid(
			row=8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10
		)
		info_frame.columnconfigure(0, weight=1)
		parent.rowconfigure(8, weight=1)

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

	def setup_batch_conversion_tab(self, parent):
		"""Set up the batch conversion tab"""
		# Configure grid weights
		parent.columnconfigure(0, weight=1)
		parent.columnconfigure(1, weight=1)
		parent.rowconfigure(2, weight=1)

		# Title
		title_label = ttk.Label(
			parent, text="Batch Image Converter", font=("Arial", 16, "bold")
		)
		title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

		# Left panel - File list
		left_frame = ttk.LabelFrame(parent, text="Files to Convert", padding="10")
		left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
		left_frame.columnconfigure(0, weight=1)
		left_frame.rowconfigure(1, weight=1)

		# File list buttons
		btn_frame = ttk.Frame(left_frame)
		btn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
		btn_frame.columnconfigure(2, weight=1)

		ttk.Button(btn_frame, text="Add Files", command=self.add_files).grid(
			row=0, column=0, padx=(0, 5)
		)
		ttk.Button(btn_frame, text="Remove", command=self.remove_selected_files).grid(
			row=0, column=1, padx=(0, 5)
		)
		ttk.Button(btn_frame, text="Clear All", command=self.clear_file_list).grid(
			row=0, column=3
		)

		# File listbox
		list_frame = ttk.Frame(left_frame)
		list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
		list_frame.columnconfigure(0, weight=1)
		list_frame.rowconfigure(0, weight=1)

		self.file_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED)
		self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
		self.file_listbox.bind("<<ListboxSelect>>", self.on_file_select)

		file_scrollbar = ttk.Scrollbar(
			list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview
		)
		file_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
		self.file_listbox.configure(yscrollcommand=file_scrollbar.set)

		# Right panel - Preview and settings
		right_frame = ttk.Frame(parent)
		right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
		right_frame.columnconfigure(0, weight=1)
		right_frame.rowconfigure(0, weight=1)

		# Preview frame
		preview_frame = ttk.LabelFrame(right_frame, text="Preview", padding="10")
		preview_frame.grid(
			row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10)
		)
		preview_frame.columnconfigure(0, weight=1)
		preview_frame.rowconfigure(0, weight=1)

		self.preview_label = ttk.Label(
			preview_frame, text="Select a file to preview", anchor="center"
		)
		self.preview_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

		# Settings frame
		settings_frame = ttk.LabelFrame(
			right_frame, text="Batch Settings", padding="10"
		)
		settings_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

		# Output format
		ttk.Label(settings_frame, text="Output Format:").grid(
			row=0, column=0, sticky=tk.W, pady=5
		)
		batch_format_combo = ttk.Combobox(
			settings_frame,
			textvariable=self.output_format,
			values=["png", "jpg", "jpeg", "bmp", "tiff", "gif", "webp", "pdf"],
			state="readonly",
			width=15,
		)
		batch_format_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)

		# Output directory
		ttk.Checkbutton(
			settings_frame,
			text="Custom output directory:",
			variable=self.use_custom_output_dir,
			command=self.toggle_output_directory,
		).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)

		self.batch_output_dir_entry = ttk.Entry(
			settings_frame,
			textvariable=self.output_directory,
			state="disabled",
			width=30,
		)
		self.batch_output_dir_entry.grid(
			row=2, column=0, sticky=(tk.W, tk.E), padx=(0, 5), pady=5
		)

		self.batch_output_dir_btn = ttk.Button(
			settings_frame,
			text="Browse",
			command=self.browse_output_directory,
			state="disabled",
		)
		self.batch_output_dir_btn.grid(row=2, column=1, padx=(5, 0), pady=5)

		# Add suffix
		ttk.Checkbutton(
			settings_frame,
			text='Add "_converted" suffix',
			variable=self.add_suffix,
		).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)

		# Convert button
		self.batch_convert_btn = ttk.Button(
			settings_frame,
			text="Convert All Images",
			command=self.batch_convert_images,
			style="Accent.TButton",
		)
		self.batch_convert_btn.grid(row=4, column=0, columnspan=2, pady=20)

		# Progress and status for batch
		batch_progress_frame = ttk.Frame(parent)
		batch_progress_frame.grid(
			row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10
		)
		batch_progress_frame.columnconfigure(0, weight=1)

		self.batch_progress = ttk.Progressbar(batch_progress_frame, mode="determinate")
		self.batch_progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)

		self.batch_status_label = ttk.Label(
			batch_progress_frame, text="Ready for batch conversion", foreground="green"
		)
		self.batch_status_label.grid(row=1, column=0, pady=5)

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
			title="Select Image File", filetypes=file_types, initialdir=str(Path.home())
		)

		if filename:
			self.input_file_path.set(filename)
			self.log_message(f"Selected input file: {filename}")
			self.update_preview(filename)

	def toggle_output_directory(self):
		"""Toggle the output directory selection"""
		if self.use_custom_output_dir.get():
			self.output_dir_entry.config(state="normal")
			self.output_dir_btn.config(state="normal")
			if hasattr(self, "batch_output_dir_entry"):
				self.batch_output_dir_entry.config(state="normal")
				self.batch_output_dir_btn.config(state="normal")
		else:
			self.output_dir_entry.config(state="disabled")
			self.output_dir_btn.config(state="disabled")
			if hasattr(self, "batch_output_dir_entry"):
				self.batch_output_dir_entry.config(state="disabled")
				self.batch_output_dir_btn.config(state="disabled")

	def browse_output_directory(self):
		"""Browse for output directory"""
		directory = filedialog.askdirectory(title="Select Output Directory")
		if directory:
			self.output_directory.set(directory)

	def add_files(self):
		"""Add files to the batch conversion list"""
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

		filenames = filedialog.askopenfilenames(
			title="Select Image Files",
			filetypes=file_types,
			initialdir=str(Path.home()),
		)

		for filename in filenames:
			if filename not in self.file_list:
				self.file_list.append(filename)
				self.file_listbox.insert(tk.END, os.path.basename(filename))

		self.batch_status_label.config(
			text=f"Ready for batch conversion ({len(self.file_list)} files)",
			foreground="green",
		)

	def remove_selected_files(self):
		"""Remove selected files from the batch list"""
		selected_indices = self.file_listbox.curselection()
		for index in reversed(selected_indices):
			del self.file_list[index]
			self.file_listbox.delete(index)

		self.batch_status_label.config(
			text=f"Ready for batch conversion ({len(self.file_list)} files)",
			foreground="green",
		)

	def clear_file_list(self):
		"""Clear all files from the batch list"""
		self.file_list.clear()
		self.file_listbox.delete(0, tk.END)
		self.preview_label.config(text="Select a file to preview")
		self.current_preview_file = None
		self.batch_status_label.config(
			text="Ready for batch conversion", foreground="green"
		)

	def on_file_select(self, event):
		"""Handle file selection in the listbox"""
		selection = self.file_listbox.curselection()
		if selection:
			index = selection[0]
			if 0 <= index < len(self.file_list):
				selected_file = self.file_list[index]
				self.update_preview(selected_file)

	def update_preview(self, filename):
		"""Update the preview with file information (without external image libraries)"""
		if not filename or not os.path.exists(filename):
			self.preview_label.config(text="File not found")
			return

		self.current_preview_file = filename

		try:
			# Get file information
			file_path = Path(filename)
			file_size = os.path.getsize(filename)
			file_size_mb = file_size / (1024 * 1024)

			# Try to get image dimensions using ImageMagick identify command
			try:
				result = subprocess.run(
					["magick", "identify", "-format", "%wx%h", filename],
					capture_output=True,
					text=True,
					timeout=5,
				)
				if result.returncode == 0:
					dimensions = result.stdout.strip()
				else:
					# Try legacy identify command
					result = subprocess.run(
						["identify", "-format", "%wx%h", filename],
						capture_output=True,
						text=True,
						timeout=5,
					)
					dimensions = (
						result.stdout.strip() if result.returncode == 0 else "Unknown"
					)
			except (
				subprocess.CalledProcessError,
				FileNotFoundError,
				subprocess.TimeoutExpired,
			):
				dimensions = "Unknown"

			preview_text = f"File: {file_path.name}\n"
			preview_text += f"Size: {file_size_mb:.2f} MB\n"
			preview_text += f"Dimensions: {dimensions}\n"
			preview_text += f"Format: {file_path.suffix.upper().lstrip('.')}\n"
			preview_text += f"Path: {filename}"

			self.preview_label.config(text=preview_text, justify=tk.LEFT)

		except Exception as e:
			self.preview_label.config(text=f"Error reading file info:\n{str(e)}")

	def batch_convert_images(self):
		"""Convert all images in the batch list"""
		if self.is_converting:
			return

		if not self.file_list:
			messagebox.showerror("Error", "Please add files to convert")
			return

		# Start batch conversion in a separate thread
		self.is_converting = True
		self.batch_convert_btn.config(state="disabled", text="Converting...")
		self.batch_progress.config(
			mode="determinate", maximum=len(self.file_list), value=0
		)
		self.batch_status_label.config(text="Converting images...", foreground="orange")

		conversion_thread = threading.Thread(target=self._perform_batch_conversion)
		conversion_thread.daemon = True
		conversion_thread.start()

	def _perform_batch_conversion(self):
		"""Perform batch conversion (runs in separate thread)"""
		successful_conversions = 0
		failed_conversions = 0

		for i, input_path in enumerate(self.file_list):
			try:
				# Generate output filename
				input_file = Path(input_path)
				output_format = self.output_format.get().lower()

				# Determine output directory
				if self.use_custom_output_dir.get() and self.output_directory.get():
					output_dir = Path(self.output_directory.get())
				else:
					output_dir = input_file.parent

				if self.add_suffix.get():
					output_path = (
						output_dir / f"{input_file.stem}_converted.{output_format}"
					)
				else:
					output_path = output_dir / f"{input_file.stem}.{output_format}"

				self.root.after(
					0,
					self.log_message,
					f"Converting {i+1}/{len(self.file_list)}: {input_file.name}",
				)

				# Try conversion commands
				commands_to_try = [
					["magick", str(input_path), str(output_path)],
					["convert", str(input_path), str(output_path)],
				]

				success = False
				for cmd in commands_to_try:
					try:
						result = subprocess.run(
							cmd, capture_output=True, text=True, timeout=60
						)
						if result.returncode == 0:
							success = True
							break
						else:
							error_msg = (
								result.stderr.strip()
								if result.stderr
								else "Unknown error"
							)
							self.root.after(
								0,
								self.log_message,
								f"Command failed: {' '.join(cmd)} - {error_msg}",
							)
					except subprocess.TimeoutExpired:
						self.root.after(
							0, self.log_message, f"Command timed out: {' '.join(cmd)}"
						)
					except FileNotFoundError:
						self.root.after(
							0, self.log_message, f"Command not found: {cmd[0]}"
						)

				if success and os.path.exists(output_path):
					successful_conversions += 1
					self.root.after(
						0, self.log_message, f"✅ Success: {output_path.name}"
					)
				else:
					failed_conversions += 1
					self.root.after(
						0, self.log_message, f"❌ Failed: {input_file.name}"
					)

				# Update progress
				self.root.after(0, lambda i=i: self.batch_progress.config(value=i + 1))

			except Exception as e:
				failed_conversions += 1
				self.root.after(
					0, self.log_message, f"❌ Error converting {input_path}: {str(e)}"
				)

		# Conversion complete
		self.root.after(
			0,
			self._batch_conversion_complete,
			successful_conversions,
			failed_conversions,
		)

	def _batch_conversion_complete(self, successful, failed):
		"""Handle batch conversion completion (runs on main thread)"""
		self.is_converting = False
		self.batch_convert_btn.config(state="normal", text="Convert All Images")

		total = successful + failed
		if successful == total:
			self.batch_status_label.config(
				text=f"All {total} images converted successfully!", foreground="green"
			)
			messagebox.showinfo(
				"Success", f"All {total} images converted successfully!"
			)
		elif successful > 0:
			self.batch_status_label.config(
				text=f"{successful}/{total} images converted", foreground="orange"
			)
			messagebox.showwarning(
				"Partial Success",
				f"{successful} of {total} images converted successfully.\n{failed} failed.",
			)
		else:
			self.batch_status_label.config(
				text=f"All {total} conversions failed", foreground="red"
			)
			messagebox.showerror(
				"Error", f"All {total} conversions failed. Check the log for details."
			)

		self.log_message(
			f"Batch conversion complete: {successful} successful, {failed} failed"
		)

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

			# Determine output directory
			if self.use_custom_output_dir.get() and self.output_directory.get():
				output_dir = Path(self.output_directory.get())
			else:
				output_dir = input_file.parent

			if self.add_suffix.get():
				# Add "_converted" suffix
				output_path = (
					output_dir / f"{input_file.stem}_converted.{output_format}"
				)
			else:
				# Use original filename with new extension
				output_path = output_dir / f"{input_file.stem}.{output_format}"

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

	def _on_quit(self, event=None):
		"""Handle quit shortcut; confirm if a conversion is running."""
		if self.is_converting:
			# Ask user to confirm aborting an ongoing conversion
			quit_anyway = messagebox.askyesno(
				"Quit", "A conversion is in progress. Quit anyway?"
			)
			if not quit_anyway:
				return
		# Cleanly close the app
		try:
			self.root.destroy()
		except Exception:
			pass


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
