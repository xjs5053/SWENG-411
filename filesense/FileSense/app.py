"""
FileSense - AI-Powered Local File Search System
Main Application File with Ollama Integration
"""

import os
import sys
import json
import sqlite3
import hashlib
import mimetypes
import subprocess
import threading
import time
import shutil
import platform
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'filesense-local-ai-search'
app.config['DATABASE'] = 'data/filesense.db'
app.config['OLLAMA_URL'] = 'http://localhost:11434'

# Global state
indexing_status = {
    'active': False,
    'progress': 0,
    'total': 0,
    'current_file': ''
}

ollama_status = {
    'installed': False,
    'running': False,
    'models': []
}

# ==================== DATABASE FUNCTIONS ====================

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()

    # Ensure foreign keys are enforced for relational integrity
    c.execute('PRAGMA foreign_keys = ON;')
    
    # Files table
    c.execute('''CREATE TABLE IF NOT EXISTS files
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  path TEXT UNIQUE NOT NULL,
                  filename TEXT NOT NULL,
                  extension TEXT,
                  size INTEGER,
                  modified_date DATETIME,
                  created_date DATETIME,
                  file_hash TEXT,
                  indexed_date DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # Tags table
    c.execute('''CREATE TABLE IF NOT EXISTS tags
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  tag_name TEXT UNIQUE NOT NULL,
                  color TEXT DEFAULT '#FFD93D',
                  usage_count INTEGER DEFAULT 0)''')
    
    # File-Tags relationship
    c.execute('''CREATE TABLE IF NOT EXISTS file_tags
                 (file_id INTEGER,
                  tag_id INTEGER,
                  FOREIGN KEY(file_id) REFERENCES files(id) ON DELETE CASCADE,
                  FOREIGN KEY(tag_id) REFERENCES tags(id) ON DELETE CASCADE,
                  PRIMARY KEY(file_id, tag_id))''')
    
    # AI Summaries table
    c.execute('''CREATE TABLE IF NOT EXISTS summaries
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  file_id INTEGER UNIQUE,
                  summary TEXT,
                  model_used TEXT,
                  generated_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(file_id) REFERENCES files(id) ON DELETE CASCADE)''')
    
    # Settings table
    c.execute('''CREATE TABLE IF NOT EXISTS settings
                 (key TEXT PRIMARY KEY,
                  value TEXT)''')
    
    # Insert default settings
    default_settings = {
        'ollama_model': 'llama3.2:3b',
        'scan_folders': json.dumps([]),
        'auto_tag': 'true',
        'auto_summarize': 'false'
    }
    
    for key, value in default_settings.items():
        c.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (key, value))
    
    conn.commit()
    conn.close()

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

# ==================== OLLAMA FUNCTIONS ====================

def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(['ollama', '--version'],
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except Exception:
        return False

def check_ollama_running():
    """Check if Ollama service is running"""
    try:
        response = requests.get(f"{app.config['OLLAMA_URL']}/api/tags", timeout=2)
        return response.status_code == 200
    except Exception:
        return False

def get_ollama_models():
    """Get list of installed Ollama models"""
    try:
        response = requests.get(f"{app.config['OLLAMA_URL']}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
        return []
    except Exception:
        return []

def pull_ollama_model(model_name):
    """Pull an Ollama model"""
    try:
        subprocess.Popen(['ollama', 'pull', model_name], 
                        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
        return True
    except:
        return False

def generate_with_ollama(prompt, model='llama3.2:3b'):
    """Generate text using Ollama"""
    try:
        response = requests.post(
            f"{app.config['OLLAMA_URL']}/api/generate",
            json={
                'model': model,
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': 0.7,
                    'num_predict': 200
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json().get('response', '')
        return None
    except Exception as e:
        print(f"Ollama generation error: {e}")
        return None

# ==================== FILE INDEXING ====================

def calculate_file_hash(filepath):
    """Calculate MD5 hash of file"""
    try:
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return None

def extract_text_content(filepath):
    """Extract text content from common file types"""
    extension = Path(filepath).suffix.lower()
    
    try:
        # Text files
        if extension in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml']:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()[:5000]  # First 5000 chars
        
        # For other files, return filename and path
        return f"Filename: {Path(filepath).name}\nPath: {filepath}"
    except:
        return f"Filename: {Path(filepath).name}"

def generate_summary(filepath, content):
    """Generate AI summary for file"""
    db = get_db()
    model = db.execute('SELECT value FROM settings WHERE key = ?', ('ollama_model',)).fetchone()
    model_name = model['value'] if model else 'llama3.2:3b'
    db.close()
    
    if not check_ollama_running():
        return None
    
    prompt = f"""Analyze this file and provide a brief 1-2 sentence summary:

File: {Path(filepath).name}
Content preview:
{content[:1000]}

Provide only the summary, no other text:"""
    
    summary = generate_with_ollama(prompt, model_name)
    return summary

def generate_tags(filepath, content):
    """Generate AI tags for file"""
    db = get_db()
    model = db.execute('SELECT value FROM settings WHERE key = ?', ('ollama_model',)).fetchone()
    model_name = model['value'] if model else 'llama3.2:3b'
    db.close()
    if not check_ollama_running():
        # Graceful offline fallback based on file metadata
        fallback = set()
        fallback.add(Path(filepath).suffix.replace('.', '').upper() or 'FILE')
        fallback.add(Path(filepath).parent.name)
        mime_type = mimetypes.guess_type(filepath)[0]
        if mime_type:
            fallback.add(mime_type.split('/')[0])
        return [tag for tag in fallback if tag]

    prompt = f"""You are a digital librarian that organizes local files.
Suggest 3-5 concise category tags (single words or short phrases) for this file.
Avoid duplicate wording and keep each tag under 30 characters.

File: {Path(filepath).name}
Content preview:
{content[:1000]}

Respond with comma-separated tags only."""

    response = generate_with_ollama(prompt, model_name)
    if response:
        tags = [tag.strip() for tag in response.split(',')]
        return [tag for tag in tags if tag and len(tag) < 30][:5]
    return []

def index_file(filepath):
    """Index a single file"""
    try:
        path_obj = Path(filepath)
        
        if not path_obj.exists() or path_obj.is_dir():
            return False
        
        stats = path_obj.stat()
        file_hash = calculate_file_hash(filepath)
        
        db = get_db()
        
        # Check if file already exists
        existing = db.execute('SELECT id, file_hash FROM files WHERE path = ?', 
                             (str(filepath),)).fetchone()
        
        if existing and existing['file_hash'] == file_hash:
            return True  # File unchanged
        
        # Insert or update file
        if existing:
            db.execute('''UPDATE files SET filename = ?, extension = ?, size = ?,
                         modified_date = ?, file_hash = ?, indexed_date = ?
                         WHERE id = ?''',
                      (path_obj.name, path_obj.suffix, stats.st_size,
                       datetime.fromtimestamp(stats.st_mtime),
                       file_hash, datetime.now(), existing['id']))
            file_id = existing['id']
        else:
            cursor = db.execute('''INSERT INTO files 
                                  (path, filename, extension, size, modified_date, 
                                   created_date, file_hash)
                                  VALUES (?, ?, ?, ?, ?, ?, ?)''',
                               (str(filepath), path_obj.name, path_obj.suffix, 
                                stats.st_size, datetime.fromtimestamp(stats.st_mtime),
                                datetime.fromtimestamp(stats.st_ctime), file_hash))
            file_id = cursor.lastrowid
        
        # Extract content and generate AI features if enabled
        auto_tag = db.execute('SELECT value FROM settings WHERE key = ?', 
                             ('auto_tag',)).fetchone()
        auto_summarize = db.execute('SELECT value FROM settings WHERE key = ?', 
                                    ('auto_summarize',)).fetchone()
        
        if (auto_tag and auto_tag['value'] == 'true') or \
           (auto_summarize and auto_summarize['value'] == 'true'):
            content = extract_text_content(filepath)
            
            # Generate summary
            if auto_summarize and auto_summarize['value'] == 'true':
                summary = generate_summary(filepath, content)
                if summary:
                    db.execute('''INSERT OR REPLACE INTO summaries 
                                 (file_id, summary, model_used) VALUES (?, ?, ?)''',
                              (file_id, summary, 'llama3.2:3b'))
            
            # Generate tags
            if auto_tag and auto_tag['value'] == 'true':
                tags = generate_tags(filepath, content)
                for tag_name in tags:
                    # Insert tag if not exists
                    db.execute('INSERT OR IGNORE INTO tags (tag_name) VALUES (?)', 
                              (tag_name,))
                    tag = db.execute('SELECT id FROM tags WHERE tag_name = ?', 
                                    (tag_name,)).fetchone()
                    if tag:
                        # Link file to tag
                        db.execute('INSERT OR IGNORE INTO file_tags (file_id, tag_id) VALUES (?, ?)',
                                  (file_id, tag['id']))
                        # Update tag usage
                        db.execute('UPDATE tags SET usage_count = usage_count + 1 WHERE id = ?',
                                  (tag['id'],))
        
        db.commit()
        db.close()
        return True
        
    except Exception as e:
        print(f"Error indexing {filepath}: {e}")
        return False

def scan_folder(folder_path):
    """Scan folder and index all files"""
    global indexing_status

    indexing_status['active'] = True
    indexing_status['progress'] = 0
    
    try:
        path_obj = Path(os.path.expanduser(folder_path))
        if not path_obj.exists():
            return
        
        # Get all files
        all_files = []
        for root, dirs, files in os.walk(folder_path):
            # Skip hidden and system folders
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if not file.startswith('.'):
                    all_files.append(os.path.join(root, file))
        
        indexing_status['total'] = len(all_files)
        
        for i, filepath in enumerate(all_files):
            indexing_status['progress'] = i + 1
            indexing_status['current_file'] = os.path.basename(filepath)
            index_file(filepath)
        
    finally:
        indexing_status['active'] = False
        indexing_status['current_file'] = 'Complete'

# ==================== SEARCH FUNCTIONS ====================

def search_files(query, limit=20):
    """Search files using natural language query"""
    db = get_db()
    
    # Simple keyword search (can be enhanced with NLP)
    keywords = query.lower().split()
    
    results = []
    
    # Search in filenames, tags, and summaries
    for keyword in keywords:
        # Filename search
        rows = db.execute('''
            SELECT DISTINCT f.*, GROUP_CONCAT(t.tag_name, ',') as tags, s.summary
            FROM files f
            LEFT JOIN file_tags ft ON f.id = ft.file_id
            LEFT JOIN tags t ON ft.tag_id = t.id
            LEFT JOIN summaries s ON f.id = s.file_id
            WHERE LOWER(f.filename) LIKE ? OR LOWER(s.summary) LIKE ? OR LOWER(t.tag_name) LIKE ?
            GROUP BY f.id
            LIMIT ?
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', limit)).fetchall()
        
        for row in rows:
            if row['id'] not in [r['id'] for r in results]:
                results.append(dict(row))
    
    db.close()
    return results[:limit]


