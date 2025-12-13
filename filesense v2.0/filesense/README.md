# FileSense - AI-Powered File Organization

<div align="center">

![FileSense Logo](https://img.shields.io/badge/FileSense-AI%20File%20Manager-blue?style=for-the-badge)

**Intelligent file organization powered by local AI**

[![Python](https://img.shields.io/badge/Python-3.9+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)]()

</div>

---

## 🌟 Features

### 🤖 AI-Powered Analysis
- **Smart Tagging**: Automatically generate relevant tags for your files
- **Content Summarization**: Get AI-generated summaries of documents
- **Insight Extraction**: Discover key points and themes in your files
- **Auto-Categorization**: Intelligently categorize files by content

### 📂 File Management
- **Folder Scanning**: Recursively scan and index your files
- **Search**: Find files by name, tags, or content
- **Batch Operations**: Tag, move, or categorize multiple files at once
- **File Preview**: Quick preview for text, code, and documents

### 🔍 Organization Tools
- **Smart Tags**: Flexible tagging system with tag management
- **Categories**: Organize files into logical categories
- **Recent Files**: Quick access to recently accessed files
- **Duplicate Finder**: Identify and remove duplicate files

### 📁 Smart Folders
- **Real-time Monitoring**: Watch folders for new files
- **Auto-Import**: Automatically add new files to database
- **Custom Filters**: Filter by extension and folder options
- **Activity Log**: Track all file changes in real-time

### 🎨 Modern Interface
- **Clean Design**: Professional, intuitive UI
- **Theme Support**: Light, Dark, and custom themes
- **Responsive Layout**: Adapts to window size
- **Easy Navigation**: Sidebar with quick access to all features

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- OLLAMA (for AI features)

### Installation

1. **Clone or download the repository**
   ```bash
   cd filesense
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install OLLAMA** (for AI features)
   - Download from: https://ollama.ai
   - Pull a model: `ollama pull llama2`

4. **Run FileSense**
   ```bash
   python main.py
   ```

### Windows Users
Double-click `run.bat` to start the application.

### Linux Users
```bash
chmod +x run.sh
./run.sh
```

---

## 📖 User Guide

### Dashboard
The dashboard provides an overview of your file library:
- Total files and storage used
- Quick statistics (tagged files, categories)
- Recent activity log
- Popular tags

### File Browser
- Click **Scan Folder** to add files to your library
- Select multiple files with checkboxes
- View file details by clicking on a file
- Use the action bar for batch operations

### AI Analysis
1. Select a file from the browser or recent files
2. Navigate to **AI Analysis**
3. Choose analysis options (tags, summary, insights)
4. Select your OLLAMA model
5. Click **Analyze** to process

### Search
- Type in the search bar to find files
- Search by filename, tags, or content
- Click results to view file details

### Tags
- View all tags in your library
- Click a tag to see associated files
- Create new tags through file editing
- Remove unused tags

### Smart Folders
- Add folders to monitor for changes
- Configure auto-import settings
- Watch real-time file activity
- Set up file type filters

### Find Duplicates
- Scan your library for duplicate files
- View duplicate groups with file sizes
- Select duplicates for removal
- Free up storage space

### Batch Operations
- Select files to process
- Choose operation (tag, move, categorize, delete)
- Process multiple files at once
- View progress in real-time

### Settings
- Configure OLLAMA connection
- Choose application theme
- Set default scan location
- Export/import data

---

## 🏗️ Architecture

```
filesense/
├── main.py                 # Application entry point
├── app/
│   ├── models/
│   │   └── database.py     # SQLAlchemy models
│   ├── services/
│   │   ├── ollama_service.py    # OLLAMA AI integration
│   │   ├── file_service.py      # File operations
│   │   ├── stats_service.py     # Statistics
│   │   └── file_watcher.py      # Folder monitoring
│   ├── views/
│   │   ├── dashboard.py         # Home view
│   │   ├── file_browser.py      # File listing
│   │   ├── ai_analysis.py       # AI features
│   │   ├── search.py            # Search view
│   │   ├── tags.py              # Tag management
│   │   ├── smart_folders.py     # Folder monitoring
│   │   ├── duplicate_finder.py  # Find duplicates
│   │   ├── batch_operations.py  # Bulk actions
│   │   ├── settings.py          # Configuration
│   │   └── dialogs.py           # Dialog components
│   └── utils/
│       ├── file_utils.py        # File helpers
│       ├── content_reader.py    # Document reading
│       ├── duplicate_finder.py  # Duplicate detection
│       └── theme_manager.py     # Theme support
├── requirements.txt        # Python dependencies
└── docs/                   # Documentation
```

---

## 🔧 Configuration

### OLLAMA Setup
FileSense uses OLLAMA for AI features. Configure in Settings:
- **URL**: Default is `http://localhost:11434`
- **Model**: Choose from available models (llama2, mistral, codellama)

### Database
- Location: `~/.filesense/filesense.db`
- Format: SQLite
- Auto-created on first run

### Smart Folders Config
- Location: `~/.filesense/smart_folders.json`
- Stores watched folder configurations

---

## 📋 Supported File Types

| Category | Extensions |
|----------|------------|
| Documents | .txt, .md, .pdf, .doc, .docx, .odt |
| Spreadsheets | .xls, .xlsx, .csv, .ods |
| Presentations | .ppt, .pptx |
| Code | .py, .js, .ts, .java, .cpp, .html, .css |
| Images | .png, .jpg, .gif, .svg, .webp |
| Audio | .mp3, .wav, .flac, .ogg |
| Video | .mp4, .avi, .mkv, .mov |
| Archives | .zip, .rar, .7z, .tar, .gz |

---

## 🐛 Troubleshooting

### OLLAMA Not Connected
1. Ensure OLLAMA is installed and running
2. Check the URL in Settings (default: http://localhost:11434)
3. Verify a model is pulled: `ollama list`

### Files Not Appearing
1. Click "Refresh" in File Browser
2. Check if file extensions are supported
3. Verify file permissions

### Database Issues
1. Delete `~/.filesense/filesense.db`
2. Restart application (will recreate database)

### Import Errors
```bash
pip install -r requirements.txt --upgrade
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern UI framework
- [OLLAMA](https://ollama.ai) - Local AI models
- [SQLAlchemy](https://sqlalchemy.org) - Database ORM

---

<div align="center">

**Made with ❤️ for better file organization**

</div>
