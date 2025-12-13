"""
File Service for file operations and management
"""
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Callable, Dict
from sqlalchemy import func
from app.models import File, Tag, ActivityLog, get_session


class FileService:
    """Service for managing files in the database"""
    
    # Supported file extensions
    SUPPORTED_EXTENSIONS = {
        '.txt', '.md', '.json', '.xml', '.csv', '.log',
        '.py', '.js', '.ts', '.jsx', '.tsx', '.cs', '.java', '.cpp', '.c', '.h',
        '.html', '.css', '.scss', '.sass',
        '.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt',
        '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp',
        '.mp3', '.wav', '.mp4', '.avi', '.mkv',
        '.zip', '.rar', '.7z', '.tar', '.gz'
    }
    
    @staticmethod
    def scan_folder(folder_path: str, progress_callback: Optional[Callable] = None) -> List[File]:
        """Scan a folder and add files to database"""
        session = get_session()
        added_files = []
        
        if not os.path.exists(folder_path):
            return added_files
        
        folder = Path(folder_path)
        
        # Get all files recursively
        try:
            all_files = list(folder.rglob('*'))
        except PermissionError:
            print(f"Permission denied: {folder_path}")
            return added_files
        
        total_files = len([f for f in all_files if f.is_file()])
        processed = 0
        
        for file_path in all_files:
            if file_path.is_file() and file_path.suffix.lower() in FileService.SUPPORTED_EXTENSIONS:
                try:
                    processed += 1
                    
                    if progress_callback:
                        progress_callback(processed, total_files, file_path.name)
                    
                    # Check if already exists
                    existing = session.query(File).filter_by(path=str(file_path)).first()
                    if existing:
                        continue
                    
                    stat = file_path.stat()
                    
                    new_file = File(
                        name=file_path.name,
                        path=str(file_path),
                        extension=file_path.suffix,
                        size=stat.st_size,
                        date_added=datetime.utcnow(),
                        last_modified=datetime.fromtimestamp(stat.st_mtime),
                        last_accessed=datetime.fromtimestamp(stat.st_atime)
                    )
                    
                    session.add(new_file)
                    session.commit()
                    
                    # Log activity
                    activity = ActivityLog(
                        file_id=new_file.id,
                        activity_type='Added',
                        description=f'File added to database from {folder_path}'
                    )
                    session.add(activity)
                    session.commit()
                    
                    added_files.append(new_file)
                    
                except PermissionError:
                    continue
                except Exception as e:
                    print(f"Error adding {file_path}: {e}")
                    session.rollback()
        
        return added_files
    
    @staticmethod
    def add_file(file_path: str) -> Optional[File]:
        """Add a single file to the database"""
        session = get_session()
        
        if not os.path.exists(file_path):
            return None
        
        path = Path(file_path)
        
        # Check if already exists
        existing = session.query(File).filter_by(path=str(path)).first()
        if existing:
            return existing
        
        try:
            stat = path.stat()
            
            new_file = File(
                name=path.name,
                path=str(path),
                extension=path.suffix,
                size=stat.st_size,
                date_added=datetime.utcnow(),
                last_modified=datetime.fromtimestamp(stat.st_mtime),
                last_accessed=datetime.fromtimestamp(stat.st_atime)
            )
            
            session.add(new_file)
            session.commit()
            
            # Log activity
            activity = ActivityLog(
                file_id=new_file.id,
                activity_type='Added',
                description='File added to database'
            )
            session.add(activity)
            session.commit()
            
            return new_file
            
        except Exception as e:
            print(f"Error adding file: {e}")
            session.rollback()
            return None
    
    @staticmethod
    def get_all_files() -> List[File]:
        """Get all files from database"""
        session = get_session()
        return session.query(File).all()
    
    @staticmethod
    def get_file_by_id(file_id: int) -> Optional[File]:
        """Get file by ID"""
        session = get_session()
        return session.query(File).get(file_id)
    
    @staticmethod
    def search_files(query: str) -> List[File]:
        """Search files by name or tags"""
        session = get_session()
        
        # Search by name
        files = session.query(File).filter(
            File.name.like(f'%{query}%')
        ).all()
        
        # Also search by tags
        tagged_files = session.query(File).join(Tag).filter(
            Tag.tag.like(f'%{query}%')
        ).all()
        
        # Combine and deduplicate
        all_files = list(set(files + tagged_files))
        return all_files
    
    @staticmethod
    def get_recent_files(limit: int = 20) -> List[File]:
        """Get recently accessed files"""
        session = get_session()
        return session.query(File).order_by(
            File.last_accessed.desc()
        ).limit(limit).all()
    
    @staticmethod
    def get_files_by_tag(tag: str) -> List[File]:
        """Get files with specific tag"""
        session = get_session()
        return session.query(File).join(Tag).filter(
            Tag.tag == tag
        ).all()
    
    @staticmethod
    def add_tags_to_file(file_id: int, tags: List[str]) -> bool:
        """Add tags to a file"""
        session = get_session()
        file = session.query(File).get(file_id)
        
        if not file:
            return False
        
        try:
            for tag_name in tags:
                # Check if tag already exists
                existing_tag = session.query(Tag).filter_by(
                    file_id=file_id,
                    tag=tag_name
                ).first()
                
                if not existing_tag:
                    tag = Tag(file_id=file_id, tag=tag_name)
                    session.add(tag)
            
            session.commit()
            
            # Log activity
            activity = ActivityLog(
                file_id=file_id,
                activity_type='Tagged',
                description=f'Added tags: {", ".join(tags)}'
            )
            session.add(activity)
            session.commit()
            
            return True
        except Exception as e:
            print(f"Error adding tags: {e}")
            session.rollback()
            return False
    
    @staticmethod
    def remove_tag_from_file(file_id: int, tag_name: str) -> bool:
        """Remove a tag from a file"""
        session = get_session()
        
        try:
            tag = session.query(Tag).filter_by(
                file_id=file_id,
                tag=tag_name
            ).first()
            
            if tag:
                session.delete(tag)
                session.commit()
                
                # Log activity
                activity = ActivityLog(
                    file_id=file_id,
                    activity_type='Untagged',
                    description=f'Removed tag: {tag_name}'
                )
                session.add(activity)
                session.commit()
                
                return True
        except Exception as e:
            print(f"Error removing tag: {e}")
            session.rollback()
        
        return False
    
    @staticmethod
    def update_summary(file_id: int, summary: str, ai_summary: bool = False) -> bool:
        """Update file summary"""
        session = get_session()
        file = session.query(File).get(file_id)
        
        if not file:
            return False
        
        try:
            if ai_summary:
                file.ai_summary = summary
            else:
                file.summary = summary
            
            session.commit()
            
            # Log activity
            activity = ActivityLog(
                file_id=file_id,
                activity_type='Updated',
                description='Summary updated'
            )
            session.add(activity)
            session.commit()
            
            return True
        except Exception as e:
            print(f"Error updating summary: {e}")
            session.rollback()
            return False
    
    @staticmethod
    def move_file(file_id: int, new_path: str) -> bool:
        """Move a file to a new location"""
        session = get_session()
        file = session.query(File).get(file_id)
        
        if not file or not os.path.exists(file.path):
            return False
        
        try:
            # Create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            
            # Move the file
            shutil.move(file.path, new_path)
            
            # Update database
            file.path = new_path
            file.name = os.path.basename(new_path)
            session.commit()
            
            # Log activity
            activity = ActivityLog(
                file_id=file_id,
                activity_type='Moved',
                description=f'File moved to {new_path}'
            )
            session.add(activity)
            session.commit()
            
            return True
        except Exception as e:
            print(f"Error moving file: {e}")
            session.rollback()
            return False
    
    @staticmethod
    def delete_file(file_id: int, delete_from_disk: bool = False) -> bool:
        """Delete a file from database (and optionally from disk)"""
        session = get_session()
        file = session.query(File).get(file_id)
        
        if not file:
            return False
        
        try:
            if delete_from_disk and os.path.exists(file.path):
                os.remove(file.path)
            
            session.delete(file)
            session.commit()
            
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            session.rollback()
            return False
    
    @staticmethod
    def read_file_content(file_path: str, max_bytes: int = 10000) -> str:
        """Read file content (text files only)"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(max_bytes)
            return content
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""
    
    @staticmethod
    def get_file_statistics() -> Dict:
        """Get file statistics"""
        session = get_session()
        
        total_files = session.query(File).count()
        total_size = session.query(File).with_entities(
            func.sum(File.size)
        ).scalar() or 0
        
        tagged_files = session.query(File).join(Tag).distinct().count()
        
        return {
            'total_files': total_files,
            'total_size': total_size,
            'tagged_files': tagged_files,
            'untagged_files': total_files - tagged_files
        }
    
    @staticmethod
    def batch_add_tags(file_ids: List[int], tags: List[str]) -> int:
        """Add tags to multiple files"""
        session = get_session()
        success_count = 0
        
        for file_id in file_ids:
            if FileService.add_tags_to_file(file_id, tags):
                success_count += 1
        
        return success_count
    
    @staticmethod
    def batch_move_files(file_ids: List[int], destination: str) -> int:
        """Move multiple files to a destination"""
        success_count = 0
        
        for file_id in file_ids:
            file = FileService.get_file_by_id(file_id)
            if file:
                new_path = os.path.join(destination, file.name)
                if FileService.move_file(file_id, new_path):
                    success_count += 1
        
        return success_count
    
    @staticmethod
    def import_file(file_path: str) -> Optional[File]:
        """Import a file to the database (alias for add_file with logging)"""
        return FileService.add_file(file_path)
    
    @staticmethod
    def get_files_by_extension(extension: str) -> List[File]:
        """Get all files with a specific extension"""
        session = get_session()
        return session.query(File).filter(
            File.extension == extension
        ).all()
    
    @staticmethod
    def get_files_by_category(category: str) -> List[File]:
        """Get all files in a specific category"""
        session = get_session()
        return session.query(File).filter(
            File.category == category
        ).all()
    
    @staticmethod
    def update_file_category(file_id: int, category: str) -> bool:
        """Update file category"""
        session = get_session()
        file = session.query(File).get(file_id)
        
        if not file:
            return False
        
        try:
            file.category = category
            session.commit()
            
            # Log activity
            activity = ActivityLog(
                file_id=file_id,
                activity_type='Categorized',
                description=f'Category set to: {category}'
            )
            session.add(activity)
            session.commit()
            
            return True
        except Exception as e:
            print(f"Error updating category: {e}")
            session.rollback()
            return False
    
    @staticmethod
    def get_all_tags() -> List[str]:
        """Get all unique tags"""
        session = get_session()
        tags = session.query(Tag.tag).distinct().all()
        return [t[0] for t in tags]
    
    @staticmethod
    def get_tag_counts() -> Dict[str, int]:
        """Get tag usage counts"""
        session = get_session()
        result = session.query(
            Tag.tag,
            func.count(Tag.id)
        ).group_by(Tag.tag).all()
        
        return {tag: count for tag, count in result}
    
    @staticmethod
    def get_files_without_tags() -> List[File]:
        """Get files that have no tags"""
        session = get_session()
        return session.query(File).outerjoin(Tag).filter(
            Tag.id == None
        ).all()
    
    @staticmethod
    def get_files_without_summary() -> List[File]:
        """Get files that have no summary"""
        session = get_session()
        return session.query(File).filter(
            (File.summary == None) | (File.summary == ''),
            (File.ai_summary == None) | (File.ai_summary == '')
        ).all()
    
    @staticmethod
    def refresh_file_metadata(file_id: int) -> bool:
        """Refresh file metadata from disk"""
        session = get_session()
        file = session.query(File).get(file_id)
        
        if not file or not os.path.exists(file.path):
            return False
        
        try:
            path = Path(file.path)
            stat = path.stat()
            
            file.size = stat.st_size
            file.last_modified = datetime.fromtimestamp(stat.st_mtime)
            file.last_accessed = datetime.fromtimestamp(stat.st_atime)
            
            session.commit()
            return True
        except Exception as e:
            print(f"Error refreshing metadata: {e}")
            session.rollback()
            return False
