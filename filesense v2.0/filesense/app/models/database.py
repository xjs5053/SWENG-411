"""
Database models for FileSense
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os

Base = declarative_base()


class File(Base):
    """File model for storing file metadata"""
    __tablename__ = 'files'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    path = Column(String(500), unique=True, nullable=False)
    extension = Column(String(10))
    size = Column(Integer)
    date_added = Column(DateTime, default=datetime.utcnow)
    last_modified = Column(DateTime, default=datetime.utcnow)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    summary = Column(Text)
    ai_summary = Column(Text)
    author = Column(String(100))
    category = Column(String(50))
    is_favorite = Column(Boolean, default=False)
    
    tags = relationship('Tag', back_populates='file', cascade='all, delete-orphan')
    activities = relationship('ActivityLog', back_populates='file', cascade='all, delete-orphan')
    
    @property
    def size_formatted(self):
        """Format file size in human-readable format"""
        if self.size is None:
            return "Unknown"
        if self.size < 1024:
            return f"{self.size} B"
        elif self.size < 1024 * 1024:
            return f"{self.size / 1024:.1f} KB"
        elif self.size < 1024 * 1024 * 1024:
            return f"{self.size / (1024 * 1024):.1f} MB"
        else:
            return f"{self.size / (1024 * 1024 * 1024):.2f} GB"
    
    @property
    def file_type_icon(self):
        """Get icon for file type"""
        ext = (self.extension or '').lower()
        icons = {
            '.docx': '📄', '.doc': '📄', '.odt': '📄', '.rtf': '📄',
            '.xlsx': '📊', '.xls': '📊', '.csv': '📊', '.ods': '📊',
            '.pptx': '📽️', '.ppt': '📽️', '.odp': '📽️',
            '.pdf': '📑',
            '.txt': '📝', '.md': '📝', '.log': '📝',
            '.png': '🖼️', '.jpg': '🖼️', '.jpeg': '🖼️', '.gif': '🖼️', '.svg': '🖼️', '.webp': '🖼️',
            '.zip': '📦', '.rar': '📦', '.7z': '📦', '.tar': '📦', '.gz': '📦',
            '.py': '🐍', '.pyc': '🐍',
            '.js': '📜', '.ts': '📜', '.jsx': '📜', '.tsx': '📜',
            '.cs': '💻', '.java': '💻', '.cpp': '💻', '.c': '💻',
            '.html': '🌐', '.css': '🎨', '.xml': '📋', '.json': '📋',
            '.mp3': '🎵', '.wav': '🎵', '.flac': '🎵',
            '.mp4': '🎬', '.avi': '🎬', '.mkv': '🎬', '.mov': '🎬',
        }
        return icons.get(ext, '📁')
    
    @property
    def file_type_name(self):
        """Get human-readable file type name"""
        ext = (self.extension or '').lower()
        types = {
            '.docx': 'Word Document', '.doc': 'Word Document',
            '.xlsx': 'Excel Spreadsheet', '.xls': 'Excel Spreadsheet', '.csv': 'CSV File',
            '.pptx': 'PowerPoint', '.ppt': 'PowerPoint',
            '.pdf': 'PDF Document',
            '.txt': 'Text File', '.md': 'Markdown', '.log': 'Log File',
            '.png': 'PNG Image', '.jpg': 'JPEG Image', '.jpeg': 'JPEG Image',
            '.zip': 'Archive', '.rar': 'Archive',
            '.py': 'Python Script', '.js': 'JavaScript', '.html': 'HTML',
        }
        return types.get(ext, ext.upper().lstrip('.') + ' File' if ext else 'File')
    
    @property
    def modified_time_ago(self):
        """Get time since last modification in human-readable format"""
        if not self.last_modified:
            return "Unknown"
        
        delta = datetime.utcnow() - self.last_modified
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
        else:
            return self.last_modified.strftime("%b %d, %Y")
    
    @property
    def tag_list(self):
        """Get list of tag names"""
        return [tag.tag for tag in self.tags]
    
    def __repr__(self):
        return f"<File(id={self.id}, name='{self.name}')>"


class Tag(Base):
    """Tag model for categorizing files"""
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.id'), nullable=False)
    tag = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    file = relationship('File', back_populates='tags')
    
    def __repr__(self):
        return f"<Tag(id={self.id}, tag='{self.tag}')>"


class ActivityLog(Base):
    """Activity log for tracking file operations"""
    __tablename__ = 'activity_log'
    
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.id'), nullable=False)
    activity_type = Column(String(50), nullable=False)
    description = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    file = relationship('File', back_populates='activities')
    
    @property
    def time_ago(self):
        """Get time since activity in human-readable format"""
        if not self.timestamp:
            return "Unknown"
        
        delta = datetime.utcnow() - self.timestamp
        seconds = delta.total_seconds()
        
        if seconds < 60:
            return "Just now"
        elif seconds < 3600:
            mins = int(seconds / 60)
            return f"{mins} min{'s' if mins != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 604800:
            days = int(seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
        else:
            return self.timestamp.strftime("%b %d, %Y")
    
    def __repr__(self):
        return f"<ActivityLog(id={self.id}, type='{self.activity_type}')>"


class Settings(Base):
    """Settings model for application configuration"""
    __tablename__ = 'settings'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(50), unique=True, nullable=False)
    value = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Settings(key='{self.key}')>"


class Category(Base):
    """Category model for organizing files"""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    color = Column(String(7))  # Hex color code
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Category(name='{self.name}')>"


# Database setup
def get_database_path():
    """Get the database file path"""
    app_dir = os.path.join(os.path.expanduser('~'), '.filesense')
    os.makedirs(app_dir, exist_ok=True)
    return os.path.join(app_dir, 'filesense.db')


def init_database():
    """Initialize the database and create tables"""
    import sqlite3
    
    db_path = get_database_path()
    
    # Check if database exists and has correct schema
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if files table has ai_summary column
            cursor.execute("PRAGMA table_info(files)")
            columns = [col[1] for col in cursor.fetchall()]
            conn.close()
            
            # If table exists but missing required columns, delete and recreate
            required_columns = ['ai_summary', 'category', 'is_favorite']
            if columns:
                missing = [col for col in required_columns if col not in columns]
                if missing:
                    print(f"Database schema outdated (missing: {missing}), recreating...")
                    os.remove(db_path)
        except Exception as e:
            print(f"Error checking database: {e}")
            # If any error, try to remove and recreate
            try:
                os.remove(db_path)
                print("Removed corrupted database, will recreate.")
            except:
                pass
    
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


# Global session
_db_session = None


def get_session():
    """Get database session (singleton)"""
    global _db_session
    if _db_session is None:
        _db_session = init_database()
    return _db_session
