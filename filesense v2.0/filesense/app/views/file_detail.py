"""
File Detail View - Detailed file information with tag editing and preview
"""
import customtkinter as ctk
from tkinter import messagebox
import os
from app.services.file_service import FileService
from app.views.dialogs import TagEditorDialog, FilePreviewDialog
from app.utils.content_reader import ContentReader


class FileDetailView(ctk.CTkFrame):
    """Enhanced file detail view with tag editing and preview"""
    
    def __init__(self, parent, app, file):
        super().__init__(parent, fg_color="#f5f5f5")
        self.app = app
        self.file = file
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.create_header()
        self.create_content()
    
    def create_header(self):
        """Create page header"""
        header_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=12)
        header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 10))
        
        header_inner = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_inner.pack(fill="x", padx=20, pady=15)
        
        # Back button
        back_btn = ctk.CTkButton(
            header_inner,
            text="← Back",
            command=self.app.show_browser,
            fg_color="transparent",
            text_color="#2E86AB",
            hover_color="#e8f4f8",
            font=("Segoe UI", 13),
            width=80
        )
        back_btn.pack(side="left", padx=(0, 20))
        
        # File info
        icon_label = ctk.CTkLabel(
            header_inner,
            text=self.file.file_type_icon,
            font=("Segoe UI", 40)
        )
        icon_label.pack(side="left", padx=(0, 15))
        
        text_frame = ctk.CTkFrame(header_inner, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)
        
        name_label = ctk.CTkLabel(
            text_frame,
            text=self.file.name,
            font=("Segoe UI", 22, "bold"),
            text_color="#2E86AB",
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        path_label = ctk.CTkLabel(
            text_frame,
            text=self.file.path,
            font=("Segoe UI", 11),
            text_color="#666",
            anchor="w"
        )
        path_label.pack(anchor="w")
        
        # Action buttons
        btn_frame = ctk.CTkFrame(header_inner, fg_color="transparent")
        btn_frame.pack(side="right")
        
        open_btn = ctk.CTkButton(
            btn_frame,
            text="📂 Open",
            command=self.open_file,
            fg_color="#6A994E",
            hover_color="#5a8440",
            font=("Segoe UI", 13),
            width=100,
            height=38
        )
        open_btn.pack(side="left", padx=3)
        
        preview_btn = ctk.CTkButton(
            btn_frame,
            text="👁️ Preview",
            command=self.preview_file,
            fg_color="#2E86AB",
            hover_color="#1a5270",
            font=("Segoe UI", 13),
            width=100,
            height=38
        )
        preview_btn.pack(side="left", padx=3)
        
        tags_btn = ctk.CTkButton(
            btn_frame,
            text="🏷️ Edit Tags",
            command=self.edit_tags,
            fg_color="#FFD93D",
            text_color="#2E86AB",
            hover_color="#e6c236",
            font=("Segoe UI", 13),
            width=110,
            height=38
        )
        tags_btn.pack(side="left", padx=3)
        
        ai_btn = ctk.CTkButton(
            btn_frame,
            text="🤖 AI Analyze",
            command=self.ai_analyze,
            fg_color="#FF9800",
            hover_color="#e68900",
            font=("Segoe UI", 13),
            width=120,
            height=38
        )
        ai_btn.pack(side="left", padx=3)
    
    def create_content(self):
        """Create detail content"""
        content_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        content_scroll.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        content_scroll.grid_columnconfigure(0, weight=1)
        content_scroll.grid_columnconfigure(1, weight=1)
        
        # Left column
        left_col = ctk.CTkFrame(content_scroll, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Properties card
        self.create_properties_card(left_col)
        
        # Tags card
        self.create_tags_card(left_col)
        
        # Right column
        right_col = ctk.CTkFrame(content_scroll, fg_color="transparent")
        right_col.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Summary card
        self.create_summary_card(right_col)
        
        # Quick preview card
        self.create_preview_card(right_col)
        
        # Activity card
        self.create_activity_card(right_col)
    
    def create_properties_card(self, parent):
        """Create file properties card"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        card.pack(fill="x", pady=(0, 15))
        
        title = ctk.CTkLabel(
            card,
            text="📋 File Properties",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E86AB"
        )
        title.pack(padx=20, pady=(15, 10), anchor="w")
        
        # Properties grid
        props_frame = ctk.CTkFrame(card, fg_color="#f9f9f9", corner_radius=8)
        props_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        properties = [
            ("Type", self.file.file_type_name),
            ("Size", self.file.size_formatted),
            ("Extension", self.file.extension or "None"),
            ("Created", self.file.date_added.strftime("%b %d, %Y %I:%M %p") if self.file.date_added else "Unknown"),
            ("Modified", self.file.last_modified.strftime("%b %d, %Y %I:%M %p") if self.file.last_modified else "Unknown"),
            ("Last Accessed", self.file.last_accessed.strftime("%b %d, %Y %I:%M %p") if self.file.last_accessed else "Unknown"),
            ("Category", self.file.category or "Uncategorized"),
        ]
        
        for label, value in properties:
            prop_row = ctk.CTkFrame(props_frame, fg_color="transparent")
            prop_row.pack(fill="x", padx=15, pady=8)
            
            label_widget = ctk.CTkLabel(
                prop_row,
                text=f"{label}:",
                font=("Segoe UI", 12, "bold"),
                text_color="#2E86AB",
                width=120,
                anchor="w"
            )
            label_widget.pack(side="left")
            
            value_widget = ctk.CTkLabel(
                prop_row,
                text=value,
                font=("Segoe UI", 12),
                text_color="#333",
                anchor="w"
            )
            value_widget.pack(side="left", fill="x", expand=True)
    
    def create_tags_card(self, parent):
        """Create tags card"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        card.pack(fill="x", pady=(0, 15))
        
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(15, 10))
        
        title = ctk.CTkLabel(
            header,
            text="🏷️ Tags",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E86AB"
        )
        title.pack(side="left")
        
        edit_btn = ctk.CTkButton(
            header,
            text="Edit",
            command=self.edit_tags,
            fg_color="#e8f4f8",
            text_color="#2E86AB",
            hover_color="#d0e8f0",
            font=("Segoe UI", 11),
            width=60,
            height=28
        )
        edit_btn.pack(side="right")
        
        # Tags display
        self.tags_container = ctk.CTkFrame(card, fg_color="transparent")
        self.tags_container.pack(fill="x", padx=15, pady=(0, 15))
        
        self.refresh_tags_display()
    
    def refresh_tags_display(self):
        """Refresh the tags display"""
        for widget in self.tags_container.winfo_children():
            widget.destroy()
        
        if self.file.tags:
            for tag in self.file.tags:
                tag_chip = ctk.CTkButton(
                    self.tags_container,
                    text=f"#{tag.tag}",
                    fg_color="#C7F0BD",
                    text_color="#2E86AB",
                    hover_color="#aae09e",
                    font=("Segoe UI", 12),
                    height=32,
                    corner_radius=16
                )
                tag_chip.pack(side="left", padx=3, pady=3)
        else:
            no_tags = ctk.CTkLabel(
                self.tags_container,
                text="No tags yet. Click 'Edit' to add tags.",
                font=("Segoe UI", 12),
                text_color="#999"
            )
            no_tags.pack(pady=10)
    
    def create_summary_card(self, parent):
        """Create summary card"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        card.pack(fill="x", pady=(0, 15))
        
        title = ctk.CTkLabel(
            card,
            text="📝 Summary",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E86AB"
        )
        title.pack(padx=20, pady=(15, 10), anchor="w")
        
        summary = self.file.ai_summary or self.file.summary
        
        if summary:
            summary_text = ctk.CTkTextbox(
                card,
                height=100,
                font=("Segoe UI", 12),
                wrap="word"
            )
            summary_text.pack(fill="x", padx=15, pady=(0, 15))
            summary_text.insert("1.0", summary)
            summary_text.configure(state="disabled")
        else:
            no_summary = ctk.CTkLabel(
                card,
                text="No summary yet. Use AI Analysis to generate one.",
                font=("Segoe UI", 12),
                text_color="#999"
            )
            no_summary.pack(pady=(0, 15))
            
            generate_btn = ctk.CTkButton(
                card,
                text="🤖 Generate with AI",
                command=self.ai_analyze,
                fg_color="#2E86AB",
                font=("Segoe UI", 12),
                height=35
            )
            generate_btn.pack(padx=15, pady=(0, 15))
    
    def create_preview_card(self, parent):
        """Create quick preview card"""
        if not ContentReader.can_read(self.file.path):
            return
        
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        card.pack(fill="x", pady=(0, 15))
        
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(15, 10))
        
        title = ctk.CTkLabel(
            header,
            text="👁️ Quick Preview",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E86AB"
        )
        title.pack(side="left")
        
        expand_btn = ctk.CTkButton(
            header,
            text="Full Preview",
            command=self.preview_file,
            fg_color="#e8f4f8",
            text_color="#2E86AB",
            hover_color="#d0e8f0",
            font=("Segoe UI", 11),
            width=100,
            height=28
        )
        expand_btn.pack(side="right")
        
        # Preview content
        preview = ContentReader.get_preview(self.file.path, lines=10)
        
        preview_text = ctk.CTkTextbox(
            card,
            height=150,
            font=("Consolas", 11),
            wrap="word"
        )
        preview_text.pack(fill="x", padx=15, pady=(0, 15))
        preview_text.insert("1.0", preview[:2000])
        preview_text.configure(state="disabled")
    
    def create_activity_card(self, parent):
        """Create activity history card"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        card.pack(fill="x")
        
        title = ctk.CTkLabel(
            card,
            text="📊 Activity History",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E86AB"
        )
        title.pack(padx=20, pady=(15, 10), anchor="w")
        
        if self.file.activities:
            for activity in self.file.activities[-5:]:  # Last 5 activities
                activity_row = ctk.CTkFrame(card, fg_color="#f9f9f9", corner_radius=8)
                activity_row.pack(fill="x", padx=15, pady=3)
                
                type_label = ctk.CTkLabel(
                    activity_row,
                    text=activity.activity_type,
                    font=("Segoe UI", 11, "bold"),
                    text_color="#2E86AB"
                )
                type_label.pack(side="left", padx=10, pady=8)
                
                time_label = ctk.CTkLabel(
                    activity_row,
                    text=activity.time_ago,
                    font=("Segoe UI", 10),
                    text_color="#999"
                )
                time_label.pack(side="right", padx=10, pady=8)
            
            ctk.CTkFrame(card, height=15, fg_color="transparent").pack()
        else:
            no_activity = ctk.CTkLabel(
                card,
                text="No activity recorded yet",
                font=("Segoe UI", 12),
                text_color="#999"
            )
            no_activity.pack(pady=(0, 15))
    
    # Action methods
    def open_file(self):
        """Open file with default application"""
        try:
            if os.path.exists(self.file.path):
                if os.name == 'nt':
                    os.startfile(self.file.path)
                else:
                    os.system(f'xdg-open "{self.file.path}"')
            else:
                messagebox.showerror("Error", "File not found on disk")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {str(e)}")
    
    def preview_file(self):
        """Open file preview dialog"""
        if not ContentReader.can_read(self.file.path):
            messagebox.showinfo(
                "Preview Unavailable",
                f"Preview is not available for {self.file.extension} files."
            )
            return
        
        FilePreviewDialog(self, self.file)
    
    def edit_tags(self):
        """Open tag editor dialog"""
        def on_save():
            # Refresh file from database
            self.file = FileService.get_file_by_id(self.file.id)
            self.refresh_tags_display()
        
        TagEditorDialog(self, self.file, on_save=on_save)
    
    def ai_analyze(self):
        """Navigate to AI analysis with this file"""
        self.app.show_ai(self.file)
