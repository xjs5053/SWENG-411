"""
Batch Operations View - Batch file operations
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading
from app.services.file_service import FileService
from app.services.ollama_service import OllamaService
from app.views.dialogs import BatchTagDialog


class BatchOperationsView(ctk.CTkFrame):
    """Batch operations view with full functionality"""
    
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#f5f5f5")
        self.app = app
        self.selected_files = []
        self.ollama = OllamaService()
        
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
            text="⚡ Batch Operations",
            font=("Segoe UI", 28, "bold"),
            text_color="#2E86AB"
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Perform bulk actions on multiple files simultaneously",
            font=("Segoe UI", 14),
            text_color="#666"
        )
        subtitle.pack(anchor="w", pady=(5, 0))
    
    def create_content(self):
        """Create batch operations content"""
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Step 1: Select files
        step1_frame = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=12)
        step1_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        step1_header = ctk.CTkFrame(step1_frame, fg_color="#e8f4f8", corner_radius=12)
        step1_header.pack(fill="x")
        
        step1_title = ctk.CTkLabel(
            step1_header,
            text="1️⃣ Select Files",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E86AB"
        )
        step1_title.pack(side="left", padx=20, pady=15)
        
        self.selection_label = ctk.CTkLabel(
            step1_header,
            text="No files selected",
            font=("Segoe UI", 12),
            text_color="#666"
        )
        self.selection_label.pack(side="right", padx=20)
        
        # Selection buttons
        btn_frame = ctk.CTkFrame(step1_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=15)
        
        select_all_btn = ctk.CTkButton(
            btn_frame,
            text="Select All Files",
            command=self.select_all_files,
            fg_color="#2E86AB",
            font=("Segoe UI", 13),
            height=40
        )
        select_all_btn.pack(side="left", padx=5)
        
        select_tagged_btn = ctk.CTkButton(
            btn_frame,
            text="Select Untagged",
            command=self.select_untagged,
            fg_color="white",
            text_color="#2E86AB",
            border_width=2,
            border_color="#2E86AB",
            font=("Segoe UI", 13),
            height=40
        )
        select_tagged_btn.pack(side="left", padx=5)
        
        select_type_btn = ctk.CTkButton(
            btn_frame,
            text="Select by Type...",
            command=self.select_by_type,
            fg_color="white",
            text_color="#2E86AB",
            border_width=2,
            border_color="#2E86AB",
            font=("Segoe UI", 13),
            height=40
        )
        select_type_btn.pack(side="left", padx=5)
        
        clear_btn = ctk.CTkButton(
            btn_frame,
            text="Clear Selection",
            command=self.clear_selection,
            fg_color="#f9f9f9",
            text_color="#666",
            font=("Segoe UI", 13),
            height=40
        )
        clear_btn.pack(side="right", padx=5)
        
        # Step 2: Choose operation
        step2_title = ctk.CTkLabel(
            content_frame,
            text="2️⃣ Choose Operation",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E86AB",
            anchor="w"
        )
        step2_title.grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 15))
        
        # Operation cards
        operations = [
            ("🏷️ Batch Tagging", "Add tags to multiple files at once", 
             self.batch_tag, "#2E86AB"),
            ("📂 Batch Move", "Move selected files to a folder", 
             self.batch_move, "#6A994E"),
            ("🤖 AI Categorize", "Auto-categorize files using AI", 
             self.batch_categorize, "#FF9800"),
            ("🗑️ Batch Delete", "Remove files from database", 
             self.batch_delete, "#EF4444"),
        ]
        
        ops_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        ops_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        ops_frame.grid_columnconfigure((0, 1), weight=1)
        
        for i, (title, desc, command, color) in enumerate(operations):
            row = i // 2
            col = i % 2
            
            card = ctk.CTkFrame(ops_frame, fg_color=color, corner_radius=12, cursor="hand2")
            card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)
            card.bind("<Button-1>", lambda e, c=command: c())
            
            card_title = ctk.CTkLabel(
                card,
                text=title,
                font=("Segoe UI", 16, "bold"),
                text_color="white"
            )
            card_title.pack(padx=20, pady=(20, 5), anchor="w")
            card_title.bind("<Button-1>", lambda e, c=command: c())
            
            card_desc = ctk.CTkLabel(
                card,
                text=desc,
                font=("Segoe UI", 12),
                text_color="rgba(255,255,255,0.9)"
            )
            card_desc.pack(padx=20, pady=(0, 20), anchor="w")
            card_desc.bind("<Button-1>", lambda e, c=command: c())
        
        # Progress section (hidden initially)
        self.progress_frame = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=12)
        self.progress_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(15, 0))
        self.progress_frame.grid_remove()
        
        self.progress_title = ctk.CTkLabel(
            self.progress_frame,
            text="Processing...",
            font=("Segoe UI", 14, "bold"),
            text_color="#2E86AB"
        )
        self.progress_title.pack(pady=(15, 5))
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, width=400)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
        
        self.progress_status = ctk.CTkLabel(
            self.progress_frame,
            text="",
            font=("Segoe UI", 11),
            text_color="#666"
        )
        self.progress_status.pack(pady=(0, 15))
    
    def select_all_files(self):
        """Select all files in database"""
        self.selected_files = FileService.get_all_files()
        self.update_selection_label()
    
    def select_untagged(self):
        """Select files without tags"""
        all_files = FileService.get_all_files()
        self.selected_files = [f for f in all_files if not f.tags]
        self.update_selection_label()
    
    def select_by_type(self):
        """Show dialog to select by file type"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Select by Type")
        dialog.geometry("300x400")
        dialog.transient(self)
        dialog.grab_set()
        
        # File types
        all_files = FileService.get_all_files()
        types = {}
        for f in all_files:
            ext = f.extension or 'Unknown'
            types[ext] = types.get(ext, 0) + 1
        
        label = ctk.CTkLabel(dialog, text="Select file types:", font=("Segoe UI", 14, "bold"))
        label.pack(pady=15)
        
        scroll = ctk.CTkScrollableFrame(dialog)
        scroll.pack(fill="both", expand=True, padx=20)
        
        selected_types = []
        
        for ext, count in sorted(types.items(), key=lambda x: -x[1]):
            var = ctk.StringVar(value="off")
            cb = ctk.CTkCheckBox(
                scroll,
                text=f"{ext} ({count} files)",
                variable=var,
                onvalue="on",
                offvalue="off"
            )
            cb.pack(anchor="w", pady=3)
            selected_types.append((ext, var))
        
        def apply():
            chosen = [ext for ext, var in selected_types if var.get() == "on"]
            self.selected_files = [f for f in all_files if f.extension in chosen]
            self.update_selection_label()
            dialog.destroy()
        
        btn = ctk.CTkButton(dialog, text="Select", command=apply)
        btn.pack(pady=15)
    
    def clear_selection(self):
        """Clear file selection"""
        self.selected_files = []
        self.update_selection_label()
    
    def update_selection_label(self):
        """Update selection count label"""
        count = len(self.selected_files)
        if count == 0:
            self.selection_label.configure(text="No files selected")
        else:
            self.selection_label.configure(text=f"{count} file(s) selected")
    
    def check_selection(self) -> bool:
        """Check if files are selected"""
        if not self.selected_files:
            messagebox.showwarning("No Selection", "Please select files first")
            return False
        return True
    
    def batch_tag(self):
        """Open batch tag dialog"""
        if not self.check_selection():
            return
        
        BatchTagDialog(self, self.selected_files, on_complete=self.clear_selection)
    
    def batch_move(self):
        """Move selected files to a folder"""
        if not self.check_selection():
            return
        
        folder = filedialog.askdirectory(title="Select Destination Folder")
        if not folder:
            return
        
        confirm = messagebox.askyesno(
            "Confirm Move",
            f"Move {len(self.selected_files)} files to:\n{folder}?"
        )
        
        if not confirm:
            return
        
        # Show progress
        self.progress_frame.grid()
        self.progress_bar.set(0)
        self.progress_title.configure(text="Moving files...")
        
        def do_move():
            success = 0
            for i, file in enumerate(self.selected_files):
                try:
                    import shutil
                    import os
                    if os.path.exists(file.path):
                        dest = os.path.join(folder, file.name)
                        shutil.move(file.path, dest)
                        
                        # Update database
                        file.path = dest
                        from app.models import get_session
                        session = get_session()
                        session.commit()
                        
                        success += 1
                except Exception as e:
                    print(f"Error moving {file.name}: {e}")
                
                progress = (i + 1) / len(self.selected_files)
                self.after(0, lambda p=progress, n=file.name: self.update_progress(p, f"Moving: {n}"))
            
            self.after(0, lambda: self.complete_operation(f"Moved {success} files"))
        
        thread = threading.Thread(target=do_move)
        thread.daemon = True
        thread.start()
    
    def batch_categorize(self):
        """Auto-categorize files using AI"""
        if not self.check_selection():
            return
        
        if not self.ollama.is_running():
            messagebox.showerror("OLLAMA Required", "Please start OLLAMA for AI categorization")
            return
        
        # Show progress
        self.progress_frame.grid()
        self.progress_bar.set(0)
        self.progress_title.configure(text="AI Categorizing files...")
        
        def do_categorize():
            success = 0
            for i, file in enumerate(self.selected_files):
                try:
                    from app.utils.content_reader import ContentReader
                    content, _ = ContentReader.read_file(file.path, max_chars=2000)
                    
                    category = self.ollama.categorize_file(file.name, content)
                    
                    if category:
                        file.category = category
                        from app.models import get_session
                        session = get_session()
                        session.commit()
                        success += 1
                except Exception as e:
                    print(f"Error categorizing {file.name}: {e}")
                
                progress = (i + 1) / len(self.selected_files)
                self.after(0, lambda p=progress, n=file.name: self.update_progress(p, f"Categorizing: {n}"))
            
            self.after(0, lambda: self.complete_operation(f"Categorized {success} files"))
        
        thread = threading.Thread(target=do_categorize)
        thread.daemon = True
        thread.start()
    
    def batch_delete(self):
        """Delete selected files from database"""
        if not self.check_selection():
            return
        
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Remove {len(self.selected_files)} files from database?\n\n"
            "Files will NOT be deleted from disk."
        )
        
        if not confirm:
            return
        
        success = 0
        for file in self.selected_files:
            if FileService.delete_file(file.id, delete_from_disk=False):
                success += 1
        
        messagebox.showinfo("Complete", f"Removed {success} files from database")
        self.clear_selection()
    
    def update_progress(self, value, status):
        """Update progress bar"""
        self.progress_bar.set(value)
        self.progress_status.configure(text=status)
    
    def complete_operation(self, message):
        """Complete operation and hide progress"""
        self.progress_frame.grid_remove()
        messagebox.showinfo("Complete", message)
        self.clear_selection()
