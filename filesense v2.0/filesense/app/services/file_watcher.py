"""
File Watcher Service - Real-time folder monitoring
"""
import os
import time
import threading
from pathlib import Path
from typing import Callable, Optional, List, Set
from datetime import datetime


class FileWatcher:
    """Monitor folders for file changes in real-time"""
    
    def __init__(self):
        self.watched_folders: Set[str] = set()
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.poll_interval = 2.0  # seconds
        
        # Callbacks
        self.on_file_created: Optional[Callable[[str], None]] = None
        self.on_file_modified: Optional[Callable[[str], None]] = None
        self.on_file_deleted: Optional[Callable[[str], None]] = None
        
        # Track file states
        self._file_states: dict = {}
    
    def add_folder(self, folder_path: str):
        """Add folder to watch list"""
        if os.path.isdir(folder_path):
            self.watched_folders.add(folder_path)
            self._scan_folder(folder_path)
    
    def remove_folder(self, folder_path: str):
        """Remove folder from watch list"""
        self.watched_folders.discard(folder_path)
    
    def start(self):
        """Start watching folders"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._watch_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop watching folders"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
            self.thread = None
    
    def _scan_folder(self, folder_path: str):
        """Initial scan to build file state"""
        try:
            for root, _, files in os.walk(folder_path):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    try:
                        stat = os.stat(file_path)
                        self._file_states[file_path] = {
                            'mtime': stat.st_mtime,
                            'size': stat.st_size
                        }
                    except (OSError, IOError):
                        pass
        except Exception as e:
            print(f"Error scanning folder {folder_path}: {e}")
    
    def _watch_loop(self):
        """Main watching loop"""
        while self.running:
            try:
                self._check_for_changes()
            except Exception as e:
                print(f"Error in watch loop: {e}")
            
            time.sleep(self.poll_interval)
    
    def _check_for_changes(self):
        """Check for file changes"""
        current_files: Set[str] = set()
        
        # Scan all watched folders
        for folder in self.watched_folders.copy():
            if not os.path.exists(folder):
                continue
            
            try:
                for root, _, files in os.walk(folder):
                    for filename in files:
                        file_path = os.path.join(root, filename)
                        current_files.add(file_path)
                        
                        try:
                            stat = os.stat(file_path)
                            current_state = {
                                'mtime': stat.st_mtime,
                                'size': stat.st_size
                            }
                            
                            if file_path not in self._file_states:
                                # New file
                                self._file_states[file_path] = current_state
                                if self.on_file_created:
                                    self.on_file_created(file_path)
                            elif self._file_states[file_path] != current_state:
                                # Modified file
                                self._file_states[file_path] = current_state
                                if self.on_file_modified:
                                    self.on_file_modified(file_path)
                        except (OSError, IOError):
                            pass
            except Exception as e:
                print(f"Error scanning folder {folder}: {e}")
        
        # Check for deleted files
        deleted_files = set(self._file_states.keys()) - current_files
        for file_path in deleted_files:
            del self._file_states[file_path]
            if self.on_file_deleted:
                self.on_file_deleted(file_path)


class SmartFolderMonitor:
    """Smart folder monitoring with automatic file import"""
    
    def __init__(self, file_service):
        self.file_service = file_service
        self.watcher = FileWatcher()
        self.auto_import = True
        self.auto_tag = False
        
        # Set up callbacks
        self.watcher.on_file_created = self._on_file_created
        self.watcher.on_file_modified = self._on_file_modified
        self.watcher.on_file_deleted = self._on_file_deleted
        
        # Event callbacks for UI
        self.on_event: Optional[Callable[[str, str, str], None]] = None
    
    def add_smart_folder(self, folder_path: str):
        """Add smart folder to monitor"""
        self.watcher.add_folder(folder_path)
    
    def remove_smart_folder(self, folder_path: str):
        """Remove smart folder from monitoring"""
        self.watcher.remove_folder(folder_path)
    
    def start(self):
        """Start monitoring"""
        self.watcher.start()
    
    def stop(self):
        """Stop monitoring"""
        self.watcher.stop()
    
    def _on_file_created(self, file_path: str):
        """Handle new file detected"""
        if self.auto_import:
            try:
                # Import file to database
                self.file_service.import_file(file_path)
                self._notify("created", file_path, "File imported automatically")
            except Exception as e:
                print(f"Error auto-importing file: {e}")
    
    def _on_file_modified(self, file_path: str):
        """Handle file modification"""
        self._notify("modified", file_path, "File was modified")
    
    def _on_file_deleted(self, file_path: str):
        """Handle file deletion"""
        self._notify("deleted", file_path, "File was deleted")
    
    def _notify(self, event_type: str, file_path: str, message: str):
        """Send notification"""
        if self.on_event:
            self.on_event(event_type, file_path, message)


class WatchedFolder:
    """Represents a watched folder configuration"""
    
    def __init__(self, path: str, recursive: bool = True, 
                 extensions: Optional[List[str]] = None,
                 auto_tag: bool = False):
        self.path = path
        self.recursive = recursive
        self.extensions = extensions or []
        self.auto_tag = auto_tag
        self.enabled = True
        self.last_scan = None
    
    def should_include(self, file_path: str) -> bool:
        """Check if file should be included based on filters"""
        if not self.enabled:
            return False
        
        if self.extensions:
            ext = Path(file_path).suffix.lower()
            if ext not in self.extensions:
                return False
        
        return True
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage"""
        return {
            'path': self.path,
            'recursive': self.recursive,
            'extensions': self.extensions,
            'auto_tag': self.auto_tag,
            'enabled': self.enabled
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'WatchedFolder':
        """Create from dictionary"""
        folder = cls(
            path=data['path'],
            recursive=data.get('recursive', True),
            extensions=data.get('extensions', []),
            auto_tag=data.get('auto_tag', False)
        )
        folder.enabled = data.get('enabled', True)
        return folder
