"""
FileSense Services Package
"""
from app.services.ollama_service import OllamaService
from app.services.file_service import FileService
from app.services.stats_service import StatsService
from app.services.file_watcher import FileWatcher, SmartFolderMonitor, WatchedFolder

__all__ = [
    'OllamaService',
    'FileService',
    'StatsService',
    'FileWatcher',
    'SmartFolderMonitor',
    'WatchedFolder'
]
