"""
Settings View - Application settings with theme support
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
from app.services.ollama_service import OllamaService
from app.utils.theme_manager import ThemeManager, get_theme_manager
from app.models import Settings, get_session


class SettingsView(ctk.CTkFrame):
    """Enhanced settings view with theme and configuration options"""
    
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#f5f5f5")
        self.app = app
        self.ollama = OllamaService()
        self.theme_manager = get_theme_manager()
        
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
            text="⚙️ Settings",
            font=("Segoe UI", 28, "bold"),
            text_color="#2E86AB"
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Configure FileSense to your preferences",
            font=("Segoe UI", 14),
            text_color="#666"
        )
        subtitle.pack(anchor="w", pady=(5, 0))
    
    def create_content(self):
        """Create settings content"""
        content_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        content_scroll.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        content_scroll.grid_columnconfigure(0, weight=1)
        
        # OLLAMA settings
        self.create_ollama_settings(content_scroll)
        
        # Appearance settings
        self.create_appearance_settings(content_scroll)
        
        # File scanning settings
        self.create_scanning_settings(content_scroll)
        
        # Data management
        self.create_data_settings(content_scroll)
        
        # About section
        self.create_about_section(content_scroll)
    
    def create_ollama_settings(self, parent):
        """Create OLLAMA configuration section"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        card.pack(fill="x", pady=(0, 15))
        
        # Header
        header = ctk.CTkFrame(card, fg_color="#e8f4f8", corner_radius=12)
        header.pack(fill="x")
        
        title = ctk.CTkLabel(
            header,
            text="🤖 OLLAMA Configuration",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E86AB"
        )
        title.pack(side="left", padx=20, pady=15)
        
        # Status indicator
        self.ollama_status = ctk.CTkLabel(
            header,
            text="Checking...",
            font=("Segoe UI", 12),
            text_color="#666"
        )
        self.ollama_status.pack(side="right", padx=20, pady=15)
        
        # Content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=15)
        
        # URL setting
        url_frame = ctk.CTkFrame(content, fg_color="transparent")
        url_frame.pack(fill="x", pady=5)
        
        url_label = ctk.CTkLabel(
            url_frame,
            text="OLLAMA URL:",
            font=("Segoe UI", 12),
            width=150,
            anchor="w"
        )
        url_label.pack(side="left")
        
        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="http://localhost:11434",
            height=38
        )
        self.url_entry.pack(side="left", fill="x", expand=True)
        self.url_entry.insert(0, self.load_setting('ollama_url', 'http://localhost:11434'))
        
        # Default model
        model_frame = ctk.CTkFrame(content, fg_color="transparent")
        model_frame.pack(fill="x", pady=10)
        
        model_label = ctk.CTkLabel(
            model_frame,
            text="Default Model:",
            font=("Segoe UI", 12),
            width=150,
            anchor="w"
        )
        model_label.pack(side="left")
        
        self.model_dropdown = ctk.CTkOptionMenu(
            model_frame,
            values=["llama2", "mistral", "codellama"],
            fg_color="#2E86AB",
            button_color="#2E86AB",
            button_hover_color="#1a5270",
            width=200
        )
        self.model_dropdown.pack(side="left")
        self.model_dropdown.set(self.load_setting('default_model', 'llama2'))
        
        # Buttons
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(15, 0))
        
        test_btn = ctk.CTkButton(
            btn_frame,
            text="Test Connection",
            command=self.test_ollama,
            fg_color="#2E86AB",
            height=40,
            width=150
        )
        test_btn.pack(side="left", padx=5)
        
        refresh_btn = ctk.CTkButton(
            btn_frame,
            text="Refresh Models",
            command=self.refresh_models,
            fg_color="white",
            text_color="#2E86AB",
            border_width=2,
            border_color="#2E86AB",
            height=40,
            width=150
        )
        refresh_btn.pack(side="left", padx=5)
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Save",
            command=self.save_ollama_settings,
            fg_color="#6A994E",
            height=40,
            width=100
        )
        save_btn.pack(side="right", padx=5)
        
        # Check status
        self.check_ollama_status()
    
    def create_appearance_settings(self, parent):
        """Create appearance settings section"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        card.pack(fill="x", pady=(0, 15))
        
        header = ctk.CTkFrame(card, fg_color="#e8f4f8", corner_radius=12)
        header.pack(fill="x")
        
        title = ctk.CTkLabel(
            header,
            text="🎨 Appearance",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E86AB"
        )
        title.pack(side="left", padx=20, pady=15)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=15)
        
        # Theme selector
        theme_frame = ctk.CTkFrame(content, fg_color="transparent")
        theme_frame.pack(fill="x", pady=5)
        
        theme_label = ctk.CTkLabel(
            theme_frame,
            text="Theme:",
            font=("Segoe UI", 12),
            width=150,
            anchor="w"
        )
        theme_label.pack(side="left")
        
        themes = list(self.theme_manager.get_available_themes().values())
        self.theme_dropdown = ctk.CTkOptionMenu(
            theme_frame,
            values=themes,
            command=self.change_theme,
            fg_color="#2E86AB",
            width=200
        )
        self.theme_dropdown.pack(side="left")
        
        # Set current theme
        current_theme = self.theme_manager.THEMES.get(
            self.theme_manager.current_theme, {}
        ).get('name', 'Light')
        self.theme_dropdown.set(current_theme)
        
        # Appearance mode
        mode_frame = ctk.CTkFrame(content, fg_color="transparent")
        mode_frame.pack(fill="x", pady=10)
        
        mode_label = ctk.CTkLabel(
            mode_frame,
            text="Mode:",
            font=("Segoe UI", 12),
            width=150,
            anchor="w"
        )
        mode_label.pack(side="left")
        
        self.mode_dropdown = ctk.CTkOptionMenu(
            mode_frame,
            values=["Light", "Dark", "System"],
            command=self.change_mode,
            fg_color="#2E86AB",
            width=200
        )
        self.mode_dropdown.pack(side="left")
        self.mode_dropdown.set(ctk.get_appearance_mode())
    
    def create_scanning_settings(self, parent):
        """Create file scanning settings section"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        card.pack(fill="x", pady=(0, 15))
        
        header = ctk.CTkFrame(card, fg_color="#e8f4f8", corner_radius=12)
        header.pack(fill="x")
        
        title = ctk.CTkLabel(
            header,
            text="📂 File Scanning",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E86AB"
        )
        title.pack(side="left", padx=20, pady=15)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=15)
        
        # Default scan location
        location_frame = ctk.CTkFrame(content, fg_color="transparent")
        location_frame.pack(fill="x", pady=5)
        
        location_label = ctk.CTkLabel(
            location_frame,
            text="Default Location:",
            font=("Segoe UI", 12),
            width=150,
            anchor="w"
        )
        location_label.pack(side="left")
        
        self.location_entry = ctk.CTkEntry(
            location_frame,
            placeholder_text="Select default folder...",
            height=38
        )
        self.location_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.location_entry.insert(0, self.load_setting('default_scan_location', ''))
        
        browse_btn = ctk.CTkButton(
            location_frame,
            text="Browse",
            command=self.browse_location,
            fg_color="#2E86AB",
            width=80,
            height=38
        )
        browse_btn.pack(side="right")
        
        # Include hidden files
        hidden_frame = ctk.CTkFrame(content, fg_color="transparent")
        hidden_frame.pack(fill="x", pady=10)
        
        self.hidden_var = ctk.StringVar(value="off")
        hidden_checkbox = ctk.CTkCheckBox(
            hidden_frame,
            text="Include hidden files",
            variable=self.hidden_var,
            onvalue="on",
            offvalue="off"
        )
        hidden_checkbox.pack(side="left")
        
        # Save button
        save_btn = ctk.CTkButton(
            content,
            text="Save Scanning Settings",
            command=self.save_scanning_settings,
            fg_color="#6A994E",
            height=40
        )
        save_btn.pack(anchor="e", pady=(10, 0))
    
    def create_data_settings(self, parent):
        """Create data management section"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        card.pack(fill="x", pady=(0, 15))
        
        header = ctk.CTkFrame(card, fg_color="#e8f4f8", corner_radius=12)
        header.pack(fill="x")
        
        title = ctk.CTkLabel(
            header,
            text="💾 Data Management",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E86AB"
        )
        title.pack(side="left", padx=20, pady=15)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=15)
        
        # Export data
        export_btn = ctk.CTkButton(
            content,
            text="📤 Export Data",
            command=self.export_data,
            fg_color="#2E86AB",
            height=40,
            width=180
        )
        export_btn.pack(side="left", padx=5)
        
        # Clear database
        clear_btn = ctk.CTkButton(
            content,
            text="🗑️ Clear Database",
            command=self.clear_database,
            fg_color="#EF4444",
            hover_color="#dc2626",
            height=40,
            width=180
        )
        clear_btn.pack(side="left", padx=5)
    
    def create_about_section(self, parent):
        """Create about section"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        card.pack(fill="x")
        
        header = ctk.CTkFrame(card, fg_color="#e8f4f8", corner_radius=12)
        header.pack(fill="x")
        
        title = ctk.CTkLabel(
            header,
            text="ℹ️ About FileSense",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E86AB"
        )
        title.pack(side="left", padx=20, pady=15)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=15)
        
        about_text = """FileSense v1.0.0
AI-Powered File Organization System

Built with:
• Python & CustomTkinter
• SQLAlchemy & SQLite
• OLLAMA Integration

© 2024 FileSense Team"""
        
        about_label = ctk.CTkLabel(
            content,
            text=about_text,
            font=("Segoe UI", 12),
            text_color="#666",
            justify="left"
        )
        about_label.pack(anchor="w")
    
    # Helper methods
    def load_setting(self, key: str, default: str = "") -> str:
        """Load a setting from database"""
        try:
            session = get_session()
            setting = session.query(Settings).filter_by(key=key).first()
            return setting.value if setting else default
        except:
            return default
    
    def save_setting(self, key: str, value: str):
        """Save a setting to database"""
        try:
            session = get_session()
            setting = session.query(Settings).filter_by(key=key).first()
            
            if setting:
                setting.value = value
            else:
                setting = Settings(key=key, value=value)
                session.add(setting)
            
            session.commit()
        except Exception as e:
            print(f"Error saving setting: {e}")
    
    def check_ollama_status(self):
        """Check OLLAMA connection status"""
        if self.ollama.is_running():
            models = self.ollama.get_available_models()
            self.ollama_status.configure(
                text=f"✅ Connected ({len(models)} models)",
                text_color="#6A994E"
            )
            if models:
                self.model_dropdown.configure(values=models)
        else:
            self.ollama_status.configure(
                text="❌ Not connected",
                text_color="#EF4444"
            )
    
    def test_ollama(self):
        """Test OLLAMA connection"""
        if self.ollama.is_running():
            models = self.ollama.get_available_models()
            messagebox.showinfo(
                "Connection Successful",
                f"OLLAMA is running!\nAvailable models: {', '.join(models[:5])}"
            )
            self.check_ollama_status()
        else:
            messagebox.showerror(
                "Connection Failed",
                "Could not connect to OLLAMA.\n\n"
                "Make sure OLLAMA is installed and running."
            )
    
    def refresh_models(self):
        """Refresh available models"""
        models = self.ollama.get_available_models()
        if models:
            self.model_dropdown.configure(values=models)
            messagebox.showinfo("Models Refreshed", f"Found {len(models)} models")
        else:
            messagebox.showwarning("No Models", "No models found. Install with: ollama pull llama2")
    
    def save_ollama_settings(self):
        """Save OLLAMA settings"""
        self.save_setting('ollama_url', self.url_entry.get())
        self.save_setting('default_model', self.model_dropdown.get())
        messagebox.showinfo("Saved", "OLLAMA settings saved!")
    
    def change_theme(self, theme_name):
        """Change application theme"""
        # Find theme key from name
        for key, theme in self.theme_manager.THEMES.items():
            if theme['name'] == theme_name:
                self.theme_manager.set_theme(key)
                messagebox.showinfo(
                    "Theme Changed",
                    f"Theme changed to {theme_name}.\n"
                    "Some changes may require restart."
                )
                break
    
    def change_mode(self, mode):
        """Change appearance mode"""
        ctk.set_appearance_mode(mode.lower())
    
    def browse_location(self):
        """Browse for default scan location"""
        folder = filedialog.askdirectory(title="Select Default Scan Location")
        if folder:
            self.location_entry.delete(0, 'end')
            self.location_entry.insert(0, folder)
    
    def save_scanning_settings(self):
        """Save scanning settings"""
        self.save_setting('default_scan_location', self.location_entry.get())
        self.save_setting('include_hidden', self.hidden_var.get())
        messagebox.showinfo("Saved", "Scanning settings saved!")
    
    def export_data(self):
        """Export database data"""
        file_path = filedialog.asksaveasfilename(
            title="Export Data",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            import json
            from app.models import File
            
            session = get_session()
            files = session.query(File).all()
            
            data = {
                'files': [
                    {
                        'name': f.name,
                        'path': f.path,
                        'extension': f.extension,
                        'size': f.size,
                        'tags': f.tag_list,
                        'summary': f.summary or f.ai_summary
                    }
                    for f in files
                ]
            }
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            messagebox.showinfo("Export Complete", f"Exported {len(files)} files to {file_path}")
            
        except Exception as e:
            messagebox.showerror("Export Failed", f"Error: {str(e)}")
    
    def clear_database(self):
        """Clear all data from database"""
        confirm = messagebox.askyesno(
            "Confirm Clear",
            "Are you sure you want to clear ALL data?\n\n"
            "This will remove all files, tags, and activity logs.\n"
            "This action cannot be undone!"
        )
        
        if not confirm:
            return
        
        try:
            from app.models import File, Tag, ActivityLog
            
            session = get_session()
            session.query(ActivityLog).delete()
            session.query(Tag).delete()
            session.query(File).delete()
            session.commit()
            
            messagebox.showinfo("Database Cleared", "All data has been removed.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear database: {str(e)}")
