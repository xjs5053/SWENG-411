"""
Dashboard View - Main landing page with statistics
"""
import customtkinter as ctk
from app.services.stats_service import StatsService
from app.services.file_service import FileService


class DashboardView(ctk.CTkFrame):
    """Dashboard view showing file statistics and recent activity"""
    
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#f5f5f5")
        self.app = app
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create header
        self.create_header()
        
        # Create main content
        self.create_content()
    
    def create_header(self):
        """Create page header"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 10))
        
        title = ctk.CTkLabel(
            header_frame,
            text="Welcome to FileSense",
            font=("Segoe UI", 28, "bold"),
            text_color="#2E86AB"
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="AI-powered file organization at your fingertips",
            font=("Segoe UI", 14),
            text_color="#666"
        )
        subtitle.pack(anchor="w", pady=(5, 0))
    
    def create_content(self):
        """Create dashboard content"""
        # Content container
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Search bar
        search_frame = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=12)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search files by content, tags, or date...",
            height=50,
            font=("Segoe UI", 15),
            border_width=0,
            fg_color="white"
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        self.search_entry.bind('<Return>', lambda e: self.perform_search())
        
        # Stats and content grid
        grid_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        grid_frame.grid(row=1, column=0, sticky="nsew")
        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)
        grid_frame.grid_rowconfigure(1, weight=1)
        
        # Get statistics
        stats = StatsService.get_summary_stats()
        
        # Stats cards row
        stats_row = ctk.CTkFrame(grid_frame, fg_color="transparent")
        stats_row.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        stats_row.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Total Files card
        self.create_stat_card(
            stats_row,
            "Total Files",
            str(stats['total_files']),
            0
        )
        
        # Tagged Files card
        self.create_stat_card(
            stats_row,
            "Tagged Files",
            str(stats['tagged_files']),
            1
        )
        
        # Total Size card
        self.create_stat_card(
            stats_row,
            "Total Size",
            stats['size_formatted'],
            2
        )
        
        # Recent Files section
        recent_frame = ctk.CTkScrollableFrame(
            grid_frame,
            fg_color="white",
            corner_radius=12
        )
        recent_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        recent_title = ctk.CTkLabel(
            recent_frame,
            text="Recent Files",
            font=("Segoe UI", 18, "bold"),
            text_color="#2E86AB",
            anchor="w"
        )
        recent_title.pack(fill="x", padx=20, pady=(20, 10))
        
        # Get recent files
        recent_files = FileService.get_recent_files(10)
        
        if recent_files:
            for file in recent_files:
                self.create_file_item(recent_frame, file)
        else:
            no_files = ctk.CTkLabel(
                recent_frame,
                text="No files yet. Start by scanning a folder!",
                font=("Segoe UI", 13),
                text_color="#999"
            )
            no_files.pack(pady=30)
        
        # Popular Tags section
        tags_frame = ctk.CTkScrollableFrame(
            grid_frame,
            fg_color="white",
            corner_radius=12
        )
        tags_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        
        tags_title = ctk.CTkLabel(
            tags_frame,
            text="Popular Tags",
            font=("Segoe UI", 18, "bold"),
            text_color="#2E86AB",
            anchor="w"
        )
        tags_title.pack(fill="x", padx=20, pady=(20, 10))
        
        popular_tags = StatsService.get_popular_tags(15)
        
        if popular_tags:
            for tag, count in popular_tags:
                self.create_tag_item(tags_frame, tag, count)
        else:
            no_tags = ctk.CTkLabel(
                tags_frame,
                text="No tags yet",
                font=("Segoe UI", 13),
                text_color="#999"
            )
            no_tags.pack(pady=30)
    
    def create_stat_card(self, parent, title, value, column):
        """Create a statistics card"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        card.grid(row=0, column=column, sticky="ew", padx=5)
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 32, "bold"),
            text_color="#2E86AB"
        )
        value_label.pack(pady=(20, 5))
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 13),
            text_color="#666"
        )
        title_label.pack(pady=(0, 20))
    
    def create_file_item(self, parent, file):
        """Create a file list item"""
        item = ctk.CTkFrame(parent, fg_color="#f9f9f9", corner_radius=8, cursor="hand2")
        item.pack(fill="x", padx=15, pady=5)
        item.bind("<Button-1>", lambda e: self.app.show_file_detail(file))
        
        # File info container
        info_frame = ctk.CTkFrame(item, fg_color="transparent")
        info_frame.pack(fill="x", padx=15, pady=12)
        
        # Icon and name
        icon_label = ctk.CTkLabel(
            info_frame,
            text=file.file_type_icon,
            font=("Segoe UI", 20)
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        text_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)
        
        name_label = ctk.CTkLabel(
            text_frame,
            text=file.name,
            font=("Segoe UI", 13, "bold"),
            text_color="#2E86AB",
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        meta_label = ctk.CTkLabel(
            text_frame,
            text=f"{file.size_formatted} • Modified: {file.modified_time_ago}",
            font=("Segoe UI", 11),
            text_color="#666",
            anchor="w"
        )
        meta_label.pack(anchor="w")
        
        # Make all children clickable
        for widget in item.winfo_children():
            widget.bind("<Button-1>", lambda e: self.app.show_file_detail(file))
            for child in widget.winfo_children():
                child.bind("<Button-1>", lambda e: self.app.show_file_detail(file))
    
    def create_tag_item(self, parent, tag, count):
        """Create a tag list item"""
        item = ctk.CTkFrame(parent, fg_color="#f9f9f9", corner_radius=8)
        item.pack(fill="x", padx=15, pady=5)
        
        tag_label = ctk.CTkLabel(
            item,
            text=f"#{tag}",
            font=("Segoe UI", 13, "bold"),
            text_color="#2E86AB",
            anchor="w"
        )
        tag_label.pack(side="left", padx=15, pady=10, fill="x", expand=True)
        
        count_label = ctk.CTkLabel(
            item,
            text=str(count),
            font=("Segoe UI", 12),
            text_color="#666"
        )
        count_label.pack(side="right", padx=15, pady=10)
    
    def perform_search(self):
        """Perform search and navigate to search view"""
        query = self.search_entry.get()
        if query:
            self.app.show_search()
            # TODO: Pass search query to search view
