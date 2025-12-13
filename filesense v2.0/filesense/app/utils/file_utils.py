"""
File Utilities - Common file operations and helpers
"""
import os
import hashlib
import mimetypes
from pathlib import Path
from typing import Optional, List, Tuple
from datetime import datetime


class FileUtils:
    """Utility functions for file operations"""
    
    # File type categories
    CATEGORIES = {
        'Documents': ['.txt', '.md', '.doc', '.docx', '.odt', '.rtf', '.pdf'],
        'Spreadsheets': ['.xls', '.xlsx', '.csv', '.ods', '.tsv'],
        'Presentations': ['.ppt', '.pptx', '.odp', '.key'],
        'Code': ['.py', '.js', '.ts', '.jsx', '.tsx', '.cs', '.java', '.cpp', '.c', '.h', 
                 '.html', '.css', '.scss', '.sass', '.json', '.xml', '.yaml', '.yml',
                 '.rb', '.go', '.rs', '.php', '.swift', '.kt', '.sql', '.sh', '.bash'],
        'Images': ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp', '.ico', '.tiff'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
        'Video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
        'Data': ['.db', '.sqlite', '.sqlite3', '.json', '.xml', '.csv'],
    }
    
    @staticmethod
    def get_file_hash(file_path: str, algorithm: str = 'md5', chunk_size: int = 8192) -> Optional[str]:
        """Calculate hash of a file"""
        try:
            if algorithm == 'md5':
                hasher = hashlib.md5()
            elif algorithm == 'sha1':
                hasher = hashlib.sha1()
            elif algorithm == 'sha256':
                hasher = hashlib.sha256()
            else:
                hasher = hashlib.md5()
            
            with open(file_path, 'rb') as f:
                while chunk := f.read(chunk_size):
                    hasher.update(chunk)
            
            return hasher.hexdigest()
        except Exception as e:
            print(f"Error calculating hash: {e}")
            return None
    
    @staticmethod
    def get_file_category(extension: str) -> str:
        """Get category for a file extension"""
        ext = extension.lower()
        for category, extensions in FileUtils.CATEGORIES.items():
            if ext in extensions:
                return category
        return 'Other'
    
    @staticmethod
    def format_size(size_bytes: int) -> str:
        """Format file size in human-readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
    
    @staticmethod
    def format_date(dt: datetime, format_str: str = "%b %d, %Y %I:%M %p") -> str:
        """Format datetime to string"""
        if not dt:
            return "Unknown"
        return dt.strftime(format_str)
    
    @staticmethod
    def time_ago(dt: datetime) -> str:
        """Get human-readable time ago string"""
        if not dt:
            return "Unknown"
        
        delta = datetime.utcnow() - dt
        seconds = delta.total_seconds()
        
        if seconds < 60:
            return "Just now"
        elif seconds < 3600:
            mins = int(seconds / 60)
            return f"{mins} min{'s' if mins != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 172800:
            return "Yesterday"
        elif seconds < 604800:
            days = int(seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
        elif seconds < 2592000:
            weeks = int(seconds / 604800)
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"
        else:
            return dt.strftime("%b %d, %Y")
    
    @staticmethod
    def get_mime_type(file_path: str) -> str:
        """Get MIME type of a file"""
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type or 'application/octet-stream'
    
    @staticmethod
    def is_text_file(file_path: str) -> bool:
        """Check if file is likely a text file"""
        text_extensions = ['.txt', '.md', '.json', '.xml', '.csv', '.log',
                         '.py', '.js', '.ts', '.html', '.css', '.yaml', '.yml',
                         '.ini', '.cfg', '.conf', '.sh', '.bash', '.sql']
        ext = Path(file_path).suffix.lower()
        return ext in text_extensions
    
    @staticmethod
    def is_image_file(file_path: str) -> bool:
        """Check if file is an image"""
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp', '.ico']
        ext = Path(file_path).suffix.lower()
        return ext in image_extensions
    
    @staticmethod
    def safe_filename(filename: str) -> str:
        """Convert string to safe filename"""
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename.strip()
    
    @staticmethod
    def get_unique_filename(directory: str, filename: str) -> str:
        """Get a unique filename in directory (add number if exists)"""
        path = Path(directory)
        name = Path(filename)
        
        if not (path / filename).exists():
            return filename
        
        stem = name.stem
        suffix = name.suffix
        counter = 1
        
        while (path / f"{stem}_{counter}{suffix}").exists():
            counter += 1
        
        return f"{stem}_{counter}{suffix}"
    
    @staticmethod
    def get_directory_size(directory: str) -> int:
        """Get total size of directory in bytes"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(file_path)
                    except (OSError, IOError):
                        pass
        except Exception as e:
            print(f"Error calculating directory size: {e}")
        return total_size
    
    @staticmethod
    def count_files_in_directory(directory: str, recursive: bool = True) -> Tuple[int, int]:
        """Count files and folders in directory"""
        file_count = 0
        folder_count = 0
        
        try:
            if recursive:
                for dirpath, dirnames, filenames in os.walk(directory):
                    file_count += len(filenames)
                    folder_count += len(dirnames)
            else:
                for item in os.listdir(directory):
                    path = os.path.join(directory, item)
                    if os.path.isfile(path):
                        file_count += 1
                    elif os.path.isdir(path):
                        folder_count += 1
        except Exception as e:
            print(f"Error counting files: {e}")
        
        return file_count, folder_count
    
    @staticmethod
    def find_files_by_extension(directory: str, extensions: List[str], recursive: bool = True) -> List[str]:
        """Find all files with specific extensions"""
        files = []
        extensions = [ext.lower() for ext in extensions]
        
        try:
            if recursive:
                for dirpath, _, filenames in os.walk(directory):
                    for filename in filenames:
                        if Path(filename).suffix.lower() in extensions:
                            files.append(os.path.join(dirpath, filename))
            else:
                for item in os.listdir(directory):
                    path = os.path.join(directory, item)
                    if os.path.isfile(path) and Path(item).suffix.lower() in extensions:
                        files.append(path)
        except Exception as e:
            print(f"Error finding files: {e}")
        
        return files
    
    @staticmethod
    def get_file_info(file_path: str) -> Optional[dict]:
        """Get comprehensive file information"""
        try:
            path = Path(file_path)
            stat = path.stat()
            
            return {
                'name': path.name,
                'path': str(path.absolute()),
                'extension': path.suffix,
                'size': stat.st_size,
                'size_formatted': FileUtils.format_size(stat.st_size),
                'created': datetime.fromtimestamp(stat.st_ctime),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'accessed': datetime.fromtimestamp(stat.st_atime),
                'is_file': path.is_file(),
                'is_dir': path.is_dir(),
                'category': FileUtils.get_file_category(path.suffix),
                'mime_type': FileUtils.get_mime_type(str(path)),
            }
        except Exception as e:
            print(f"Error getting file info: {e}")
            return None