def fetch_files(query=None, tag=None, limit=50, sort='recent'):
    """Retrieve files with optional filtering for UI views"""
    db = get_db()

    base_query = """
        SELECT f.*, GROUP_CONCAT(t.tag_name, ',') as tags, s.summary
        FROM files f
        LEFT JOIN file_tags ft ON f.id = ft.file_id
        LEFT JOIN tags t ON ft.tag_id = t.id
        LEFT JOIN summaries s ON f.id = s.file_id
    """

    conditions = []
    params = []

    if query:
        like_query = f"%{query.lower()}%"
        conditions.append("(LOWER(f.filename) LIKE ? OR LOWER(f.path) LIKE ? OR LOWER(s.summary) LIKE ?)")
        params.extend([like_query, like_query, like_query])

    if tag:
        conditions.append("LOWER(t.tag_name) LIKE ?")
        params.append(f"%{tag.lower()}%")

    where_clause = f" WHERE {' AND '.join(conditions)}" if conditions else ""
    order_clause = " ORDER BY f.modified_date DESC" if sort == 'recent' else " ORDER BY f.filename ASC"

    query_sql = base_query + where_clause + " GROUP BY f.id" + order_clause + " LIMIT ?"
    params.append(limit)

    rows = db.execute(query_sql, params).fetchall()
    db.close()
    return [dict(row) for row in rows]


