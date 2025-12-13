# FileSense Project Structure

This document provides a detailed overview of the FileSense project structure and architecture.

## Directory Structure

```
filesense/
│
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   │
│   ├── models/                   # Data models and database
│   │   ├── __init__.py          # Models package initialization
│   │   └── database.py          # SQLAlchemy models and database setup
│   │
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py          # Services package initialization
│   │   ├── ollama_service.py    # OLLAMA AI integration service
│   │   ├── file_service.py      # File operations and management
│   │   └── stats_service.py     # Statistics and analytics
│   │
│   └── views/                    # UI components (CustomTkinter)
│       ├── __init__.py          # Views package initialization
│       ├── dashboard.py         # Main dashboard view
│       ├── search.py            # File search view
│       ├── file_browser.py      # File browser and management
│       ├── file_detail.py       # Detailed file information
│       ├── recent_files.py      # Recently accessed files
│       ├── tags.py              # Tag management
│       ├── batch_operations.py  # Batch file operations
│       ├── ai_analysis.py       # AI-powered file analysis
│       └── settings.py          # Application settings
│
├── docs/                         # Documentation
│   ├── INSTALLATION.md          # Installation guide
│   ├── QUICKSTART.md            # Quick start guide
│   └── PROJECT_STRUCTURE.md     # This file
│
├── assets/                       # Static assets (future use)
│   └── logo.png                 # Application logo
│
├── main.py                       # Application entry point
├── setup.py                      # Setup and installation script
├── requirements.txt              # Python dependencies
│
├── run.bat                       # Windows launcher
├── run.sh                        # Linux launcher
│
├── README.md                     # Main documentation
├── LICENSE                       # MIT License
└── .gitignore                    # Git ignore rules

```

## Core Components

### 1. Main Application (`main.py`)

**Purpose**: Application entry point and main window management

**Key Features**:
- Creates main application window
- Manages sidebar navigation
- Handles view switching
- Initializes database

**Main Class**: `FileSenseApp(ctk.CTk)`

### 2. Data Models (`app/models/`)

#### `database.py`

**Models**:
- `File`: Stores file metadata
  - id, name, path, extension, size
  - date_added, last_modified, last_accessed
  - summary, ai_summary, author, category
  - Properties: size_formatted, file_type_icon, etc.

- `Tag`: File tagging system
  - id, file_id, tag, created_at

- `ActivityLog`: Tracks file operations
  - id, file_id, activity_type, description, timestamp

- `Settings`: Application configuration
  - id, key, value, updated_at

- `Category`: File categories
  - id, name, color, description

**Database**: SQLite at `~/.filesense/filesense.db`

### 3. Services Layer (`app/services/`)

#### `ollama_service.py` - AI Integration

**Purpose**: Interface with OLLAMA for AI operations

**Key Methods**:
- `is_running()`: Check OLLAMA status
- `get_available_models()`: List installed models
- `generate_tags(text, model)`: Generate file tags
- `generate_summary(text, model)`: Create summaries
- `extract_insights(text, model)`: Extract key insights
- `categorize_file(filename, content)`: Auto-categorize files
- `analyze_file_content(content)`: Comprehensive analysis

**Configuration**: Default URL `http://localhost:11434`

#### `file_service.py` - File Operations

**Purpose**: Manage file database and operations

**Key Methods**:
- `scan_folder(path, callback)`: Recursively scan folder
- `add_file(path)`: Add single file
- `get_all_files()`: Retrieve all files
- `search_files(query)`: Search by name/tags
- `get_recent_files(limit)`: Get recent files
- `add_tags_to_file(file_id, tags)`: Add tags
- `move_file(file_id, new_path)`: Move file
- `delete_file(file_id, delete_from_disk)`: Delete file
- `batch_add_tags(file_ids, tags)`: Batch operations

**Supported Extensions**: 40+ file types including:
- Documents: .txt, .md, .doc, .docx, .pdf
- Code: .py, .js, .ts, .cs, .java, .cpp
- Media: .png, .jpg, .mp3, .mp4
- Archives: .zip, .rar, .7z

#### `stats_service.py` - Analytics

**Purpose**: Calculate statistics for dashboard

**Key Methods**:
- `get_total_files()`: Total file count
- `get_total_size()`: Total size in bytes
- `get_tagged_files_count()`: Tagged files count
- `get_file_type_distribution()`: File type breakdown
- `get_recent_activity(limit)`: Recent operations
- `get_popular_tags(limit)`: Most used tags
- `get_summary_stats()`: Comprehensive statistics

### 4. UI Views (`app/views/`)

All views inherit from `ctk.CTkFrame` and follow consistent patterns:

#### `dashboard.py` - Main Dashboard
- File statistics cards
- Recent files list
- Popular tags
- Search bar

#### `file_browser.py` - File Browser
- Folder scanning
- File list with sorting
- Multi-select with checkboxes
- Batch operations toolbar
- List/grid view modes

#### `ai_analysis.py` - AI Analysis
- OLLAMA status indicator
- File selection
- Analysis options (summary, tags, insights, category)
- Model selection
- Results display with actions
- Apply tags/save summary

