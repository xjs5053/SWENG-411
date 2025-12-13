"""
FileSense Views Package
"""
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
from app.views.dialogs import TagEditorDialog, FilePreviewDialog, BatchTagDialog, ConfirmDialog

__all__ = [
    'DashboardView',
    'SearchView',
    'FileBrowserView',
    'FileDetailView',
    'RecentFilesView',
    'TagsView',
    'BatchOperationsView',
    'AIAnalysisView',
    'SettingsView',
    'DuplicateFinderView',
    'SmartFoldersView',
    'TagEditorDialog',
    'FilePreviewDialog',
    'BatchTagDialog',
    'ConfirmDialog',
]