def apply_tags_to_file(file_id, tag_list):
    """Persist tags for a file and increment usage counts"""
    db = get_db()
    for tag_name in tag_list:
        clean_tag = tag_name.strip()
        if not clean_tag:
            continue
        db.execute('INSERT OR IGNORE INTO tags (tag_name) VALUES (?)', (clean_tag,))
        tag_row = db.execute('SELECT id FROM tags WHERE tag_name = ?', (clean_tag,)).fetchone()
        if tag_row:
            db.execute('INSERT OR IGNORE INTO file_tags (file_id, tag_id) VALUES (?, ?)',
                      (file_id, tag_row['id']))
            db.execute('UPDATE tags SET usage_count = usage_count + 1 WHERE id = ?', (tag_row['id'],))
    db.commit()
    db.close()


def ensure_file_record(file_path):
    """Ensure the file exists in the database and return its record"""
    db = get_db()
    record = db.execute('SELECT * FROM files WHERE path = ?', (str(file_path),)).fetchone()
    db.close()
    if record:
        return record

    # Index the file to insert it
    index_file(file_path)
    db = get_db()
    record = db.execute('SELECT * FROM files WHERE path = ?', (str(file_path),)).fetchone()
    db.close()
    return record


def move_files_to_category(file_records, destination_root, category_name):
    """Move provided files into a category folder and update the database"""
    dest_root = Path(destination_root).expanduser()
    secure_category = secure_filename(category_name) or 'categorized'
    category_dir = dest_root / secure_category
    category_dir.mkdir(parents=True, exist_ok=True)

    moved = []
    errors = []

    db = get_db()

    for record in file_records:
        file_path = Path(record['path'])
        if not file_path.exists():
            errors.append({'file': str(file_path), 'error': 'File not found on disk'})
            continue

        target_path = category_dir / file_path.name
        counter = 1
        while target_path.exists():
            target_path = category_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
            counter += 1

        try:
            shutil.move(str(file_path), target_path)
            stats = target_path.stat()
            db.execute('''UPDATE files SET path = ?, filename = ?, extension = ?, size = ?,
                          modified_date = ?, created_date = ?, indexed_date = ?, file_hash = ?
                          WHERE id = ?''',
                       (str(target_path), target_path.name, target_path.suffix, stats.st_size,
                        datetime.fromtimestamp(stats.st_mtime), datetime.fromtimestamp(stats.st_ctime),
                        datetime.now(), calculate_file_hash(target_path), record['id']))
            moved.append({'from': str(file_path), 'to': str(target_path)})
        except Exception as exc:
            errors.append({'file': str(file_path), 'error': str(exc)})

    db.commit()
    db.close()
    return moved, errors


