"""
Recent Files View - Recently accessed files
"""
import customtkinter as ctk
from app.services.file_service import FileService


class RecentFilesView(ctk.CTkFrame):
    """Recent files view"""
    
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
            text="Recent Files",
            font=("Segoe UI", 28, "bold"),
            text_color="#2E86AB"
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Files you've recently accessed or modified",
            font=("Segoe UI", 14),
            text_color="#666"
        )
        subtitle.pack(anchor="w", pady=(5, 0))
    
    def create_content(self):
        """Create recent files content"""
        # Filter tabs
        tabs_frame = ctk.CTkFrame(self, fg_color="transparent")
        tabs_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 10))
        
        filters = ["All Files", "Documents", "Spreadsheets", "Images", "PDFs"]
        for filter_name in filters:
            btn = ctk.CTkButton(
                tabs_frame,
                text=filter_name,
                fg_color="#FFD93D" if filter_name == "All Files" else "white",
                text_color="#2E86AB",
                font=("Segoe UI", 12),
                height=35,
                corner_radius=8,
                width=120
            )
            btn.pack(side="left", padx=3)
        
        # Files list
        files_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="white",
            corner_radius=12
        )
        files_scroll.grid(row=2, column=0, sticky="nsew", padx=30, pady=10)
        
        # Get recent files
        recent_files = FileService.get_recent_files(50)
        
        if recent_files:
            for file in recent_files:
                self.create_file_item(files_scroll, file)
        else:
            no_files = ctk.CTkLabel(
                files_scroll,
                text="No recent files",
                font=("Segoe UI", 14),
                text_color="#999"
            )
            no_files.pack(pady=50)
    
    def create_file_item(self, parent, file):
        """Create a file list item"""
        item = ctk.CTkFrame(parent, fg_color="#f9f9f9", corner_radius=8, cursor="hand2")
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
            text=f"{file.size_formatted} • Modified: {file.modified_time_ago}",
            font=("Segoe UI", 11),
            text_color="#666",
            anchor="w"
        )
        meta_label.pack(anchor="w")
