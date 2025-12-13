# FileSense Installation Guide

Complete installation instructions for Windows and Linux.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Windows Installation](#windows-installation)
3. [Linux Installation](#linux-installation)
4. [OLLAMA Setup](#ollama-setup)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11 or Linux (Ubuntu 20.04+, Fedora, etc.)
- **Python**: 3.8 or higher
- **RAM**: 4 GB (8 GB recommended for AI features)
- **Disk Space**: 500 MB for application + models
- **Internet**: For downloading dependencies and OLLAMA models

### Recommended Requirements
- **RAM**: 8 GB or more
- **CPU**: Multi-core processor
- **Disk Space**: 2+ GB for multiple AI models

## Windows Installation

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```cmd
   python --version
   ```

### Step 2: Install FileSense Dependencies

1. Open Command Prompt or PowerShell
2. Navigate to FileSense directory:
   ```cmd
   cd path\to\filesense
   ```
3. Run the setup script:
   ```cmd
   python setup.py
   ```
   Or manually install:
   ```cmd
   python -m pip install -r requirements.txt
   ```

### Step 3: Install OLLAMA (For AI Features)

1. Download OLLAMA for Windows from [ollama.ai](https://ollama.ai)
2. Run the installer
3. OLLAMA will run in the background
4. Open Command Prompt and pull a model:
   ```cmd
   ollama pull llama2
   ```

### Step 4: Launch FileSense

Double-click `run.bat` or run:
```cmd
python main.py
```

## Linux Installation

### Step 1: Install Python

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip python3-tkinter
```

**Arch:**
```bash
sudo pacman -S python python-pip tk
```

Verify installation:
```bash
python3 --version
```

### Step 2: Install FileSense Dependencies

```bash
cd path/to/filesense
python3 setup.py
```

Or manually:
```bash
pip3 install -r requirements.txt --user
```

### Step 3: Install OLLAMA (For AI Features)

**Using curl:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Manual installation:**
1. Download from [ollama.ai](https://ollama.ai)
2. Extract and move to `/usr/local/bin/`
3. Make executable: `chmod +x /usr/local/bin/ollama`

**Pull a model:**
```bash
ollama pull llama2
```

**Start OLLAMA service (if needed):**
```bash
ollama serve
```

### Step 4: Launch FileSense

```bash
./run.sh
```

Or:
```bash
python3 main.py
```

## OLLAMA Setup

### Installing Models

OLLAMA provides various models for different use cases:

**Recommended for FileSense:**
```bash
ollama pull llama2
```

**Alternative models:**
```bash
# Smaller, faster model
ollama pull mistral

# Specialized for code
ollama pull codellama

# Larger, more capable model
ollama pull llama2:13b
```

### Verifying OLLAMA Installation

```bash
# List installed models
ollama list

# Test model
ollama run llama2 "Hello, how are you?"
```

### Configuring OLLAMA in FileSense

1. Launch FileSense
2. Click **Settings** in sidebar
3. Go to **OLLAMA Configuration**
4. Default URL: `http://localhost:11434`
5. Click **Test Connection**

## Verification

### Check Python Installation
```bash
# Windows
python --version
python -m pip list

# Linux
python3 --version
pip3 list
```

### Check Dependencies
Ensure these packages are installed:
- customtkinter >= 5.2.0
- sqlalchemy >= 2.0.0
- requests >= 2.31.0
- pillow >= 10.0.0

### Check OLLAMA
```bash
# Check if OLLAMA is running
ollama list

# Check FileSense can connect
# Launch FileSense > Settings > Test Connection
```

### First Run Checklist
- [ ] Python 3.8+ installed
- [ ] All dependencies installed
- [ ] OLLAMA installed (for AI features)
- [ ] At least one model pulled
- [ ] FileSense launches without errors
- [ ] Can scan a folder
- [ ] Can connect to OLLAMA (Settings)

## Troubleshooting

### Python Not Found

**Windows:**
- Reinstall Python with "Add to PATH" checked
- Or add manually to System Environment Variables

**Linux:**
- Install python3: `sudo apt install python3`
- Create symlink if needed: `sudo ln -s /usr/bin/python3 /usr/bin/python`

### Tkinter Import Error

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

### pip Install Fails

**Windows:**
```cmd
python -m pip install --upgrade pip
python -m pip install -r requirements.txt --user
```

**Linux:**
```bash
pip3 install --upgrade pip --user
pip3 install -r requirements.txt --user
```

### OLLAMA Connection Failed

1. **Check if OLLAMA is running:**
   ```bash
   ollama list
   ```

2. **Start OLLAMA server:**
   ```bash
   ollama serve
   ```

3. **Check port 11434:**
   ```bash
   # Linux/Mac
   lsof -i :11434
   
   # Windows
   netstat -ano | findstr :11434
   ```

4. **Firewall issues:**
   - Allow OLLAMA through firewall
   - Check antivirus isn't blocking it

### Permission Errors (Linux)

```bash
# Install packages to user directory
pip3 install --user -r requirements.txt

# Or use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Database Errors

1. Delete existing database:
   ```bash
   # Windows
   rmdir /s %USERPROFILE%\.filesense
   
   # Linux
   rm -rf ~/.filesense
   ```

2. Restart FileSense to recreate database

### CustomTkinter Issues

```bash
# Update to latest version
pip install --upgrade customtkinter

# Or specific version
pip install customtkinter==5.2.0
```

## Advanced Installation

### Using Virtual Environment (Recommended)

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running from Source

```bash
# Clone repository
git clone https://github.com/yourusername/filesense.git
cd filesense

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Building Executable (Optional)

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed main.py

# Find executable in dist/ folder
```

## Getting Help

Still having issues? Try:

1. **Check the logs**: Look for error messages in the console
2. **Verify versions**: Ensure Python 3.8+ and latest dependencies
3. **Clean install**: Remove and reinstall all components
4. **Documentation**: Read the full [README](../README.md)
5. **Support**: Create an issue on GitHub with:
   - Operating system and version
   - Python version
   - Error messages
   - Steps to reproduce

## Next Steps

After successful installation:

1. Read the [Quick Start Guide](QUICKSTART.md)
2. Scan your first folder
3. Try AI analysis on a document
4. Explore all features
5. Configure settings to your preference

---

**Note**: FileSense requires an active internet connection only for:
- Initial dependency installation
- Downloading OLLAMA models
- (Optional) Remote OLLAMA connections

Once installed, FileSense works completely offline!