def get_default_paths():
    """Return common folders for the host OS to help populate the UI"""
    home = Path.home()
    defaults = {
        'home': str(home),
        'documents': str(home / 'Documents'),
        'downloads': str(home / 'Downloads'),
        'desktop': str(home / 'Desktop'),
        'pictures': str(home / 'Pictures')
    }
    return defaults

# ==================== FLASK ROUTES ====================

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """Get system status"""
    ollama_status['installed'] = check_ollama_installed()
    ollama_status['running'] = check_ollama_running()
    if ollama_status['running']:
        ollama_status['models'] = get_ollama_models()
    
    db = get_db()
    file_count = db.execute('SELECT COUNT(*) as count FROM files').fetchone()['count']
    tag_count = db.execute('SELECT COUNT(*) as count FROM tags').fetchone()['count']
    db.close()

    return jsonify({
        'ollama': ollama_status,
        'indexing': indexing_status,
        'stats': {
            'files': file_count,
            'tags': tag_count
        },
        'platform': platform.system(),
        'paths': get_default_paths()
    })

@app.route('/api/search', methods=['POST'])
def api_search():
    """Search files"""
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    results = search_files(query)
    return jsonify({'results': results})

@app.route('/api/scan', methods=['POST'])
def api_scan():
    """Start folder scan"""
    data = request.json
    folder = os.path.expanduser(data.get('folder', ''))

    if not folder or not os.path.exists(folder):
        return jsonify({'error': 'Invalid folder path'}), 400
    
    # Start scan in background thread
    thread = threading.Thread(target=scan_folder, args=(folder,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'started'})

@app.route('/api/ollama/pull', methods=['POST'])
def api_ollama_pull():
    """Pull Ollama model"""
    data = request.json
    model = data.get('model', 'llama3.2:3b')
    
    success = pull_ollama_model(model)
    return jsonify({'success': success})

@app.route('/api/settings', methods=['GET', 'POST'])
def api_settings():
    """Get or update settings"""
    db = get_db()
    
    if request.method == 'GET':
        settings = {}
        rows = db.execute('SELECT key, value FROM settings').fetchall()
        for row in rows:
            settings[row['key']] = row['value']
        db.close()
        return jsonify(settings)
    
    else:  # POST
        data = request.json
        for key, value in data.items():
            db.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)',
                      (key, str(value)))
        db.commit()
        db.close()
        return jsonify({'success': True})

