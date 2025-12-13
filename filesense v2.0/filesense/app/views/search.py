"""
Search View - Search and filter files
"""
import customtkinter as ctk
from app.services.file_service import FileService


class SearchView(ctk.CTkFrame):
    """Search view for finding files"""
    
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#f5f5f5")
        self.app = app
        self.results = []
        
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
            text="Search Files",
            font=("Segoe UI", 28, "bold"),
            text_color="#2E86AB"
        )
        title.pack(anchor="w")
    
    def create_content(self):
        """Create search content"""
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Search bar
        search_frame = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=12)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        search_inner = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_inner.pack(fill="x", padx=20, pady=15)
        search_inner.grid_columnconfigure(0, weight=1)
        
        self.search_entry = ctk.CTkEntry(
            search_inner,
            placeholder_text="Search by filename, tags, or content...",
            height=45,
            font=("Segoe UI", 14)
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_entry.bind('<Return>', lambda e: self.perform_search())
        
        search_btn = ctk.CTkButton(
            search_inner,
            text="🔍 Search",
            command=self.perform_search,
            fg_color="#2E86AB",
            font=("Segoe UI", 14),
            height=45,
            width=120
        )
        search_btn.grid(row=0, column=1)
        
        # Results area
        self.results_scroll = ctk.CTkScrollableFrame(
            content_frame,
            fg_color="white",
            corner_radius=12
        )
        self.results_scroll.grid(row=1, column=0, sticky="nsew")
        
        # Initial message
        self.show_initial_message()
    
    def show_initial_message(self):
        """Show initial search message"""
        msg = ctk.CTkLabel(
            self.results_scroll,
            text="🔍 Enter a search term to find files",
            font=("Segoe UI", 14),
            text_color="#999"
        )
        msg.pack(pady=50)
    
    def perform_search(self):
        """Perform search"""
        query = self.search_entry.get().strip()
        
        # Clear results
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
        
        if not query:
            self.show_initial_message()
            return
        
        # Search files
        self.results = FileService.search_files(query)
        
        if not self.results:
            no_results = ctk.CTkLabel(
                self.results_scroll,
                text=f"No files found matching '{query}'",
                font=("Segoe UI", 14),
                text_color="#999"
            )
            no_results.pack(pady=50)
            return
        
        # Show results count
        count_label = ctk.CTkLabel(
            self.results_scroll,
            text=f"Found {len(self.results)} file(s)",
            font=("Segoe UI", 14, "bold"),
            text_color="#2E86AB",
            anchor="w"
        )
        count_label.pack(fill="x", padx=20, pady=(20, 10))
        
        # Display results
        for file in self.results:
            self.create_result_item(file)
    
    def create_result_item(self, file):
        """Create a search result item"""
        item = ctk.CTkFrame(self.results_scroll, fg_color="#f9f9f9", corner_radius=8, cursor="hand2")
        item.pack(fill="x", padx=15, pady=5)
        item.bind("<Button-1>", lambda e: self.app.show_file_detail(file))
        
        info_frame = ctk.CTkFrame(item, fg_color="transparent")
        info_frame.pack(fill="x", padx=15, pady=12)
        
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
            text=f"{file.file_type_name} • {file.size_formatted} • {file.modified_time_ago}",
            font=("Segoe UI", 11),
            text_color="#666",
            anchor="w"
        )
        meta_label.pack(anchor="w")
        
        if file.tags:
            tags_text = " ".join([f"#{tag.tag}" for tag in file.tags[:3]])
            tags_label = ctk.CTkLabel(
                text_frame,
                text=tags_text,
                font=("Segoe UI", 10),
                text_color="#6A994E",
                anchor="w"
            )
            tags_label.pack(anchor="w")
