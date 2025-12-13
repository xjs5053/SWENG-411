"""
AI Analysis View - AI-powered file analysis using OLLAMA
"""
import customtkinter as ctk
from tkinter import messagebox
import threading
from app.services.ollama_service import OllamaService
from app.services.file_service import FileService


class AIAnalysisView(ctk.CTkFrame):
    """AI Analysis view for intelligent file analysis"""
    
    def __init__(self, parent, app, file=None):
        super().__init__(parent, fg_color="#f5f5f5")
        self.app = app
        self.selected_file = file
        self.ollama = OllamaService()
        self.analysis_results = None
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create header
        self.create_header()
        
        # Create content
        self.create_content()
        
        # Check OLLAMA status
        self.check_ollama_status()
    
    def create_header(self):
        """Create page header"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 10))
        
        title = ctk.CTkLabel(
            header_frame,
            text="AI File Analysis",
            font=("Segoe UI", 28, "bold"),
            text_color="#2E86AB"
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Generate intelligent summaries and insights using OLLAMA AI",
            font=("Segoe UI", 14),
            text_color="#666"
        )
        subtitle.pack(anchor="w", pady=(5, 0))
    
    def create_content(self):
        """Create analysis content"""
        # Scrollable content
        content_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        content_scroll.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        content_scroll.grid_columnconfigure(0, weight=1)
        
        # OLLAMA status card
        self.status_card = ctk.CTkFrame(content_scroll, fg_color="white", corner_radius=12)
        self.status_card.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        status_title = ctk.CTkLabel(
            self.status_card,
            text="🤖 OLLAMA Status",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E86AB",
            anchor="w"
        )
        status_title.pack(fill="x", padx=20, pady=(15, 5))
        
        self.status_label = ctk.CTkLabel(
            self.status_card,
            text="Checking OLLAMA connection...",
            font=("Segoe UI", 12),
            text_color="#666",
            anchor="w"
        )
        self.status_label.pack(fill="x", padx=20, pady=(0, 15))
        
        # File selection card
        file_card = ctk.CTkFrame(content_scroll, fg_color="white", corner_radius=12)
        file_card.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        file_title = ctk.CTkLabel(
            file_card,
            text="📄 Selected File",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E86AB",
            anchor="w"
        )
        file_title.pack(fill="x", padx=20, pady=(15, 10))
        
        if self.selected_file:
            self.create_file_display(file_card, self.selected_file)
        else:
            # File selection button
            select_btn = ctk.CTkButton(
                file_card,
                text="Choose File to Analyze",
                command=self.choose_file,
                fg_color="#2E86AB",
                font=("Segoe UI", 14),
                height=40
            )
            select_btn.pack(padx=20, pady=(0, 20))
        
        # Analysis options card
        self.options_card = ctk.CTkFrame(content_scroll, fg_color="white", corner_radius=12)
        self.options_card.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        
        options_title = ctk.CTkLabel(
            self.options_card,
            text="🎯 Analysis Options",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E86AB",
            anchor="w"
        )
        options_title.pack(fill="x", padx=20, pady=(15, 10))
        
        # Create option toggles
        options_frame = ctk.CTkFrame(self.options_card, fg_color="transparent")
        options_frame.pack(fill="x", padx=20, pady=(0, 20))
        options_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.option_summary = ctk.CTkCheckBox(
            options_frame,
            text="Generate Summary",
            font=("Segoe UI", 13)
        )
        self.option_summary.grid(row=0, column=0, sticky="w", pady=5)
        self.option_summary.select()
        
        self.option_tags = ctk.CTkCheckBox(
            options_frame,
            text="Suggest Tags",
            font=("Segoe UI", 13)
        )
        self.option_tags.grid(row=0, column=1, sticky="w", pady=5)
        self.option_tags.select()
        
        self.option_insights = ctk.CTkCheckBox(
            options_frame,
            text="Extract Insights",
            font=("Segoe UI", 13)
        )
        self.option_insights.grid(row=1, column=0, sticky="w", pady=5)
        self.option_insights.select()
        
        self.option_category = ctk.CTkCheckBox(
            options_frame,
            text="Categorize File",
            font=("Segoe UI", 13)
        )
        self.option_category.grid(row=1, column=1, sticky="w", pady=5)
        
        # Model selection
        model_frame = ctk.CTkFrame(self.options_card, fg_color="transparent")
        model_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        model_label = ctk.CTkLabel(
            model_frame,
            text="AI Model:",
            font=("Segoe UI", 12),
            text_color="#666"
        )
        model_label.pack(side="left", padx=(0, 10))
        
        self.model_dropdown = ctk.CTkOptionMenu(
            model_frame,
            values=["llama2", "mistral", "codellama"],
            fg_color="#2E86AB",
            button_color="#2E86AB",
            button_hover_color="#1a5270"
        )
        self.model_dropdown.pack(side="left")
        
        # Start analysis button
        self.analyze_btn = ctk.CTkButton(
            self.options_card,
            text="Start AI Analysis",
            command=self.start_analysis,
            fg_color="#2E86AB",
            hover_color="#1a5270",
            font=("Segoe UI", 15, "bold"),
            height=45
        )
        self.analyze_btn.pack(fill="x", padx=20, pady=(0, 20))
        
        # Results container (hidden initially)
        self.results_frame = ctk.CTkFrame(content_scroll, fg_color="transparent")
        self.results_frame.grid(row=3, column=0, sticky="ew")
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_remove()  # Hide initially
    
    def create_file_display(self, parent, file):
        """Display selected file information"""
        display_frame = ctk.CTkFrame(parent, fg_color="#f9f9f9", corner_radius=8)
        display_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        info_frame = ctk.CTkFrame(display_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=15)
        
        # Icon
        icon_label = ctk.CTkLabel(
            info_frame,
            text=file.file_type_icon,
            font=("Segoe UI", 40)
        )
        icon_label.pack(side="left", padx=(0, 15))
        
        # File info
        text_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)
        
        name_label = ctk.CTkLabel(
            text_frame,
            text=file.name,
            font=("Segoe UI", 16, "bold"),
            text_color="#2E86AB",
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        meta_label = ctk.CTkLabel(
            text_frame,
            text=f"{file.file_type_name} • {file.size_formatted} • Modified: {file.modified_time_ago}",
            font=("Segoe UI", 11),
            text_color="#666",
            anchor="w"
        )
        meta_label.pack(anchor="w", pady=(2, 0))
        
        path_label = ctk.CTkLabel(
            text_frame,
            text=f"Location: {file.path}",
            font=("Segoe UI", 10),
            text_color="#999",
            anchor="w"
        )
        path_label.pack(anchor="w", pady=(2, 0))
        
        # Change file button
        change_btn = ctk.CTkButton(
            info_frame,
            text="Change File",
            command=self.choose_file,
            fg_color="white",
            text_color="#2E86AB",
            border_width=2,
            border_color="#2E86AB",
            font=("Segoe UI", 12),
            width=120
        )
        change_btn.pack(side="right")
    
    def check_ollama_status(self):
        """Check if OLLAMA is running"""
        if self.ollama.is_running():
            models = self.ollama.get_available_models()
            if models:
                self.status_label.configure(
                    text=f"✅ Connected • {len(models)} models available: {', '.join(models[:3])}...",
                    text_color="#6A994E"
                )
                self.model_dropdown.configure(values=models)
                if models:
                    self.model_dropdown.set(models[0])
            else:
                self.status_label.configure(
                    text="⚠️ Connected but no models found. Run 'ollama pull llama2' to download a model.",
                    text_color="#FF9800"
                )
        else:
            self.status_label.configure(
                text="❌ OLLAMA not running. Please start OLLAMA service.",
                text_color="#EF4444"
            )
    
    def choose_file(self):
        """Show file chooser dialog"""
        # Get all files
        files = FileService.get_all_files()
        
        if not files:
            messagebox.showwarning(
                "No Files",
                "No files in database. Please scan a folder first."
            )
            return
        
        # Create selection dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Choose File")
        dialog.geometry("600x500")
        dialog.transient(self)
        dialog.grab_set()
        
        # File list
        scroll = ctk.CTkScrollableFrame(dialog)
        scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        for file in files[:100]:  # Limit to 100 files
            btn = ctk.CTkButton(
                scroll,
                text=f"{file.file_type_icon} {file.name}",
                command=lambda f=file: self.select_file(f, dialog),
                fg_color="#f9f9f9",
                text_color="#2E86AB",
                hover_color="#e8f4f8",
                anchor="w",
                font=("Segoe UI", 12)
            )
            btn.pack(fill="x", pady=2)
    
    def select_file(self, file, dialog):
        """Select a file for analysis"""
        self.selected_file = file
        dialog.destroy()
        
        # Recreate content to show selected file
        self.create_content()
    
    def start_analysis(self):
        """Start AI analysis"""
        if not self.selected_file:
            messagebox.showwarning("No File", "Please select a file first")
            return
        
        if not self.ollama.is_running():
            messagebox.showerror(
                "OLLAMA Not Running",
                "Please start the OLLAMA service before running analysis."
            )
            return
        
        # Disable button
        self.analyze_btn.configure(state="disabled", text="Analyzing...")
        
        # Run analysis in thread
        thread = threading.Thread(target=self.perform_analysis)
        thread.daemon = True
        thread.start()
    
    def perform_analysis(self):
        """Perform AI analysis (runs in background thread)"""
        try:
            # Read file content
            content = FileService.read_file_content(self.selected_file.path)
            
            if not content:
                self.after(0, lambda: messagebox.showerror(
                    "Error",
                    "Could not read file content"
                ))
                return
            
            model = self.model_dropdown.get()
            results = {}
            
            # Generate summary
            if self.option_summary.get():
                results['summary'] = self.ollama.generate_summary(content, model)
            
            # Generate tags
            if self.option_tags.get():
                results['tags'] = self.ollama.generate_tags(content, model)
            
            # Extract insights
            if self.option_insights.get():
                results['insights'] = self.ollama.extract_insights(content, model)
            
            # Categorize
            if self.option_category.get():
                results['category'] = self.ollama.categorize_file(
                    self.selected_file.name,
                    content,
                    model
                )
            
            self.analysis_results = results
            
            # Update UI in main thread
            self.after(0, self.display_results)
            
        except Exception as e:
            self.after(0, lambda: messagebox.showerror(
                "Analysis Error",
                f"Error during analysis: {str(e)}"
            ))
        finally:
            self.after(0, lambda: self.analyze_btn.configure(
                state="normal",
                text="Start AI Analysis"
            ))
    
    def display_results(self):
        """Display analysis results"""
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Show results frame
        self.results_frame.grid()
        
        # Results title
        title_label = ctk.CTkLabel(
            self.results_frame,
            text="🤖 AI Analysis Results",
            font=("Segoe UI", 18, "bold"),
            text_color="#2E86AB",
            anchor="w"
        )
        title_label.pack(fill="x", pady=(0, 15))
        
        row = 0
        
        # Summary
        if 'summary' in self.analysis_results and self.analysis_results['summary']:
            summary_card = ctk.CTkFrame(self.results_frame, fg_color="white", corner_radius=12)
            summary_card.pack(fill="x", pady=(0, 15))
            
            summary_title = ctk.CTkLabel(
                summary_card,
                text="📝 Document Summary",
                font=("Segoe UI", 15, "bold"),
                text_color="#2E86AB",
                anchor="w"
            )
            summary_title.pack(fill="x", padx=20, pady=(15, 10))
            
            summary_text = ctk.CTkTextbox(
                summary_card,
                height=100,
                font=("Segoe UI", 12),
                wrap="word"
            )
            summary_text.pack(fill="x", padx=20, pady=(0, 15))
            summary_text.insert("1.0", self.analysis_results['summary'])
            summary_text.configure(state="disabled")
            
            row += 1
        
        # Tags
        if 'tags' in self.analysis_results and self.analysis_results['tags']:
            tags_card = ctk.CTkFrame(self.results_frame, fg_color="white", corner_radius=12)
            tags_card.pack(fill="x", pady=(0, 15))
            
            tags_title = ctk.CTkLabel(
                tags_card,
                text="🏷️ Suggested Tags",
                font=("Segoe UI", 15, "bold"),
                text_color="#2E86AB",
                anchor="w"
            )
            tags_title.pack(fill="x", padx=20, pady=(15, 10))
            
            tags_container = ctk.CTkFrame(tags_card, fg_color="transparent")
            tags_container.pack(fill="x", padx=20, pady=(0, 10))
            
            for tag in self.analysis_results['tags']:
                tag_btn = ctk.CTkButton(
                    tags_container,
                    text=f"#{tag}",
                    fg_color="#C7F0BD",
                    text_color="#2E86AB",
                    hover_color="#6A994E",
                    font=("Segoe UI", 12),
                    height=32,
                    corner_radius=16
                )
                tag_btn.pack(side="left", padx=3, pady=3)
            
            apply_btn = ctk.CTkButton(
                tags_card,
                text="Apply These Tags",
                command=lambda: self.apply_tags(self.analysis_results['tags']),
                fg_color="#6A994E",
                font=("Segoe UI", 13),
                height=38
            )
            apply_btn.pack(fill="x", padx=20, pady=(10, 15))
            
            row += 1
        
        # Insights
        if 'insights' in self.analysis_results and self.analysis_results['insights']:
            insights_card = ctk.CTkFrame(self.results_frame, fg_color="white", corner_radius=12)
            insights_card.pack(fill="x", pady=(0, 15))
            
            insights_title = ctk.CTkLabel(
                insights_card,
                text="💡 Key Insights",
                font=("Segoe UI", 15, "bold"),
                text_color="#2E86AB",
                anchor="w"
            )
            insights_title.pack(fill="x", padx=20, pady=(15, 10))
            
            for insight in self.analysis_results['insights']:
                insight_item = ctk.CTkFrame(insights_card, fg_color="#FFF9E6", corner_radius=8)
                insight_item.pack(fill="x", padx=20, pady=5)
                
                insight_text = ctk.CTkLabel(
                    insight_item,
                    text=f"• {insight.get('title', '')}: {insight.get('description', '')}",
                    font=("Segoe UI", 11),
                    text_color="#333",
                    anchor="w",
                    wraplength=700,
                    justify="left"
                )
                insight_text.pack(fill="x", padx=15, pady=10)
            
            ctk.CTkFrame(insights_card, height=15, fg_color="transparent").pack()
        
        # Category
        if 'category' in self.analysis_results:
            category_card = ctk.CTkFrame(self.results_frame, fg_color="white", corner_radius=12)
            category_card.pack(fill="x", pady=(0, 15))
            
            category_label = ctk.CTkLabel(
                category_card,
                text=f"📂 Suggested Category: {self.analysis_results['category']}",
                font=("Segoe UI", 14, "bold"),
                text_color="#2E86AB"
            )
            category_label.pack(padx=20, pady=15)
        
        # Action buttons
        actions_card = ctk.CTkFrame(self.results_frame, fg_color="white", corner_radius=12)
        actions_card.pack(fill="x")
        
        actions_frame = ctk.CTkFrame(actions_card, fg_color="transparent")
        actions_frame.pack(fill="x", padx=20, pady=15)
        
        save_btn = ctk.CTkButton(
            actions_frame,
            text="Save Analysis to File",
            command=self.save_analysis,
            fg_color="#2E86AB",
            font=("Segoe UI", 13),
            height=40
        )
        save_btn.pack(side="left", padx=5)
        
        new_btn = ctk.CTkButton(
            actions_frame,
            text="Analyze Another File",
            command=self.choose_file,
            fg_color="white",
            text_color="#2E86AB",
            border_width=2,
            border_color="#2E86AB",
            font=("Segoe UI", 13),
            height=40
        )
        new_btn.pack(side="left", padx=5)
    
    def apply_tags(self, tags):
        """Apply suggested tags to the file"""
        if FileService.add_tags_to_file(self.selected_file.id, tags):
            messagebox.showinfo("Success", "Tags applied successfully!")
        else:
            messagebox.showerror("Error", "Failed to apply tags")
    
    def save_analysis(self):
        """Save analysis results to file"""
        if self.analysis_results and 'summary' in self.analysis_results:
            FileService.update_summary(
                self.selected_file.id,
                self.analysis_results['summary'],
                ai_summary=True
            )
            messagebox.showinfo("Success", "Analysis saved to file!")
        else:
            messagebox.showwarning("No Summary", "No summary to save")
