# FileSense Quick Start Guide

Welcome to FileSense! This guide will help you get started in minutes.

## Step 1: Installation

### Install Python Dependencies
```bash
# Windows
python -m pip install -r requirements.txt

# Linux
pip3 install -r requirements.txt
```

Or use the setup script:
```bash
# Windows
python setup.py

# Linux
python3 setup.py
```

### Install OLLAMA (for AI features)

1. Download OLLAMA from [ollama.ai](https://ollama.ai)
2. Install and run OLLAMA
3. Download a model:
   ```bash
   ollama pull llama2
   ```

## Step 2: Launch FileSense

### Windows
Double-click `run.bat` or run:
```bash
python main.py
```

### Linux
Run the launch script or python directly:
```bash
./run.sh
# OR
python3 main.py
```

## Step 3: Add Your Files

1. Click **"File Browser"** in the sidebar
2. Click **"📂 Scan Folder"** button
3. Select a folder containing files
4. Wait for the scan to complete

FileSense will index all supported files in that folder and its subfolders.

## Step 4: Try AI Analysis

1. Click **"🤖 AI Analysis"** in the sidebar
2. Click **"Choose File to Analyze"**
3. Select a file from the list
4. Choose analysis options:
   - ✅ Generate Summary
   - ✅ Suggest Tags
   - ✅ Extract Insights
   - ☐ Categorize File
5. Click **"Start AI Analysis"**

**Note**: Make sure OLLAMA is running first!

## Step 5: Explore Features

### Search Files
- Click **"🔍 Search"**
- Type your search query
- Press Enter or click Search
- Click on any result to view details

### View Recent Files
- Click **"🕒 Recent Files"**
- Filter by file type
- Click any file to see details

### Browse Tags
- Click **"🏷️ Tags"**
- See all tags and their usage counts
- Click a tag to see files with that tag

### Batch Operations
- Click **"⚡ Batch Operations"**
- Choose an operation type
- Follow the on-screen instructions

## Common Tasks

### Adding Tags to a File
1. Click on a file to view details
2. Click **"Edit Tags"** button
3. Enter tags and save

### Searching for Files
1. Use the search bar on Dashboard
2. Or go to Search page
3. Type your query
4. View results

### Viewing File Details
1. Click any file in any view
2. See comprehensive information
3. Click **"Open"** to open the file
4. Click **"Edit Tags"** to manage tags

### Organizing Files with AI
1. Select files in File Browser
2. Click **"AI Analyze"**
3. Let AI suggest tags and categories
4. Apply the suggestions

## Tips & Tricks

### 🎯 Better AI Results
- Use specific, descriptive files
- Choose appropriate AI models
- Analyze text files for best results

### 🏷️ Effective Tagging
- Use consistent tag names
- Keep tags short and descriptive
- Use lowercase for consistency
- Group related tags

### 🔍 Better Searches
- Search by filename, tags, or content
- Use specific keywords
- Combine multiple search terms

### ⚡ Batch Operations
- Select multiple files in File Browser
- Use batch operations for efficiency
- AI can process multiple files

## Troubleshooting

### OLLAMA Not Working?
1. Check if OLLAMA is running: `ollama list`
2. Try: `ollama serve` if not running
3. Verify the connection in Settings

### Files Not Showing?
1. Refresh the file browser
2. Check file permissions
3. Ensure files are supported types
4. Try scanning a smaller folder

### Slow Performance?
1. Use a faster AI model
2. Reduce file content analyzed
3. Close other applications
4. Scan smaller folders at a time

## Need Help?

- Check the [full README](README.md)
- Visit our documentation
- Submit an issue on GitHub

---

Happy organizing! 🎉