@app.route('/api/files/<int:file_id>')
def api_file_detail(file_id):
    """Get file details"""
    db = get_db()
    
    file = db.execute('''
        SELECT f.*, s.summary, GROUP_CONCAT(t.tag_name, ',') as tags
        FROM files f
        LEFT JOIN summaries s ON f.id = s.file_id
        LEFT JOIN file_tags ft ON f.id = ft.file_id
        LEFT JOIN tags t ON ft.tag_id = t.id
        WHERE f.id = ?
        GROUP BY f.id
    ''', (file_id,)).fetchone()
    
    db.close()

    if file:
        return jsonify(dict(file))
    return jsonify({'error': 'File not found'}), 404


@app.route('/api/files')
def api_files():
    """List files with optional query or tag filtering"""
    query = request.args.get('q', '')
    tag = request.args.get('tag', '')
    limit = int(request.args.get('limit', 50))
    files = fetch_files(query=query if query else None,
                        tag=tag if tag else None,
                        limit=limit)
    return jsonify({'results': files})


@app.route('/api/files/categorize', methods=['POST'])
def api_categorize_files():
    """Categorize files using Ollama tags"""
    payload = request.json or {}
    file_ids = payload.get('file_ids', [])
    paths = payload.get('paths', [])

    if not file_ids and not paths:
        return jsonify({'error': 'No files provided'}), 400

    categorized = []
    errors = []

    # Convert paths into records
    for file_path in paths:
        record = ensure_file_record(os.path.expanduser(file_path))
        if record:
            file_ids.append(record['id'])
        else:
            errors.append({'file': file_path, 'error': 'File could not be indexed'})

    db = get_db()
    for file_id in file_ids:
        record = db.execute('SELECT * FROM files WHERE id = ?', (file_id,)).fetchone()
        if not record:
            errors.append({'file': str(file_id), 'error': 'Unknown file id'})
            continue

        file_path = record['path']
        content = extract_text_content(file_path)
        tags = generate_tags(file_path, content)
        apply_tags_to_file(file_id, tags)

        # Optional summary refresh
        summary = generate_summary(file_path, content)
        if summary:
            db.execute('''INSERT OR REPLACE INTO summaries (file_id, summary, model_used)
                         VALUES (?, ?, ?)''', (file_id, summary, 'llama3.2:3b'))
            db.commit()

        categorized.append({'file_id': file_id, 'tags': tags, 'summary': summary})

    db.close()
    return jsonify({'categorized': categorized, 'errors': errors})


@app.route('/api/files/move', methods=['POST'])
def api_move_files():
    """Move files into a chosen category folder"""
    payload = request.json or {}
    category = payload.get('category', '')
    destination_root = payload.get('destination_root', '')
    file_ids = payload.get('file_ids', [])
    paths = payload.get('paths', [])

    if not category or not destination_root:
        return jsonify({'error': 'Category and destination_root are required'}), 400

    if not file_ids and not paths:
        return jsonify({'error': 'No files selected'}), 400

    records = []
    errors = []
    db = get_db()

    for file_id in file_ids:
        record = db.execute('SELECT * FROM files WHERE id = ?', (file_id,)).fetchone()
        if record:
            records.append(record)
        else:
            errors.append({'file': str(file_id), 'error': 'Unknown file id'})

    db.close()

    for file_path in paths:
        record = ensure_file_record(os.path.expanduser(file_path))
        if record:
            records.append(record)
        else:
            errors.append({'file': file_path, 'error': 'File could not be indexed'})

    moved, move_errors = move_files_to_category(records, destination_root, category)
    errors.extend(move_errors)

    return jsonify({'moved': moved, 'errors': errors})

@app.route('/api/tags')
def api_tags():
    """Get all tags"""
    db = get_db()
    tags = db.execute('SELECT * FROM tags ORDER BY usage_count DESC').fetchall()
    db.close()
    return jsonify([dict(tag) for tag in tags])

# ==================== STARTUP ====================

if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Initialize database
    init_db()
    
    print("=" * 60)
    print("FileSense - AI-Powered Local File Search")
    print("=" * 60)
    print(f"Starting server at http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    # Start Flask app
    app.run(debug=False, host='0.0.0.0', port=5000)
