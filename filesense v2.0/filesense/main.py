#!/usr/bin/env python3
"""
FileSense - AI-Powered File Organization
Main application entry point
"""
import sys
import os
import customtkinter as ctk
from app.views.dashboard import DashboardView
from app.views.search import SearchView
from app.views.file_browser import FileBrowserView
from app.views.file_detail import FileDetailView
from app.views.recent_files import RecentFilesView
from app.views.tags import TagsView
from app.views.batch_operations import BatchOperationsView
from app.views.ai_analysis import AIAnalysisView
from app.views.settings import SettingsView
from app.views.duplicate_finder import DuplicateFinderView
from app.views.smart_folders import SmartFoldersView
from app.models import init_database

class FileSenseApp(ctk.CTk):
    """Main FileSense Application"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("FileSense - AI-Powered File Organization")
        self.geometry("1400x800")
        
        # Set minimum size
        self.minsize(1200, 700)
        
        # Set color theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Initialize database
        init_database()
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.main_frame = ctk.CTkFrame(self, fg_color="#f5f5f5")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Current view
        self.current_view = None
        
        # Track active button
        self.active_button = None
        
        # Show dashboard by default
        self.show_dashboard()
        
        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_sidebar(self):
        """Create sidebar navigation"""
        # Sidebar frame with gradient-like effect
        self.sidebar_frame = ctk.CTkFrame(
            self, 
            width=220, 
            corner_radius=0, 
            fg_color="#2E86AB"
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(13, weight=1)
        
        # Logo section
        logo_container = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        logo_container.grid(row=0, column=0, padx=20, pady=(30, 10), sticky="w")
        
        logo_frame = ctk.CTkFrame(
            logo_container, 
            fg_color="#FFD93D", 
            corner_radius=8,
            width=35, 
            height=35
        )
        logo_frame.pack(side="left", padx=(0, 10))
        logo_frame.pack_propagate(False)
        
        logo_label = ctk.CTkLabel(logo_frame, text="📁", font=("Segoe UI", 20))
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
        
        title_label = ctk.CTkLabel(
            logo_container, 
            text="FileSense",
            font=("Segoe UI", 24, "bold"), 
            text_color="white"
        )
        title_label.pack(side="left")
        
        # Spacer
        spacer = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent", height=30)
        spacer.grid(row=1, column=0)
        
        # Navigation buttons
        self.btn_dashboard = self.create_nav_button("🏠 Dashboard", self.show_dashboard, 2)
        self.btn_search = self.create_nav_button("🔍 Search", self.show_search, 3)
        self.btn_browser = self.create_nav_button("📂 File Browser", self.show_browser, 4)
        self.btn_recent = self.create_nav_button("🕒 Recent Files", self.show_recent, 5)
        self.btn_tags = self.create_nav_button("🏷️ Tags", self.show_tags, 6)
        self.btn_smart = self.create_nav_button("📁 Smart Folders", self.show_smart_folders, 7)
        self.btn_duplicates = self.create_nav_button("🔍 Find Duplicates", self.show_duplicates, 8)
        self.btn_batch = self.create_nav_button("⚡ Batch Operations", self.show_batch, 9)
        self.btn_ai = self.create_nav_button("🤖 AI Analysis", self.show_ai, 10)
        self.btn_settings = self.create_nav_button("⚙️ Settings", self.show_settings, 11)
    
    def create_nav_button(self, text, command, row):
        """Create navigation button with mockup styling"""
        btn = ctk.CTkButton(
            self.sidebar_frame,
            text=text,
            command=command,
            fg_color="transparent",
            text_color="white",
            hover_color="rgba(255, 255, 255, 0.1)",
            anchor="w",
            height=45,
            corner_radius=8,
            font=("Segoe UI", 15),
            border_width=0
        )
        btn.grid(row=row, column=0, padx=15, pady=4, sticky="ew")
        
        # Store original colors for reset
        btn._original_fg = "transparent"
        btn._original_text = "white"
        
        return btn
    
    def set_active_button(self, button):
        """Highlight the active button"""
        # Reset previous active button
        if self.active_button:
            self.active_button.configure(
                fg_color=self.active_button._original_fg,
                text_color=self.active_button._original_text,
                font=("Segoe UI", 15)
            )
        
        # Set new active button - Yellow background, Blue text
        button.configure(
            fg_color="#FFD93D",
            text_color="#2E86AB",
            font=("Segoe UI", 15, "bold")
        )
        
        self.active_button = button
    
    def clear_main_frame(self):
        """Clear current view"""
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None
    
    def show_dashboard(self):
        """Show dashboard view"""
        self.clear_main_frame()
        self.current_view = DashboardView(self.main_frame, self)
        self.current_view.grid(row=0, column=0, sticky="nsew")
        self.set_active_button(self.btn_dashboard)
    
    def show_search(self):
        """Show search view"""
        self.clear_main_frame()
        self.current_view = SearchView(self.main_frame, self)
        self.current_view.grid(row=0, column=0, sticky="nsew")
        self.set_active_button(self.btn_search)
    
    def show_browser(self):
        """Show file browser view"""
        self.clear_main_frame()
        self.current_view = FileBrowserView(self.main_frame, self)
        self.current_view.grid(row=0, column=0, sticky="nsew")
        self.set_active_button(self.btn_browser)
    
    def show_file_detail(self, file):
        """Show file detail view"""
        self.clear_main_frame()
        self.current_view = FileDetailView(self.main_frame, self, file)
        self.current_view.grid(row=0, column=0, sticky="nsew")
        # Don't change active button for file details
    
    def show_recent(self):
        """Show recent files view"""
        self.clear_main_frame()
        self.current_view = RecentFilesView(self.main_frame, self)
        self.current_view.grid(row=0, column=0, sticky="nsew")
        self.set_active_button(self.btn_recent)
    
    def show_tags(self):
        """Show tags view"""
        self.clear_main_frame()
        self.current_view = TagsView(self.main_frame, self)
        self.current_view.grid(row=0, column=0, sticky="nsew")
        self.set_active_button(self.btn_tags)
    
    def show_smart_folders(self):
        """Show smart folders view"""
        self.clear_main_frame()
        self.current_view = SmartFoldersView(self.main_frame, self)
        self.current_view.grid(row=0, column=0, sticky="nsew")
        self.set_active_button(self.btn_smart)
    
    def show_duplicates(self):
        """Show duplicate finder view"""
        self.clear_main_frame()
        self.current_view = DuplicateFinderView(self.main_frame, self)
        self.current_view.grid(row=0, column=0, sticky="nsew")
        self.set_active_button(self.btn_duplicates)
    
    def show_batch(self):
        """Show batch operations view"""
        self.clear_main_frame()
        self.current_view = BatchOperationsView(self.main_frame, self)
        self.current_view.grid(row=0, column=0, sticky="nsew")
        self.set_active_button(self.btn_batch)
    
    def show_ai(self, file=None):
        """Show AI analysis view"""
        self.clear_main_frame()
        self.current_view = AIAnalysisView(self.main_frame, self, file)
        self.current_view.grid(row=0, column=0, sticky="nsew")
        self.set_active_button(self.btn_ai)
    
    def show_settings(self):
        """Show settings view"""
        self.clear_main_frame()
        self.current_view = SettingsView(self.main_frame, self)
        self.current_view.grid(row=0, column=0, sticky="nsew")
        self.set_active_button(self.btn_settings)
    
    def on_closing(self):
        """Handle application close"""
        self.destroy()


def main():
    """Main application entry point"""
    app = FileSenseApp()
    app.mainloop()


if __name__ == "__main__":
    main()
