"""
File Browser View - Browse and organize files
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from pathlib import Path
from app.services.file_service import FileService


class FileBrowserView(ctk.CTkFrame):
    """File browser view with folder navigation"""
    
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#f5f5f5")
        self.app = app
        self.current_files = []
        self.selected_files = []
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create header
        self.create_header()
        
        # Create content
        self.create_content()
        
        # Load files
        self.refresh_files()
    
    def create_header(self):
        """Create page header"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 10))
        
        title = ctk.CTkLabel(
            header_frame,
            text="File Browser",
            font=("Segoe UI", 28, "bold"),
            text_color="#2E86AB"
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Browse and manage your files",
            font=("Segoe UI", 14),
            text_color="#666"
        )
        subtitle.pack(anchor="w", pady=(5, 0))
    
    def create_content(self):
        """Create browser content"""
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Toolbar
        toolbar = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=12)
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        toolbar_inner = ctk.CTkFrame(toolbar, fg_color="transparent")
        toolbar_inner.pack(fill="x", padx=15, pady=12)
        
        # Scan folder button
        scan_btn = ctk.CTkButton(
            toolbar_inner,
            text="📂 Scan Folder",
            command=self.scan_folder,
            fg_color="#2E86AB",
            hover_color="#1a5270",
            font=("Segoe UI", 14),
            height=40,
            width=150
        )
        scan_btn.pack(side="left", padx=5)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            toolbar_inner,
            text="🔄 Refresh",
            command=self.refresh_files,
            fg_color="white",
            text_color="#2E86AB",
            border_width=2,
            border_color="#2E86AB",
            hover_color="#e8f4f8",
            font=("Segoe UI", 14),
            height=40,
            width=120
        )
        refresh_btn.pack(side="left", padx=5)
        
        # View mode buttons
        view_frame = ctk.CTkFrame(toolbar_inner, fg_color="transparent")
        view_frame.pack(side="right")
        
        list_btn = ctk.CTkButton(
            view_frame,
            text="📋 List",
            command=lambda: self.set_view_mode("list"),
            fg_color="#FFD93D",
            text_color="#2E86AB",
            font=("Segoe UI", 13),
            height=36,
            width=80
        )
        list_btn.pack(side="left", padx=2)
        
        # File list
        list_frame = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=12)
        list_frame.grid(row=1, column=0, sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        
        # Header row
        header_row = ctk.CTkFrame(list_frame, fg_color="#e8f4f8", height=45)
        header_row.grid(row=0, column=0, sticky="ew")
        header_row.grid_columnconfigure(0, weight=2)
        header_row.grid_columnconfigure(1, weight=1)
        header_row.grid_columnconfigure(2, weight=1)
        header_row.grid_columnconfigure(3, weight=1)
        header_row.grid_propagate(False)
        
        headers = ["Name", "Type", "Size", "Modified"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                header_row,
                text=header,
                font=("Segoe UI", 13, "bold"),
                text_color="#2E86AB"
            )
            label.grid(row=0, column=i, sticky="w", padx=15, pady=10)
        
        # Scrollable file list
        self.files_scroll = ctk.CTkScrollableFrame(
            list_frame,
            fg_color="white"
        )
        self.files_scroll.grid(row=1, column=0, sticky="nsew")
        self.files_scroll.grid_columnconfigure(0, weight=1)
        
        # Action bar
        action_bar = ctk.CTkFrame(list_frame, fg_color="#f5f5f5", height=60)
        action_bar.grid(row=2, column=0, sticky="ew")
        action_bar.grid_propagate(False)
        
        action_frame = ctk.CTkFrame(action_bar, fg_color="transparent")
        action_frame.pack(expand=True, fill="x", padx=15, pady=10)
        
        # Selection info
        self.selection_label = ctk.CTkLabel(
            action_frame,
            text="0 files selected",
            font=("Segoe UI", 12),
            text_color="#666"
        )
        self.selection_label.pack(side="left")
        
        # Action buttons
        batch_btn = ctk.CTkButton(
            action_frame,
            text="Batch Tag",
            command=self.batch_tag,
            fg_color="#2E86AB",
            font=("Segoe UI", 13),
            height=36,
            width=120
        )
        batch_btn.pack(side="right", padx=2)
        
        ai_btn = ctk.CTkButton(
            action_frame,
            text="AI Analyze",
            command=self.ai_analyze_selected,
            fg_color="#6A994E",
            font=("Segoe UI", 13),
            height=36,
            width=120
        )
        ai_btn.pack(side="right", padx=2)
    
    def set_view_mode(self, mode):
        """Set view mode (list/grid)"""
        # Currently only list mode implemented
        pass
    
    def scan_folder(self):
        """Scan a folder and add files to database"""
        folder = filedialog.askdirectory(title="Select Folder to Scan")
        if folder:
            # Progress dialog
            progress_window = ctk.CTkToplevel(self)
            progress_window.title("Scanning Folder")
            progress_window.geometry("400x150")
            progress_window.transient(self)
            progress_window.grab_set()
            
            label = ctk.CTkLabel(
                progress_window,
                text="Scanning files...",
                font=("Segoe UI", 14)
            )
            label.pack(pady=20)
            
            progress = ctk.CTkProgressBar(progress_window, width=350)
            progress.pack(pady=10)
            progress.set(0)
            
            status_label = ctk.CTkLabel(
                progress_window,
                text="",
                font=("Segoe UI", 11)
            )
            status_label.pack(pady=5)
            
            def update_progress(current, total, filename):
                if total > 0:
                    progress.set(current / total)
                status_label.configure(text=f"Processing: {filename}")
                progress_window.update()
            
            # Scan in background
            try:
                added_files = FileService.scan_folder(folder, update_progress)
                progress_window.destroy()
                
                messagebox.showinfo(
                    "Scan Complete",
                    f"Added {len(added_files)} files to database!"
                )
                
                self.refresh_files()
            except Exception as e:
                progress_window.destroy()
                messagebox.showerror("Error", f"Failed to scan folder: {str(e)}")
    
    def refresh_files(self):
        """Refresh file list"""
        # Clear current list
        for widget in self.files_scroll.winfo_children():
            widget.destroy()
        
        # Get all files
        self.current_files = FileService.get_all_files()
        
        if not self.current_files:
            no_files = ctk.CTkLabel(
                self.files_scroll,
                text="No files in database. Click 'Scan Folder' to add files.",
                font=("Segoe UI", 13),
                text_color="#999"
            )
            no_files.pack(pady=50)
            return
        
        # Create file rows
        for file in self.current_files:
            self.create_file_row(file)
    
    def create_file_row(self, file):
        """Create a file row in the list"""
        row = ctk.CTkFrame(self.files_scroll, fg_color="transparent")
        row.pack(fill="x", pady=1)
        row.grid_columnconfigure(0, weight=2)
        row.grid_columnconfigure(1, weight=1)
        row.grid_columnconfigure(2, weight=1)
        row.grid_columnconfigure(3, weight=1)
        
        # Hover effect
        row.bind("<Enter>", lambda e: row.configure(fg_color="#f9f9f9"))
        row.bind("<Leave>", lambda e: row.configure(fg_color="transparent"))
        
        # Checkbox and name
        name_frame = ctk.CTkFrame(row, fg_color="transparent")
        name_frame.grid(row=0, column=0, sticky="w", padx=15, pady=8)
        
        checkbox_var = tk.BooleanVar()
        checkbox = ctk.CTkCheckBox(
            name_frame,
            text="",
            variable=checkbox_var,
            command=lambda: self.toggle_selection(file, checkbox_var.get()),
            width=20
        )
        checkbox.pack(side="left", padx=(0, 10))
        
        icon_label = ctk.CTkLabel(
            name_frame,
            text=file.file_type_icon,
            font=("Segoe UI", 16)
        )
        icon_label.pack(side="left", padx=(0, 8))
        
        name_label = ctk.CTkLabel(
            name_frame,
            text=file.name,
            font=("Segoe UI", 12),
            text_color="#2E86AB",
            anchor="w",
            cursor="hand2"
        )
        name_label.pack(side="left")
        name_label.bind("<Button-1>", lambda e: self.app.show_file_detail(file))
        
        # Type
        type_label = ctk.CTkLabel(
            row,
            text=file.file_type_name,
            font=("Segoe UI", 11),
            text_color="#666"
        )
        type_label.grid(row=0, column=1, sticky="w", padx=15)
        
        # Size
        size_label = ctk.CTkLabel(
            row,
            text=file.size_formatted,
            font=("Segoe UI", 11),
            text_color="#666"
        )
        size_label.grid(row=0, column=2, sticky="w", padx=15)
        
        # Modified
        modified_label = ctk.CTkLabel(
            row,
            text=file.modified_time_ago,
            font=("Segoe UI", 11),
            text_color="#666"
        )
        modified_label.grid(row=0, column=3, sticky="w", padx=15)
    
    def toggle_selection(self, file, selected):
        """Toggle file selection"""
        if selected:
            if file not in self.selected_files:
                self.selected_files.append(file)
        else:
            if file in self.selected_files:
                self.selected_files.remove(file)
        
        self.update_selection_label()
    
    def update_selection_label(self):
        """Update selection count label"""
        count = len(self.selected_files)
        self.selection_label.configure(
            text=f"{count} file{'s' if count != 1 else ''} selected"
        )
    
    def batch_tag(self):
        """Batch tag selected files"""
        if not self.selected_files:
            messagebox.showwarning("No Selection", "Please select files first")
            return
        
        # TODO: Show batch tag dialog
        messagebox.showinfo("Batch Tag", f"Would tag {len(self.selected_files)} files")
    
    def ai_analyze_selected(self):
        """AI analyze selected files"""
        if not self.selected_files:
            messagebox.showwarning("No Selection", "Please select files first")
            return
        
        if len(self.selected_files) == 1:
            self.app.show_ai(self.selected_files[0])
        else:
            messagebox.showinfo("AI Analysis", "Multi-file AI analysis coming soon!")
