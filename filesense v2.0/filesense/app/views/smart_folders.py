"""
Smart Folders View - Configure and manage watched folders
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
import os
from pathlib import Path
from app.services.file_watcher import FileWatcher, WatchedFolder


class SmartFoldersView(ctk.CTkFrame):
    """View for managing smart/watched folders"""
    
    CONFIG_FILE = os.path.expanduser("~/.filesense/smart_folders.json")
    
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#f5f5f5")
        self.app = app
        self.watched_folders = []
        self.watcher = FileWatcher()
        
        # Set up watcher callbacks
        self.watcher.on_file_created = self.on_file_created
        self.watcher.on_file_modified = self.on_file_modified
        self.watcher.on_file_deleted = self.on_file_deleted
        
        # Activity log
        self.activity_log = []
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Load saved configuration
        self.load_config()
        
        self.create_header()
        self.create_content()
        
        # Start watcher if any folders are enabled
        self.start_watching()
    
    def create_header(self):
        """Create page header"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 10))
        
        title = ctk.CTkLabel(
            header_frame,
            text="📁 Smart Folders",
            font=("Segoe UI", 28, "bold"),
            text_color="#2E86AB"
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Automatically monitor folders for new and changed files",
            font=("Segoe UI", 14),
            text_color="#666"
        )
        subtitle.pack(anchor="w", pady=(5, 0))
    
    def create_content(self):
        """Create main content"""
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)
        
        # Left side - Folder list
        left_frame = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=1)
        
        # Folder list header
        header = ctk.CTkFrame(left_frame, fg_color="#e8f4f8", corner_radius=12)
        header.grid(row=0, column=0, sticky="ew")
        
        header_title = ctk.CTkLabel(
            header,
            text="Watched Folders",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E86AB"
        )
        header_title.pack(side="left", padx=20, pady=15)
        
        add_btn = ctk.CTkButton(
            header,
            text="+ Add Folder",
            command=self.add_folder,
            fg_color="#6A994E",
            hover_color="#5a8440",
            font=("Segoe UI", 12),
            width=120,
            height=35
        )
        add_btn.pack(side="right", padx=15, pady=10)
        
        # Folder list scroll
        self.folder_scroll = ctk.CTkScrollableFrame(
            left_frame,
            fg_color="transparent"
        )
        self.folder_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.folder_scroll.grid_columnconfigure(0, weight=1)
        
        # Refresh folder display
        self.refresh_folder_list()
        
        # Right side - Activity & Status
        right_frame = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)
        
        # Status section
        status_header = ctk.CTkFrame(right_frame, fg_color="#e8f4f8", corner_radius=12)
        status_header.grid(row=0, column=0, sticky="ew")
        
        status_title = ctk.CTkLabel(
            status_header,
            text="Watcher Status",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E86AB"
        )
        status_title.pack(side="left", padx=20, pady=15)
        
        self.status_indicator = ctk.CTkLabel(
            status_header,
            text="● Stopped",
            font=("Segoe UI", 12),
            text_color="#EF4444"
        )
        self.status_indicator.pack(side="right", padx=20, pady=15)
        
        # Controls
        controls = ctk.CTkFrame(right_frame, fg_color="transparent")
        controls.grid(row=1, column=0, sticky="new", padx=15, pady=15)
        
        self.toggle_btn = ctk.CTkButton(
            controls,
            text="▶ Start Watching",
            command=self.toggle_watcher,
            fg_color="#6A994E",
            font=("Segoe UI", 13, "bold"),
            height=45,
            width=180
        )
        self.toggle_btn.pack(pady=(0, 10))
        
        # Activity log
        activity_frame = ctk.CTkFrame(right_frame, fg_color="#f9f9f9", corner_radius=8)
        activity_frame.grid(row=2, column=0, sticky="nsew", padx=15, pady=(0, 15))
        activity_frame.grid_columnconfigure(0, weight=1)
        activity_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_rowconfigure(2, weight=1)
        
        activity_title = ctk.CTkLabel(
            activity_frame,
            text="Recent Activity",
            font=("Segoe UI", 13, "bold"),
            text_color="#2E86AB"
        )
        activity_title.pack(padx=15, pady=(10, 5), anchor="w")
        
        self.activity_scroll = ctk.CTkScrollableFrame(
            activity_frame,
            fg_color="transparent",
            height=200
        )
        self.activity_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Initial no activity message
        self.no_activity = ctk.CTkLabel(
            self.activity_scroll,
            text="No activity yet",
            font=("Segoe UI", 11),
            text_color="#999"
        )
        self.no_activity.pack(pady=20)
    
    def refresh_folder_list(self):
        """Refresh the folder list display"""
        for widget in self.folder_scroll.winfo_children():
            widget.destroy()
        
        if not self.watched_folders:
            no_folders = ctk.CTkLabel(
                self.folder_scroll,
                text="No folders being watched.\nClick 'Add Folder' to start.",
                font=("Segoe UI", 12),
                text_color="#999",
                justify="center"
            )
            no_folders.pack(pady=50)
            return
        
        for i, folder in enumerate(self.watched_folders):
            self.create_folder_card(folder, i)
    
    def create_folder_card(self, folder: WatchedFolder, index: int):
        """Create a folder card"""
        card = ctk.CTkFrame(
            self.folder_scroll,
            fg_color="#f9f9f9" if folder.enabled else "#f0f0f0",
            corner_radius=10
        )
        card.pack(fill="x", pady=5)
        
        # Main content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=12)
        
        # Enabled toggle
        enabled_var = ctk.StringVar(value="on" if folder.enabled else "off")
        toggle = ctk.CTkSwitch(
            content,
            text="",
            variable=enabled_var,
            onvalue="on",
            offvalue="off",
            command=lambda: self.toggle_folder(index, enabled_var.get()),
            width=50
        )
        toggle.pack(side="left", padx=(0, 10))
        
        # Folder info
        info = ctk.CTkFrame(content, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)
        
        # Folder icon and name
        folder_name = os.path.basename(folder.path) or folder.path
        name_label = ctk.CTkLabel(
            info,
            text=f"📂 {folder_name}",
            font=("Segoe UI", 13, "bold"),
            text_color="#2E86AB" if folder.enabled else "#999",
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        path_label = ctk.CTkLabel(
            info,
            text=folder.path,
            font=("Segoe UI", 10),
            text_color="#666" if folder.enabled else "#999",
            anchor="w"
        )
        path_label.pack(anchor="w")
        
        # Options display
        options = []
        if folder.recursive:
            options.append("Recursive")
        if folder.extensions:
            options.append(f"Types: {', '.join(folder.extensions[:3])}")
        if folder.auto_tag:
            options.append("Auto-tag")
        
        if options:
            options_label = ctk.CTkLabel(
                info,
                text=" • ".join(options),
                font=("Segoe UI", 10),
                text_color="#999",
                anchor="w"
            )
            options_label.pack(anchor="w", pady=(2, 0))
        
        # Action buttons
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(side="right")
        
        edit_btn = ctk.CTkButton(
            btn_frame,
            text="⚙",
            command=lambda: self.edit_folder(index),
            fg_color="#e8f4f8",
            text_color="#2E86AB",
            hover_color="#d0e8f0",
            width=35,
            height=35,
            corner_radius=8
        )
        edit_btn.pack(side="left", padx=2)
        
        delete_btn = ctk.CTkButton(
            btn_frame,
            text="🗑",
            command=lambda: self.remove_folder(index),
            fg_color="#fee2e2",
            text_color="#EF4444",
            hover_color="#fecaca",
            width=35,
            height=35,
            corner_radius=8
        )
        delete_btn.pack(side="left", padx=2)
    
    def add_folder(self):
        """Add a new watched folder"""
        folder_path = filedialog.askdirectory(title="Select Folder to Watch")
        if not folder_path:
            return
        
        # Check if already watching
        for f in self.watched_folders:
            if f.path == folder_path:
                messagebox.showwarning("Already Watching", "This folder is already being watched.")
                return
        
        # Show configuration dialog
        self.show_folder_config_dialog(folder_path)
    
    def show_folder_config_dialog(self, folder_path: str, existing_index: int = None):
        """Show folder configuration dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Configure Watched Folder")
        dialog.geometry("450x400")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - 450) // 2
        y = self.winfo_rooty() + (self.winfo_height() - 400) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Get existing config if editing
        existing = self.watched_folders[existing_index] if existing_index is not None else None
        
        # Content
        content = ctk.CTkFrame(dialog, fg_color="#f5f5f5")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Path
        path_label = ctk.CTkLabel(
            content,
            text="Folder Path:",
            font=("Segoe UI", 12, "bold"),
            text_color="#2E86AB"
        )
        path_label.pack(anchor="w", pady=(0, 5))
        
        path_entry = ctk.CTkEntry(content, height=35)
        path_entry.pack(fill="x", pady=(0, 15))
        path_entry.insert(0, folder_path)
        path_entry.configure(state="disabled")
        
        # Options
        recursive_var = ctk.StringVar(value="on" if (existing is None or existing.recursive) else "off")
        recursive_cb = ctk.CTkCheckBox(
            content,
            text="Include subfolders (recursive)",
            variable=recursive_var,
            onvalue="on",
            offvalue="off"
        )
        recursive_cb.pack(anchor="w", pady=5)
        
        auto_tag_var = ctk.StringVar(value="on" if (existing and existing.auto_tag) else "off")
        auto_tag_cb = ctk.CTkCheckBox(
            content,
            text="Auto-tag new files with AI",
            variable=auto_tag_var,
            onvalue="on",
            offvalue="off"
        )
        auto_tag_cb.pack(anchor="w", pady=5)
        
        # Extensions filter
        ext_label = ctk.CTkLabel(
            content,
            text="File extensions to include (comma-separated, leave empty for all):",
            font=("Segoe UI", 11),
            text_color="#666"
        )
        ext_label.pack(anchor="w", pady=(15, 5))
        
        ext_entry = ctk.CTkEntry(content, placeholder_text=".txt, .pdf, .docx", height=35)
        ext_entry.pack(fill="x", pady=(0, 15))
        
        if existing and existing.extensions:
            ext_entry.insert(0, ", ".join(existing.extensions))
        
        # Buttons
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(20, 0))
        
        def save():
            # Parse extensions
            ext_text = ext_entry.get().strip()
            extensions = []
            if ext_text:
                extensions = [e.strip().lower() for e in ext_text.split(",")]
                extensions = [e if e.startswith('.') else f'.{e}' for e in extensions if e]
            
            folder = WatchedFolder(
                path=folder_path,
                recursive=recursive_var.get() == "on",
                extensions=extensions,
                auto_tag=auto_tag_var.get() == "on"
            )
            
            if existing_index is not None:
                self.watched_folders[existing_index] = folder
            else:
                self.watched_folders.append(folder)
            
            self.save_config()
            self.refresh_folder_list()
            self.restart_watching()
            dialog.destroy()
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            fg_color="white",
            text_color="#666",
            border_width=2,
            border_color="#ddd",
            width=100
        )
        cancel_btn.pack(side="left")
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Save",
            command=save,
            fg_color="#2E86AB",
            width=100
        )
        save_btn.pack(side="right")
    
    def edit_folder(self, index: int):
        """Edit a watched folder"""
        folder = self.watched_folders[index]
        self.show_folder_config_dialog(folder.path, index)
    
    def remove_folder(self, index: int):
        """Remove a watched folder"""
        confirm = messagebox.askyesno(
            "Remove Folder",
            "Stop watching this folder?"
        )
        
        if confirm:
            del self.watched_folders[index]
            self.save_config()
            self.refresh_folder_list()
            self.restart_watching()
    
    def toggle_folder(self, index: int, state: str):
        """Toggle folder enabled state"""
        self.watched_folders[index].enabled = state == "on"
        self.save_config()
        self.refresh_folder_list()
        self.restart_watching()
    
    def toggle_watcher(self):
        """Toggle watcher on/off"""
        if self.watcher.running:
            self.stop_watching()
        else:
            self.start_watching()
    
    def start_watching(self):
        """Start the file watcher"""
        # Add enabled folders to watcher
        for folder in self.watched_folders:
            if folder.enabled:
                self.watcher.add_folder(folder.path)
        
        if self.watcher.watched_folders:
            self.watcher.start()
            self.status_indicator.configure(
                text="● Watching",
                text_color="#6A994E"
            )
            self.toggle_btn.configure(
                text="⏹ Stop Watching",
                fg_color="#EF4444",
                hover_color="#dc2626"
            )
    
    def stop_watching(self):
        """Stop the file watcher"""
        self.watcher.stop()
        self.status_indicator.configure(
            text="● Stopped",
            text_color="#EF4444"
        )
        self.toggle_btn.configure(
            text="▶ Start Watching",
            fg_color="#6A994E",
            hover_color="#5a8440"
        )
    
    def restart_watching(self):
        """Restart watcher with updated folders"""
        self.stop_watching()
        self.watcher.watched_folders.clear()
        self.start_watching()
    
    def on_file_created(self, file_path: str):
        """Handle new file event"""
        self.log_activity("created", file_path)
        
        # Auto-import if configured
        for folder in self.watched_folders:
            if file_path.startswith(folder.path) and folder.enabled:
                if folder.should_include(file_path):
                    from app.services.file_service import FileService
                    FileService.import_file(file_path)
    
    def on_file_modified(self, file_path: str):
        """Handle file modified event"""
        self.log_activity("modified", file_path)
    
    def on_file_deleted(self, file_path: str):
        """Handle file deleted event"""
        self.log_activity("deleted", file_path)
    
    def log_activity(self, event_type: str, file_path: str):
        """Log activity to UI"""
        from datetime import datetime
        
        self.activity_log.append({
            'type': event_type,
            'path': file_path,
            'time': datetime.now()
        })
        
        # Keep only last 50 entries
        self.activity_log = self.activity_log[-50:]
        
        # Update UI (schedule on main thread)
        self.after(0, self.refresh_activity_log)
    
    def refresh_activity_log(self):
        """Refresh activity log display"""
        for widget in self.activity_scroll.winfo_children():
            widget.destroy()
        
        if not self.activity_log:
            self.no_activity = ctk.CTkLabel(
                self.activity_scroll,
                text="No activity yet",
                font=("Segoe UI", 11),
                text_color="#999"
            )
            self.no_activity.pack(pady=20)
            return
        
        # Show recent activities (newest first)
        for activity in reversed(self.activity_log[-20:]):
            row = ctk.CTkFrame(self.activity_scroll, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            # Icon based on type
            icons = {
                'created': '➕',
                'modified': '✏️',
                'deleted': '🗑️'
            }
            colors = {
                'created': '#6A994E',
                'modified': '#FF9800',
                'deleted': '#EF4444'
            }
            
            icon = ctk.CTkLabel(
                row,
                text=icons.get(activity['type'], '•'),
                font=("Segoe UI", 12),
                width=25
            )
            icon.pack(side="left")
            
            filename = os.path.basename(activity['path'])
            file_label = ctk.CTkLabel(
                row,
                text=filename[:30] + ('...' if len(filename) > 30 else ''),
                font=("Segoe UI", 11),
                text_color=colors.get(activity['type'], '#666'),
                anchor="w"
            )
            file_label.pack(side="left", fill="x", expand=True)
            
            time_str = activity['time'].strftime("%H:%M:%S")
            time_label = ctk.CTkLabel(
                row,
                text=time_str,
                font=("Segoe UI", 10),
                text_color="#999"
            )
            time_label.pack(side="right")
    
    def save_config(self):
        """Save configuration to file"""
        config_dir = os.path.dirname(self.CONFIG_FILE)
        os.makedirs(config_dir, exist_ok=True)
        
        data = [f.to_dict() for f in self.watched_folders]
        
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_config(self):
        """Load configuration from file"""
        if not os.path.exists(self.CONFIG_FILE):
            return
        
        try:
            with open(self.CONFIG_FILE, 'r') as f:
                data = json.load(f)
            
            self.watched_folders = [WatchedFolder.from_dict(d) for d in data]
        except Exception as e:
            print(f"Error loading config: {e}")
    
    def destroy(self):
        """Clean up when view is destroyed"""
        self.stop_watching()
        super().destroy()