#### `search.py` - Search Files
- Real-time search
- Results display
- Click to view details

#### `file_detail.py` - File Details
- Comprehensive file info
- Properties table
- Tags display
- Summary display
- Open/Edit actions

#### `recent_files.py` - Recent Files
- Filter tabs
- File list
- Quick access

#### `tags.py` - Tag Management
- All tags with counts
- Click to filter

#### `batch_operations.py` - Batch Operations
- Batch tagging
- Batch moving
- AI categorization

#### `settings.py` - Settings
- OLLAMA configuration
- Appearance settings
- Test connection

## Data Flow

### File Scanning Flow
```
User clicks "Scan Folder"
    ↓
file_browser.py → scan_folder()
    ↓
file_service.py → scan_folder()
    ↓
For each file:
    - Create File model
    - Save to database
    - Log activity
    ↓
Update UI with results
```

### AI Analysis Flow
```
User selects file and starts analysis
    ↓
ai_analysis.py → start_analysis()
    ↓
Background thread:
    - Read file content
    - Call OLLAMA service
    - Generate summary/tags/insights
    ↓
ollama_service.py → API calls to OLLAMA
    ↓
Process results
    ↓
Update UI with results
    ↓
User applies tags/saves summary
    ↓
file_service.py → update database
```

### Search Flow
```
User enters search query
    ↓
search.py → perform_search()
    ↓
file_service.py → search_files()
    ↓
Query database:
    - Search by filename
    - Search by tags
    - Combine results
    ↓
Display results in UI
```

## Design Patterns

### MVC-Like Architecture
- **Models** (`app/models/`): Data structures and database
- **Views** (`app/views/`): UI components
- **Controllers/Services** (`app/services/`): Business logic

### Service Layer Pattern
- Services encapsulate business logic
- Views call services for operations
- Services interact with models
- Clean separation of concerns

### Repository Pattern
- `file_service.py` acts as repository
- Abstract database operations
- Provide high-level API

## Key Technologies

### UI Framework
- **CustomTkinter 5.2.0+**: Modern, customizable Tkinter
- Responsive design
- Custom styling
- Cross-platform

### Database
- **SQLAlchemy 2.0.0+**: ORM for database operations
- SQLite backend
- Migrations not needed (auto-create)

### AI Integration
- **OLLAMA**: Local AI models
- REST API communication
- **Requests 2.31.0+**: HTTP library

### File Handling
- **Pillow 10.0.0+**: Image processing
- **PyPDF2**: PDF reading
- **python-docx**: Word documents
- **openpyxl**: Excel files

## Extension Points

### Adding New File Types
1. Add extension to `FileService.SUPPORTED_EXTENSIONS`
2. Add icon mapping in `File.file_type_icon` property
3. Add reader function if needed

### Adding New AI Features
1. Add method to `OllamaService`
2. Update `ai_analysis.py` view
3. Add analysis option checkbox
4. Handle results in `display_results()`

### Adding New Views
1. Create view file in `app/views/`
2. Inherit from `ctk.CTkFrame`
3. Implement `__init__`, `create_header`, `create_content`
4. Add navigation button in `main.py`
5. Add show method in `FileSenseApp`

### Adding Database Models
1. Define model in `app/models/database.py`
2. Inherit from `Base`
3. Define columns
4. Add relationships
5. Database auto-updates on first run

## Best Practices

### Code Style
- Follow PEP 8
- Use type hints
- Docstrings for functions/classes
- Meaningful variable names

### Error Handling
- Try-except blocks for I/O operations
- Log errors to console
- Show user-friendly messages
- Never crash on errors

### UI Guidelines
- Consistent color scheme (#2E86AB blue, #FFD93D yellow)
- "Segoe UI" font family
- Proper padding and spacing
- Responsive layouts

### Database
- Always use sessions from `get_session()`
- Commit after changes
- Rollback on errors
- Use relationships for joins

## Performance Considerations

### File Scanning
- Progress callbacks for long operations
- Background threads for heavy work
- Batch database commits

### AI Operations
- Background threads mandatory
- Timeout handling
- Partial results on failure
- Model selection affects speed

### UI Responsiveness
- Don't block main thread
- Update UI with `after()` method
- Show loading indicators
- Cancel long operations

## Testing

### Manual Testing Checklist
- [ ] Scan folder successfully
- [ ] View file details
- [ ] Search files
- [ ] Add/remove tags
- [ ] AI analysis works
- [ ] OLLAMA connection
- [ ] Batch operations
- [ ] Settings changes persist

### Common Issues
- OLLAMA not running → Check Settings
- Slow scanning → Check folder size
- Tags not saving → Check database permissions
- UI freezing → Check for blocking operations

## Future Enhancements

Potential additions:
- File organization recommendations
- Duplicate file detection
- Cloud storage integration
- Advanced search filters
- Export/import capabilities
- Plugins system
- Dark mode
- Multi-language support

---

**Note**: This structure is designed for maintainability, extensibility, and clear separation of concerns. Follow these patterns when adding new features.
