# FileSense - AI-Powered Local File Search

![FileSense](https://img.shields.io/badge/Version-1.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)
![Ollama](https://img.shields.io/badge/Ollama-Local%20AI-orange.svg)

A powerful desktop application that uses local AI (Ollama) to intelligently index, tag, and search your files using natural language queries.

## 🌟 Features

- **🔍 Natural Language Search**: Search files using plain English like "financial reports from last quarter"
- **🤖 Local AI Processing**: Uses Ollama for privacy-focused, offline AI features
- **🏷️ Auto-Tagging**: Automatically generates relevant tags for your files
- **📝 AI Summaries**: Creates concise summaries of file contents
- **⚡ Fast Indexing**: Quickly scans and indexes large folder structures
- **💾 Local Database**: All data stored locally on your machine
- **🎨 Modern UI**: Clean, intuitive web-based interface

## 📋 Requirements

### Required:
- **Windows 10/11** (64-bit)
- **Python 3.8 or later** ([Download](https://www.python.org/downloads/))
- **4GB RAM minimum** (8GB recommended)

### Optional (for AI features):
- **Ollama** ([Download](https://ollama.com/download))
- **5-10GB disk space** for AI models

## 🚀 Quick Start

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Verify installation by opening Command Prompt and typing: `python --version`

### Step 2: Setup FileSense

1. Extract the FileSense folder to your desired location (e.g., `C:\FileSense`)
2. Open the FileSense folder
3. **Double-click `SETUP.bat`**
4. Wait for installation to complete (1-2 minutes)

### Step 3: Install Ollama (for AI features)

1. Visit [ollama.com/download](https://ollama.com/download)
2. Download and install Ollama for Windows
3. Ollama will start automatically after installation
4. You can verify it's running by checking the system tray

### Step 4: Start FileSense

1. **Double-click `START_FILESENSE.bat`**
2. Your browser will open automatically at `http://localhost:5000`
3. If it doesn't open, manually navigate to `http://localhost:5000`

### Step 5: Download AI Model (First time only)

1. In FileSense, click the **"Ollama Setup"** tab
2. Click **"Pull Model"** on "Llama 3.2 (3B) - Recommended"
3. Wait 5-10 minutes for the model to download
4. You'll see progress in the Command Prompt window

### Step 6: Index Your Files

1. Click the **"Indexing"** tab
2. Enter a folder path (e.g., `C:\Users\YourName\Documents`)
3. Click **"Start Scan"**
4. Or use quick buttons for common folders (Documents, Downloads, etc.)

### Step 7: Search!

1. Return to the **Dashboard** tab
2. Type a natural language query like:
   - "financial reports from last quarter"
   - "photos with family from 2024"
   - "meeting notes with John"
3. View results with AI-generated summaries and tags!

## 📖 Detailed Usage

### Natural Language Search Examples

FileSense understands natural language queries. Try these:

- **Time-based**: "documents from last month", "files created yesterday"
- **Content-based**: "budget spreadsheets", "project proposals"
- **Person-based**: "files from Sarah", "documents shared with team"
- **Size-based**: "large video files", "documents over 5MB"
- **Type-based**: "PDF reports", "Excel spreadsheets", "image files"

### Recommended Ollama Models

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **Llama 3.2 (1B)** | ~1GB | Fast | Good | Quick tagging, low-end PCs |
| **Llama 3.2 (3B)** ⭐ | ~2GB | Medium | Great | Balanced performance (Recommended) |
| **Llama 3.1 (8B)** | ~5GB | Slow | Excellent | Best quality, high-end PCs |

### Settings Explained

**Auto-generate tags for new files**
- Automatically creates relevant tags when indexing files
- Uses AI to analyze file content and suggest appropriate tags
- Recommended: ✅ Enabled

**Auto-generate summaries**
- Creates brief summaries of file contents during indexing
- Makes indexing slower but provides better search context
- Recommended: ❌ Disabled for large scans (enable later for specific files)

**Ollama Model**
- Choose which AI model to use
- Larger models are smarter but slower
- Can be changed anytime in Settings tab

## 🛠️ Troubleshooting

### Problem: "Python is not installed" error

**Solution:**
1. Install Python from [python.org](https://www.python.org/downloads/)
2. Make sure to check "Add Python to PATH"
3. Restart your computer
4. Run SETUP.bat again

### Problem: Ollama not detected

**Solution:**
1. Check if Ollama is installed (look for Ollama icon in system tray)
2. If not installed, download from [ollama.com/download](https://ollama.com/download)
3. After installation, Ollama starts automatically
4. Restart FileSense

### Problem: Model pull fails

**Solution:**
1. Make sure Ollama is running (check system tray)
2. Check your internet connection
3. Try pulling the model manually:
   - Open Command Prompt
   - Type: `ollama pull llama3.2:3b`
   - Wait for completion

### Problem: Indexing is slow

**Tips:**
1. Disable "Auto-generate summaries" for initial scans
2. Index smaller folders first
3. Use a faster/smaller AI model (Llama 3.2 1B)
4. Close other applications to free up RAM
5. Consider indexing when you're not using the PC

### Problem: Can't access http://localhost:5000

**Solution:**
1. Make sure FileSense is running (START_FILESENSE.bat window should be open)
2. Check if port 5000 is already in use by another application
3. Try accessing from a different browser
4. Check Windows Firewall settings

### Problem: Search returns no results

**Possible causes:**
1. No files have been indexed yet (go to Indexing tab)
2. Search query is too specific
3. Files don't match the query
4. Database is empty (check Dashboard stats)

## 📁 File Structure

```
FileSense/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── SETUP.bat                # Windows setup script
├── START_FILESENSE.bat      # Windows start script
├── README.md                # This file
├── data/                    # Database and data storage
│   └── filesense.db         # SQLite database (created on first run)
├── static/                  # Static web assets
│   ├── css/
│   │   └── style.css       # Application styles
│   └── js/
│       └── app.js          # Frontend JavaScript
└── templates/               # HTML templates
    └── index.html          # Main application page
```

## 🔐 Privacy & Security

- **100% Local**: All data stays on your computer
- **No Cloud**: No data is sent to external servers
- **Offline AI**: Ollama runs completely offline
- **Your Control**: You control what gets indexed
- **Open Source**: Inspect the code yourself

## ⚙️ Advanced Usage

### Command Line Options

You can also run FileSense directly with Python:

```bash
# Activate virtual environment
venv\Scripts\activate

# Run with custom port
python app.py --port 8080

# Run in debug mode
set FLASK_DEBUG=1
python app.py
```

### API Endpoints

FileSense provides a REST API:

- `GET /api/status` - System status
- `POST /api/search` - Search files
- `POST /api/scan` - Start folder scan
- `GET /api/tags` - Get all tags
- `GET /api/files/<id>` - Get file details
- `GET/POST /api/settings` - Get/update settings
- `POST /api/ollama/pull` - Pull Ollama model

### Database Management

The SQLite database is located at `data/filesense.db`. You can:

- **Backup**: Copy the `data/` folder
- **Reset**: Delete `data/filesense.db` to start fresh
- **Export**: Use SQLite tools to export data

## 🆘 Support & Resources

### Official Resources

- **Ollama Documentation**: [docs.ollama.com](https://docs.ollama.com)
- **Python Documentation**: [docs.python.org](https://docs.python.org)
- **Flask Documentation**: [flask.palletsprojects.com](https://flask.palletsprojects.com)

### Getting Help

1. Check this README first
2. Look at the Troubleshooting section
3. Check if Ollama is running (system tray icon)
4. Try restarting FileSense
5. Check the Command Prompt window for error messages

## 🔄 Updates

To update FileSense:

1. Download the new version
2. Copy your `data/` folder from the old version
3. Paste it into the new version folder
4. Run SETUP.bat again
5. Your indexed files and settings will be preserved

## ⚠️ Limitations

- **Windows Only**: Currently only supports Windows (Mac/Linux coming soon)
- **English Only**: Natural language processing works best with English queries
- **File Types**: Best with text-based files (PDF, DOCX, TXT, etc.)
- **Large Files**: Very large files (>100MB) may be slow to process
- **Real-time Updates**: Changes to files aren't detected automatically (re-scan needed)

## 🎯 Best Practices

1. **Start Small**: Index a single folder first to test
2. **Use Quick Folders**: Use the quick access buttons for common locations
3. **Regular Scans**: Re-scan important folders weekly to catch new files
4. **Relevant Tags**: Review and clean up auto-generated tags periodically
5. **Backup Database**: Regularly backup your `data/` folder
6. **Update Models**: Try different Ollama models to find what works best

## 📊 System Requirements by Use Case

### Light Use (Personal Documents)
- Files: Up to 10,000
- RAM: 4GB
- Disk: 5GB (including models)
- Model: Llama 3.2 (1B)

### Medium Use (Work Documents)
- Files: Up to 50,000
- RAM: 8GB
- Disk: 10GB (including models)
- Model: Llama 3.2 (3B)

### Heavy Use (Enterprise/Archive)
- Files: Up to 200,000
- RAM: 16GB
- Disk: 20GB (including models)
- Model: Llama 3.1 (8B)

## 🚀 Performance Tips

1. **SSD Storage**: Store FileSense on an SSD for faster indexing
2. **Close Apps**: Close unnecessary applications during indexing
3. **Exclude Folders**: Don't index system folders or temp directories
4. **Smaller Models**: Use lighter AI models if speed is priority
5. **Batch Operations**: Index multiple folders at once during off-hours

## 📝 License

FileSense is provided as-is for personal and educational use.

## 🎓 Credits

- **Created by**: Xavier Sutherland & Team
- **University**: Penn State CMPSC 465
- **Powered by**: Flask, SQLite, Ollama, Llama 3.2
- **Inspired by**: Modern file search needs and AI capabilities

---

**Version 1.0** | Last Updated: November 2024

*Happy Searching! 🔍*
