"""
Duplicate Finder View - Find and manage duplicate files
"""
import customtkinter as ctk
from tkinter import messagebox
import threading
from app.utils.duplicate_finder import DuplicateFinder
from app.services.file_service import FileService


class DuplicateFinderView(ctk.CTkFrame):
    """View for finding and managing duplicate files"""
    
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#f5f5f5")
        self.app = app
        self.duplicates = {}
        self.selected_for_deletion = set()
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create UI
        self.create_header()
        self.create_content()
    
    def create_header(self):
        """Create page header"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 10))
        
        title = ctk.CTkLabel(
            header_frame,
            text="🔍 Duplicate Finder",
            font=("Segoe UI", 28, "bold"),
            text_color="#2E86AB"
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Find and remove duplicate files to free up space",
            font=("Segoe UI", 14),
            text_color="#666"
        )
        subtitle.pack(anchor="w", pady=(5, 0))
    
    def create_content(self):
        """Create main content"""
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Controls section
        controls_frame = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=12)
        controls_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        controls_inner = ctk.CTkFrame(controls_frame, fg_color="transparent")
        controls_inner.pack(fill="x", padx=20, pady=15)
        
        # Scan button
        self.scan_btn = ctk.CTkButton(
            controls_inner,
            text="🔍 Scan for Duplicates",
            command=self.start_scan,
            fg_color="#2E86AB",
            hover_color="#1a5270",
            font=("Segoe UI", 14, "bold"),
            height=45,
            width=200
        )
        self.scan_btn.pack(side="left", padx=5)
        
        # Progress label
        self.progress_label = ctk.CTkLabel(
            controls_inner,
            text="",
            font=("Segoe UI", 12),
            text_color="#666"
        )
        self.progress_label.pack(side="left", padx=20)
        
        # Stats section
        self.stats_frame = ctk.CTkFrame(controls_inner, fg_color="transparent")
        self.stats_frame.pack(side="right")
        
        self.stats_label = ctk.CTkLabel(
            self.stats_frame,
            text="Click 'Scan' to find duplicates",
            font=("Segoe UI", 12),
            text_color="#666"
        )
        self.stats_label.pack()
        
        # Results section
        results_container = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=12)
        results_container.grid(row=1, column=0, sticky="nsew")
        results_container.grid_columnconfigure(0, weight=1)
        results_container.grid_rowconfigure(1, weight=1)
        
        # Results header
        results_header = ctk.CTkFrame(results_container, fg_color="#e8f4f8", height=50)
        results_header.grid(row=0, column=0, sticky="ew")
        results_header.grid_propagate(False)
        
        results_title = ctk.CTkLabel(
            results_header,
            text="Duplicate Groups",
            font=("Segoe UI", 14, "bold"),
            text_color="#2E86AB"
        )
        results_title.pack(side="left", padx=20, pady=15)
        
        # Delete selected button
        self.delete_btn = ctk.CTkButton(
            results_header,
            text="🗑️ Delete Selected",
            command=self.delete_selected,
            fg_color="#EF4444",
            hover_color="#dc2626",
            font=("Segoe UI", 12),
            height=35,
            state="disabled"
        )
        self.delete_btn.pack(side="right", padx=20, pady=10)
        
        # Results scroll area
        self.results_scroll = ctk.CTkScrollableFrame(
            results_container,
            fg_color="white"
        )
        self.results_scroll.grid(row=1, column=0, sticky="nsew")
        self.results_scroll.grid_columnconfigure(0, weight=1)
        
        # Initial message
        self.show_initial_message()
    
    def show_initial_message(self):
        """Show initial scan message"""
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
        
        msg = ctk.CTkLabel(
            self.results_scroll,
            text="🔍 Click 'Scan for Duplicates' to analyze your files",
            font=("Segoe UI", 14),
            text_color="#999"
        )
        msg.pack(pady=50)
    
    def start_scan(self):
        """Start duplicate scan in background thread"""
        self.scan_btn.configure(state="disabled", text="Scanning...")
        self.progress_label.configure(text="Initializing...")
        
        # Clear previous results
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
        
        self.duplicates = {}
        self.selected_for_deletion = set()
        
        # Start scan in thread
        thread = threading.Thread(target=self.perform_scan)
        thread.daemon = True
        thread.start()
    
    def perform_scan(self):
        """Perform the duplicate scan"""
        def progress_callback(current, total, filename):
            self.after(0, lambda: self.progress_label.configure(
                text=f"Scanning {current}/{total}: {filename[:30]}..."
            ))
        
        try:
            self.duplicates = DuplicateFinder.find_duplicates_in_database(progress_callback)
            self.after(0, self.display_results)
        except Exception as e:
            self.after(0, lambda: messagebox.showerror(
                "Scan Error",
                f"Error during scan: {str(e)}"
            ))
        finally:
            self.after(0, lambda: self.scan_btn.configure(
                state="normal",
                text="🔍 Scan for Duplicates"
            ))
    
    def display_results(self):
        """Display scan results"""
        # Clear scroll area
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
        
        if not self.duplicates:
            no_dupes = ctk.CTkLabel(
                self.results_scroll,
                text="✅ No duplicate files found!",
                font=("Segoe UI", 16),
                text_color="#6A994E"
            )
            no_dupes.pack(pady=50)
            
            self.stats_label.configure(text="No duplicates found")
            self.progress_label.configure(text="")
            return
        
        # Update stats
        stats = DuplicateFinder.get_duplicate_stats(self.duplicates)
        self.stats_label.configure(
            text=f"{stats['duplicate_groups']} groups • {stats['duplicate_files']} files • "
                 f"{stats['wasted_space_formatted']} can be freed"
        )
        self.progress_label.configure(text="Scan complete")
        
        # Display each duplicate group
        for group_idx, (file_hash, files) in enumerate(self.duplicates.items()):
            self.create_duplicate_group(group_idx + 1, files, file_hash[:8])
    
    def create_duplicate_group(self, group_num, files, hash_preview):
        """Create a duplicate group display"""
        group_frame = ctk.CTkFrame(
            self.results_scroll,
            fg_color="#f9f9f9",
            corner_radius=12
        )
        group_frame.pack(fill="x", padx=15, pady=8)
        group_frame.grid_columnconfigure(0, weight=1)
        
        # Group header
        header = ctk.CTkFrame(group_frame, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 10))
        
        header_label = ctk.CTkLabel(
            header,
            text=f"Group {group_num} ({len(files)} files)",
            font=("Segoe UI", 14, "bold"),
            text_color="#2E86AB"
        )
        header_label.pack(side="left")
        
        size_label = ctk.CTkLabel(
            header,
            text=files[0]['size_formatted'] if files else "",
            font=("Segoe UI", 12),
            text_color="#666"
        )
        size_label.pack(side="right")
        
        # File list
        for file_info in files:
            self.create_file_row(group_frame, file_info)
    
    def create_file_row(self, parent, file_info):
        """Create a file row in duplicate group"""
        row = ctk.CTkFrame(parent, fg_color="white", corner_radius=8)
        row.pack(fill="x", padx=10, pady=3)
        
        row_inner = ctk.CTkFrame(row, fg_color="transparent")
        row_inner.pack(fill="x", padx=10, pady=8)
        
        # Checkbox for selection
        var = ctk.StringVar(value="off")
        checkbox = ctk.CTkCheckBox(
            row_inner,
            text="",
            variable=var,
            onvalue="on",
            offvalue="off",
            command=lambda: self.toggle_file_selection(file_info['path'], var.get()),
            width=20
        )
        checkbox.pack(side="left", padx=(0, 10))
        
        # File icon and name
        icon_label = ctk.CTkLabel(
            row_inner,
            text="📄",
            font=("Segoe UI", 16)
        )
        icon_label.pack(side="left", padx=(0, 8))
        
        info_frame = ctk.CTkFrame(row_inner, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=file_info['name'],
            font=("Segoe UI", 12, "bold"),
            text_color="#333",
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        path_label = ctk.CTkLabel(
            info_frame,
            text=file_info['path'],
            font=("Segoe UI", 10),
            text_color="#999",
            anchor="w"
        )
        path_label.pack(anchor="w")
        
        # View button
        view_btn = ctk.CTkButton(
            row_inner,
            text="View",
            command=lambda: self.view_file(file_info),
            fg_color="#e8f4f8",
            text_color="#2E86AB",
            hover_color="#d0e8f0",
            font=("Segoe UI", 11),
            width=60,
            height=28
        )
        view_btn.pack(side="right", padx=5)
    
    def toggle_file_selection(self, file_path, state):
        """Toggle file selection for deletion"""
        if state == "on":
            self.selected_for_deletion.add(file_path)
        else:
            self.selected_for_deletion.discard(file_path)
        
        # Update delete button state
        if self.selected_for_deletion:
            self.delete_btn.configure(
                state="normal",
                text=f"🗑️ Delete Selected ({len(self.selected_for_deletion)})"
            )
        else:
            self.delete_btn.configure(
                state="disabled",
                text="🗑️ Delete Selected"
            )
    
    def view_file(self, file_info):
        """View file details"""
        file = FileService.get_file_by_id(file_info['id'])
        if file:
            self.app.show_file_detail(file)
    
    def delete_selected(self):
        """Delete selected duplicate files"""
        if not self.selected_for_deletion:
            return
        
        count = len(self.selected_for_deletion)
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete {count} file(s)?\n\n"
            "This action cannot be undone!"
        )
        
        if not confirm:
            return
        
        deleted = 0
        errors = []
        
        for file_path in list(self.selected_for_deletion):
            try:
                import os
                if os.path.exists(file_path):
                    os.remove(file_path)
                    deleted += 1
                    
                    # Remove from database
                    from app.models import File, get_session
                    session = get_session()
                    file_record = session.query(File).filter_by(path=file_path).first()
                    if file_record:
                        session.delete(file_record)
                        session.commit()
            except Exception as e:
                errors.append(f"{file_path}: {str(e)}")
        
        # Show result
        if errors:
            messagebox.showwarning(
                "Deletion Complete",
                f"Deleted {deleted} files.\n\nErrors:\n" + "\n".join(errors[:5])
            )
        else:
            messagebox.showinfo(
                "Deletion Complete",
                f"Successfully deleted {deleted} files!"
            )
        
        # Refresh results
        self.selected_for_deletion.clear()
        self.start_scan()
