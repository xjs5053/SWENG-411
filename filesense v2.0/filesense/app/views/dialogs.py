"""
Dialog Components - Tag Editor, File Preview, and other dialogs
"""
import customtkinter as ctk
from tkinter import messagebox
import os
from typing import List, Callable, Optional
from app.services.file_service import FileService
from app.utils.content_reader import ContentReader


class TagEditorDialog(ctk.CTkToplevel):
    """Dialog for editing file tags"""
    
    def __init__(self, parent, file, on_save: Optional[Callable] = None):
        super().__init__(parent)
        
        self.file = file
        self.on_save = on_save
        self.selected_tags = set(file.tag_list)
        
        # Configure window
        self.title(f"Edit Tags - {file.name}")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Center on parent
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - 500) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - 600) // 2
        self.geometry(f"+{x}+{y}")
        
        # Create UI
        self.create_ui()
    
    def create_ui(self):
        """Create dialog UI"""
        # Header
        header = ctk.CTkFrame(self, fg_color="#2E86AB", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header,
            text=f"🏷️ Edit Tags",
            font=("Segoe UI", 20, "bold"),
            text_color="white"
        )
        title.pack(pady=15)
        
        filename = ctk.CTkLabel(
            header,
            text=self.file.name,
            font=("Segoe UI", 12),
            text_color="#e0e0e0"
        )
        filename.pack()
        
        # Content
        content = ctk.CTkFrame(self, fg_color="#f5f5f5")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add new tag section
        add_frame = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        add_frame.pack(fill="x", pady=(0, 15))
        
        add_title = ctk.CTkLabel(
            add_frame,
            text="Add New Tag",
            font=("Segoe UI", 14, "bold"),
            text_color="#2E86AB"
        )
        add_title.pack(padx=15, pady=(15, 10), anchor="w")
        
        add_input_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        add_input_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.tag_entry = ctk.CTkEntry(
            add_input_frame,
            placeholder_text="Enter tag name...",
            height=40,
            font=("Segoe UI", 13)
        )
        self.tag_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.tag_entry.bind('<Return>', lambda e: self.add_tag())
        
        add_btn = ctk.CTkButton(
            add_input_frame,
            text="+ Add",
            command=self.add_tag,
            fg_color="#6A994E",
            hover_color="#5a8440",
            font=("Segoe UI", 13),
            width=80,
            height=40
        )
        add_btn.pack(side="right")
        
        # Current tags section
        tags_frame = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        tags_frame.pack(fill="both", expand=True)
        
        tags_title = ctk.CTkLabel(
            tags_frame,
            text="Current Tags",
            font=("Segoe UI", 14, "bold"),
            text_color="#2E86AB"
        )
        tags_title.pack(padx=15, pady=(15, 10), anchor="w")
        
        # Tags scroll area
        self.tags_scroll = ctk.CTkScrollableFrame(
            tags_frame,
            fg_color="transparent"
        )
        self.tags_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Display current tags
        self.refresh_tags()
        
        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self.destroy,
            fg_color="white",
            text_color="#2E86AB",
            border_width=2,
            border_color="#2E86AB",
            hover_color="#e8f4f8",
            font=("Segoe UI", 14),
            width=120,
            height=40
        )
        cancel_btn.pack(side="left")
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Save Changes",
            command=self.save_tags,
            fg_color="#2E86AB",
            hover_color="#1a5270",
            font=("Segoe UI", 14, "bold"),
            width=140,
            height=40
        )
        save_btn.pack(side="right")
    
    def refresh_tags(self):
        """Refresh tags display"""
        for widget in self.tags_scroll.winfo_children():
            widget.destroy()
        
        if not self.selected_tags:
            no_tags = ctk.CTkLabel(
                self.tags_scroll,
                text="No tags yet",
                font=("Segoe UI", 12),
                text_color="#999"
            )
            no_tags.pack(pady=20)
            return
        
        for tag in sorted(self.selected_tags):
            self.create_tag_chip(tag)
    
    def create_tag_chip(self, tag_name):
        """Create a tag chip with remove button"""
        chip = ctk.CTkFrame(self.tags_scroll, fg_color="#C7F0BD", corner_radius=20)
        chip.pack(anchor="w", pady=3)
        
        tag_label = ctk.CTkLabel(
            chip,
            text=f"#{tag_name}",
            font=("Segoe UI", 12),
            text_color="#2E86AB"
        )
        tag_label.pack(side="left", padx=(15, 5), pady=8)
        
        remove_btn = ctk.CTkButton(
            chip,
            text="✕",
            command=lambda: self.remove_tag(tag_name),
            fg_color="transparent",
            text_color="#666",
            hover_color="#aae09e",
            font=("Segoe UI", 12),
            width=25,
            height=25
        )
        remove_btn.pack(side="right", padx=(0, 5), pady=5)
    
    def add_tag(self):
        """Add a new tag"""
        tag_name = self.tag_entry.get().strip()
        
        if not tag_name:
            return
        
        # Clean tag name
        tag_name = tag_name.lower().replace(' ', '-')
        tag_name = ''.join(c for c in tag_name if c.isalnum() or c == '-')
        
        if len(tag_name) > 30:
            tag_name = tag_name[:30]
        
        if tag_name and tag_name not in self.selected_tags:
            self.selected_tags.add(tag_name)
            self.refresh_tags()
        
        self.tag_entry.delete(0, 'end')
    
    def remove_tag(self, tag_name):
        """Remove a tag"""
        self.selected_tags.discard(tag_name)
        self.refresh_tags()
    
    def save_tags(self):
        """Save tags to file"""
        try:
            # Get current tags from database
            current_tags = set(self.file.tag_list)
            
            # Find tags to add and remove
            tags_to_add = self.selected_tags - current_tags
            tags_to_remove = current_tags - self.selected_tags
            
            # Remove old tags
            for tag in tags_to_remove:
                FileService.remove_tag_from_file(self.file.id, tag)
            
            # Add new tags
            if tags_to_add:
                FileService.add_tags_to_file(self.file.id, list(tags_to_add))
            
            messagebox.showinfo("Success", "Tags saved successfully!")
            
            if self.on_save:
                self.on_save()
            
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tags: {str(e)}")


