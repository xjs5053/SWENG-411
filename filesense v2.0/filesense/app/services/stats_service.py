"""
Statistics Service for dashboard analytics
"""
from sqlalchemy import func
from sqlalchemy.sql import func as sql_func
from datetime import datetime, timedelta
from typing import Dict, List
from app.models import File, Tag, ActivityLog, get_session


class StatsService:
    """Service for calculating file statistics"""
    
    @staticmethod
    def get_total_files() -> int:
        """Get total number of files"""
        session = get_session()
        return session.query(File).count()
    
    @staticmethod
    def get_total_size() -> int:
        """Get total size of all files in bytes"""
        session = get_session()
        total = session.query(func.sum(File.size)).scalar()
        return total if total else 0
    
    @staticmethod
    def get_tagged_files_count() -> int:
        """Get number of tagged files"""
        session = get_session()
        return session.query(File).join(Tag).distinct().count()
    
    @staticmethod
    def get_untagged_files_count() -> int:
        """Get number of untagged files"""
        return StatsService.get_total_files() - StatsService.get_tagged_files_count()
    
    @staticmethod
    def get_file_type_distribution() -> Dict[str, int]:
        """Get distribution of file types"""
        session = get_session()
        
        results = session.query(
            File.extension,
            func.count(File.id)
        ).group_by(File.extension).all()
        
        distribution = {}
        for ext, count in results:
            ext_clean = ext.upper().lstrip('.') if ext else 'Unknown'
            distribution[ext_clean] = count
        
        return distribution
    
    @staticmethod
    def get_recent_activity(limit: int = 10) -> List[ActivityLog]:
        """Get recent file activities"""
        session = get_session()
        return session.query(ActivityLog).order_by(
            ActivityLog.timestamp.desc()
        ).limit(limit).all()
    
    @staticmethod
    def get_files_added_today() -> int:
        """Get number of files added today"""
        session = get_session()
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        return session.query(File).filter(
            File.date_added >= today_start
        ).count()
    
    @staticmethod
    def get_files_added_this_week() -> int:
        """Get number of files added this week"""
        session = get_session()
        week_start = datetime.utcnow() - timedelta(days=7)
        
        return session.query(File).filter(
            File.date_added >= week_start
        ).count()
    
    @staticmethod
    def get_popular_tags(limit: int = 10) -> List[tuple]:
        """Get most popular tags"""
        session = get_session()
        
        results = session.query(
            Tag.tag,
            func.count(Tag.id).label('count')
        ).group_by(Tag.tag).order_by(
            func.count(Tag.id).desc()
        ).limit(limit).all()
        
        return results
    
    @staticmethod
    def get_largest_files(limit: int = 10) -> List[File]:
        """Get largest files"""
        session = get_session()
        return session.query(File).order_by(
            File.size.desc()
        ).limit(limit).all()
    
    @staticmethod
    def get_category_distribution() -> Dict[str, int]:
        """Get distribution of file categories"""
        session = get_session()
        
        results = session.query(
            File.category,
            func.count(File.id)
        ).group_by(File.category).all()
        
        distribution = {}
        for category, count in results:
            cat_name = category if category else 'Uncategorized'
            distribution[cat_name] = count
        
        return distribution
    
    @staticmethod
    def get_summary_stats() -> Dict:
        """Get comprehensive summary statistics"""
        total_files = StatsService.get_total_files()
        total_size = StatsService.get_total_size()
        
        # Format size
        if total_size < 1024 * 1024:
            size_formatted = f"{total_size / 1024:.1f} KB"
        elif total_size < 1024 * 1024 * 1024:
            size_formatted = f"{total_size / (1024 * 1024):.1f} MB"
        else:
            size_formatted = f"{total_size / (1024 * 1024 * 1024):.2f} GB"
        
        return {
            'total_files': total_files,
            'total_size': total_size,
            'size_formatted': size_formatted,
            'tagged_files': StatsService.get_tagged_files_count(),
            'untagged_files': StatsService.get_untagged_files_count(),
            'added_today': StatsService.get_files_added_today(),
            'added_this_week': StatsService.get_files_added_this_week(),
            'file_types': len(StatsService.get_file_type_distribution()),
        }
