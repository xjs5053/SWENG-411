"""
Tags View - Manage and browse tags
"""
import customtkinter as ctk
from app.services.stats_service import StatsService
from app.services.file_service import FileService


class TagsView(ctk.CTkFrame):
    """Tags view for managing file tags"""
    
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#f5f5f5")
        self.app = app
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.create_header()
        self.create_content()
    
    def create_header(self):
        """Create page header"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 10))
        
        title = ctk.CTkLabel(
            header_frame,
            text="Tags",
            font=("Segoe UI", 28, "bold"),
            text_color="#2E86AB"
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Browse files by tags",
            font=("Segoe UI", 14),
            text_color="#666"
        )
        subtitle.pack(anchor="w", pady=(5, 0))
    
    def create_content(self):
        """Create tags content"""
        content_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        content_scroll.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        content_scroll.grid_columnconfigure(0, weight=1)
        
        # Get popular tags
        tags = StatsService.get_popular_tags(100)
        
        if not tags:
            no_tags = ctk.CTkLabel(
                content_scroll,
                text="No tags yet. Add tags to your files!",
                font=("Segoe UI", 14),
                text_color="#999"
            )
            no_tags.pack(pady=50)
            return
        
        # Create tag cloud
        tags_container = ctk.CTkFrame(content_scroll, fg_color="white", corner_radius=12)
        tags_container.grid(row=0, column=0, sticky="ew")
        
        tags_title = ctk.CTkLabel(
            tags_container,
            text="All Tags",
            font=("Segoe UI", 18, "bold"),
            text_color="#2E86AB",
            anchor="w"
        )
        tags_title.pack(fill="x", padx=20, pady=(20, 10))
        
        # Tag items
        for tag, count in tags:
            tag_item = ctk.CTkFrame(tags_container, fg_color="#f9f9f9", corner_radius=8, cursor="hand2")
            tag_item.pack(fill="x", padx=15, pady=5)
            
            tag_label = ctk.CTkLabel(
                tag_item,
                text=f"#{tag}",
                font=("Segoe UI", 14, "bold"),
                text_color="#2E86AB",
                anchor="w"
            )
            tag_label.pack(side="left", padx=15, pady=12, fill="x", expand=True)
            
            count_badge = ctk.CTkLabel(
                tag_item,
                text=str(count),
                font=("Segoe UI", 12),
                text_color="white",
                fg_color="#2E86AB",
                corner_radius=12,
                width=40,
                height=24
            )
            count_badge.pack(side="right", padx=15)
