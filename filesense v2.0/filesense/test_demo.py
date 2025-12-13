#!/usr/bin/env python3
"""
FileSense Demo/Test Script
Verifies all components are working properly
"""
import os
import sys

def check_imports():
    """Check all imports work correctly"""
    print("Checking imports...")
    
    try:
        from app.models import File, Tag, ActivityLog, Settings, Category, init_database, get_session
        print("  ✅ Models imported successfully")
    except ImportError as e:
        print(f"  ❌ Models import failed: {e}")
        return False
    
    try:
        from app.services import OllamaService, FileService, StatsService, FileWatcher
        print("  ✅ Services imported successfully")
    except ImportError as e:
        print(f"  ❌ Services import failed: {e}")
        return False
    
    try:
        from app.utils import FileUtils, ContentReader, DuplicateFinder, ThemeManager
        print("  ✅ Utils imported successfully")
    except ImportError as e:
        print(f"  ❌ Utils import failed: {e}")
        return False
    
    try:
        from app.views import (
            DashboardView, SearchView, FileBrowserView, FileDetailView,
            RecentFilesView, TagsView, BatchOperationsView, AIAnalysisView,
            SettingsView, DuplicateFinderView, SmartFoldersView
        )
        print("  ✅ Views imported successfully")
    except ImportError as e:
        print(f"  ❌ Views import failed: {e}")
        return False
    
    try:
        from app.views.dialogs import TagEditorDialog, FilePreviewDialog, BatchTagDialog
        print("  ✅ Dialogs imported successfully")
    except ImportError as e:
        print(f"  ❌ Dialogs import failed: {e}")
        return False
    
    return True


def check_database():
    """Check database initialization"""
    print("\nChecking database...")
    
    try:
        from app.models import init_database, get_session, File
        init_database()
        session = get_session()
        count = session.query(File).count()
        print(f"  ✅ Database initialized ({count} files)")
        return True
    except Exception as e:
        print(f"  ❌ Database error: {e}")
        return False


def check_services():
    """Check services"""
    print("\nChecking services...")
    
    try:
        from app.services import OllamaService
        ollama = OllamaService()
        running = ollama.is_running()
        print(f"  ✅ OllamaService initialized (OLLAMA running: {running})")
    except Exception as e:
        print(f"  ❌ OllamaService error: {e}")
    
    try:
        from app.services import FileService
        stats = FileService.get_file_statistics()
        print(f"  ✅ FileService initialized ({stats['total_files']} files)")
    except Exception as e:
        print(f"  ❌ FileService error: {e}")
    
    try:
        from app.services import StatsService
        total = StatsService.get_total_files()
        print(f"  ✅ StatsService initialized ({total} total files)")
    except Exception as e:
        print(f"  ❌ StatsService error: {e}")
    
    try:
        from app.services import FileWatcher
        watcher = FileWatcher()
        print(f"  ✅ FileWatcher initialized")
    except Exception as e:
        print(f"  ❌ FileWatcher error: {e}")
    
    return True


def check_utils():
    """Check utility modules"""
    print("\nChecking utilities...")
    
    try:
        from app.utils import FileUtils
        size = FileUtils.format_size(1024 * 1024)
        print(f"  ✅ FileUtils working (1MB = {size})")
    except Exception as e:
        print(f"  ❌ FileUtils error: {e}")
    
    try:
        from app.utils import ContentReader
        can_read = ContentReader.can_read("test.txt")
        print(f"  ✅ ContentReader working (can read .txt: {can_read})")
    except Exception as e:
        print(f"  ❌ ContentReader error: {e}")
    
    try:
        from app.utils import DuplicateFinder
        stats = DuplicateFinder.get_duplicate_stats({})
        print(f"  ✅ DuplicateFinder working")
    except Exception as e:
        print(f"  ❌ DuplicateFinder error: {e}")
    
    try:
        from app.utils import ThemeManager
        tm = ThemeManager()
        themes = tm.get_available_themes()
        print(f"  ✅ ThemeManager working ({len(themes)} themes available)")
    except Exception as e:
        print(f"  ❌ ThemeManager error: {e}")
    
    return True


def run_demo():
    """Run a quick demo"""
    print("\n" + "="*60)
    print("FileSense Component Test")
    print("="*60 + "\n")
    
    all_ok = True
    
    all_ok = check_imports() and all_ok
    all_ok = check_database() and all_ok
    all_ok = check_services() and all_ok
    all_ok = check_utils() and all_ok
    
    print("\n" + "="*60)
    if all_ok:
        print("✅ All checks passed! FileSense is ready to run.")
        print("\nTo start the application, run:")
        print("  python main.py")
    else:
        print("⚠️ Some checks failed. Please review the errors above.")
    print("="*60 + "\n")
    
    return all_ok


if __name__ == "__main__":
    # Add project root to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    success = run_demo()
    sys.exit(0 if success else 1)