class FilePreviewDialog(ctk.CTkToplevel):
    """Dialog for previewing file contents"""
    
    def __init__(self, parent, file):
        super().__init__(parent)
        
        self.file = file
        
        # Configure window
        self.title(f"Preview - {file.name}")
        self.geometry("800x600")
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Center on parent
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - 800) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - 600) // 2
        self.geometry(f"+{x}+{y}")
        
        # Create UI
        self.create_ui()
        
        # Load content
        self.load_content()
    
    def create_ui(self):
        """Create dialog UI"""
        # Header
        header = ctk.CTkFrame(self, fg_color="#2E86AB", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        header_inner = ctk.CTkFrame(header, fg_color="transparent")
        header_inner.pack(fill="x", padx=20, pady=15)
        
        icon_label = ctk.CTkLabel(
            header_inner,
            text=self.file.file_type_icon,
            font=("Segoe UI", 28)
        )
        icon_label.pack(side="left", padx=(0, 15))
        
        info_frame = ctk.CTkFrame(header_inner, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=self.file.name,
            font=("Segoe UI", 16, "bold"),
            text_color="white"
        )
        name_label.pack(anchor="w")
        
        meta_label = ctk.CTkLabel(
            info_frame,
            text=f"{self.file.file_type_name} • {self.file.size_formatted}",
            font=("Segoe UI", 11),
            text_color="#e0e0e0"
        )
        meta_label.pack(anchor="w")
        
        close_btn = ctk.CTkButton(
            header_inner,
            text="✕",
            command=self.destroy,
            fg_color="transparent",
            text_color="white",
            hover_color="#1a5270",
            font=("Segoe UI", 16),
            width=40,
            height=40
        )
        close_btn.pack(side="right")
        
        # Content area
        content_frame = ctk.CTkFrame(self, fg_color="#f5f5f5")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Text preview
        self.content_text = ctk.CTkTextbox(
            content_frame,
            font=("Consolas", 12),
            wrap="word"
        )
        self.content_text.pack(fill="both", expand=True)
        
        # Status bar
        self.status_label = ctk.CTkLabel(
            self,
            text="Loading...",
            font=("Segoe UI", 11),
            text_color="#666",
            height=30
        )
        self.status_label.pack(fill="x", padx=10, pady=(0, 10))
    
    def load_content(self):
        """Load file content"""
        if not ContentReader.can_read(self.file.path):
            self.content_text.insert("1.0", f"[Preview not available for this file type: {self.file.extension}]")
            self.status_label.configure(text="Preview not supported")
            return
        
        content, error = ContentReader.read_file(self.file.path, max_chars=100000)
        
        if error:
            self.content_text.insert("1.0", f"[Error loading preview: {error}]")
            self.status_label.configure(text=f"Error: {error}")
        elif content:
            self.content_text.insert("1.0", content)
            
            word_count = ContentReader.get_word_count(content)
            line_count = ContentReader.get_line_count(content)
            self.status_label.configure(
                text=f"{line_count:,} lines • {word_count:,} words • {len(content):,} characters"
            )
        else:
            self.content_text.insert("1.0", "[File is empty]")
            self.status_label.configure(text="Empty file")
        
        self.content_text.configure(state="disabled")


class BatchTagDialog(ctk.CTkToplevel):
    """Dialog for batch tagging multiple files"""
    
    def __init__(self, parent, files: List, on_complete: Optional[Callable] = None):
        super().__init__(parent)
        
        self.files = files
        self.on_complete = on_complete
        
        # Configure window
        self.title("Batch Tag Files")
        self.geometry("500x450")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Center
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - 500) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - 450) // 2
        self.geometry(f"+{x}+{y}")
        
        self.tags_to_add = set()
        
        # Create UI
        self.create_ui()
    
    def create_ui(self):
        """Create dialog UI"""
        # Header
        header = ctk.CTkFrame(self, fg_color="#2E86AB", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header,
            text=f"🏷️ Tag {len(self.files)} Files",
            font=("Segoe UI", 18, "bold"),
            text_color="white"
        )
        title.pack(pady=20)
        
        # Content
        content = ctk.CTkFrame(self, fg_color="#f5f5f5")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Files summary
        files_frame = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        files_frame.pack(fill="x", pady=(0, 15))
        
        files_title = ctk.CTkLabel(
            files_frame,
            text="Selected Files",
            font=("Segoe UI", 13, "bold"),
            text_color="#2E86AB"
        )
        files_title.pack(padx=15, pady=(10, 5), anchor="w")
        
        # Show first few files
        files_text = "\n".join([f"• {f.name}" for f in self.files[:5]])
        if len(self.files) > 5:
            files_text += f"\n• ... and {len(self.files) - 5} more"
        
        files_list = ctk.CTkLabel(
            files_frame,
            text=files_text,
            font=("Segoe UI", 11),
            text_color="#666",
            justify="left"
        )
        files_list.pack(padx=15, pady=(0, 10), anchor="w")
        
        # Add tags section
        tags_frame = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        tags_frame.pack(fill="both", expand=True)
        
        tags_title = ctk.CTkLabel(
            tags_frame,
            text="Tags to Add",
            font=("Segoe UI", 13, "bold"),
            text_color="#2E86AB"
        )
        tags_title.pack(padx=15, pady=(10, 5), anchor="w")
        
        # Tag input
        input_frame = ctk.CTkFrame(tags_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=15, pady=5)
        
        self.tag_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter tag and press Enter...",
            height=38
        )
        self.tag_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.tag_entry.bind('<Return>', lambda e: self.add_tag())
        
        add_btn = ctk.CTkButton(
            input_frame,
            text="Add",
            command=self.add_tag,
            fg_color="#6A994E",
            width=70,
            height=38
        )
        add_btn.pack(side="right")
        
        # Tags display
        self.tags_display = ctk.CTkScrollableFrame(
            tags_frame,
            fg_color="transparent",
            height=100
        )
        self.tags_display.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        
        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self.destroy,
            fg_color="white",
            text_color="#2E86AB",
            border_width=2,
            border_color="#2E86AB",
            width=120,
            height=40
        )
        cancel_btn.pack(side="left")
        
        apply_btn = ctk.CTkButton(
            btn_frame,
            text="Apply Tags",
            command=self.apply_tags,
            fg_color="#2E86AB",
            font=("Segoe UI", 14, "bold"),
            width=140,
            height=40
        )
        apply_btn.pack(side="right")
    
    def add_tag(self):
        """Add a tag to the list"""
        tag = self.tag_entry.get().strip().lower().replace(' ', '-')
        tag = ''.join(c for c in tag if c.isalnum() or c == '-')
        
        if tag and tag not in self.tags_to_add:
            self.tags_to_add.add(tag)
            self.refresh_tags_display()
        
        self.tag_entry.delete(0, 'end')
    
    def remove_tag(self, tag):
        """Remove a tag from the list"""
        self.tags_to_add.discard(tag)
        self.refresh_tags_display()
    
    def refresh_tags_display(self):
        """Refresh tags display"""
        for widget in self.tags_display.winfo_children():
            widget.destroy()
        
        for tag in sorted(self.tags_to_add):
            chip = ctk.CTkFrame(self.tags_display, fg_color="#C7F0BD", corner_radius=15)
            chip.pack(side="left", padx=3, pady=3)
            
            label = ctk.CTkLabel(chip, text=f"#{tag}", font=("Segoe UI", 11), text_color="#2E86AB")
            label.pack(side="left", padx=(10, 5), pady=5)
            
            remove_btn = ctk.CTkButton(
                chip,
                text="✕",
                command=lambda t=tag: self.remove_tag(t),
                fg_color="transparent",
                text_color="#666",
                width=20,
                height=20
            )
            remove_btn.pack(side="right", padx=(0, 5))
    
    def apply_tags(self):
        """Apply tags to all files"""
        if not self.tags_to_add:
            messagebox.showwarning("No Tags", "Please add at least one tag")
            return
        
        success = 0
        for file in self.files:
            if FileService.add_tags_to_file(file.id, list(self.tags_to_add)):
                success += 1
        
        messagebox.showinfo(
            "Complete",
            f"Added {len(self.tags_to_add)} tag(s) to {success} file(s)"
        )
        
        if self.on_complete:
            self.on_complete()
        
        self.destroy()


class ConfirmDialog(ctk.CTkToplevel):
    """Simple confirmation dialog"""
    
    def __init__(self, parent, title: str, message: str, on_confirm: Callable, 
                 confirm_text: str = "Confirm", danger: bool = False):
        super().__init__(parent)
        
        self.on_confirm = on_confirm
        self.result = False
        
        # Configure window
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Center
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - 400) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - 200) // 2
        self.geometry(f"+{x}+{y}")
        
        # Content
        content = ctk.CTkFrame(self, fg_color="#f5f5f5")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        msg_label = ctk.CTkLabel(
            content,
            text=message,
            font=("Segoe UI", 14),
            wraplength=350,
            justify="center"
        )
        msg_label.pack(expand=True)
        
        # Buttons
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(20, 0))
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self.cancel,
            fg_color="white",
            text_color="#666",
            border_width=2,
            border_color="#ddd",
            width=100
        )
        cancel_btn.pack(side="left", expand=True, padx=10)
        
        confirm_btn = ctk.CTkButton(
            btn_frame,
            text=confirm_text,
            command=self.confirm,
            fg_color="#EF4444" if danger else "#2E86AB",
            width=100
        )
        confirm_btn.pack(side="right", expand=True, padx=10)
    
    def cancel(self):
        self.result = False
        self.destroy()
    
    def confirm(self):
        self.result = True
        self.on_confirm()
        self.destroy()
