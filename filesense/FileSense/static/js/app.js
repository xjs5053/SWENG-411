const state = {
    files: [],
    tags: [],
    defaults: {},
};

function showSection(name) {
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    document.querySelector(`#section-${name}`).classList.add('active');
    document.querySelectorAll('.nav-link').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.section === name);
    });
}

function setupNavigation() {
    document.querySelectorAll('.nav-link').forEach(btn => {
        btn.addEventListener('click', () => showSection(btn.dataset.section));
    });

    document.getElementById('search-submit').addEventListener('click', searchFiles);
    document.getElementById('global-search').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchFiles();
    });
}

async function refreshStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();

        document.getElementById('stat-files').textContent = data.stats.files;
        document.getElementById('stat-tags').textContent = data.stats.tags;
        document.getElementById('pill-files').textContent = `Files: ${data.stats.files}`;
        document.getElementById('pill-tags').textContent = `Tags: ${data.stats.tags}`;

        state.defaults = data.paths || {};
        document.getElementById('stat-path').textContent = state.defaults.home || '';

        const ollamaRunning = data.ollama.running;
        document.getElementById('stat-ollama').textContent = ollamaRunning ? 'Running' : 'Not Running';
        document.getElementById('stat-models').textContent = data.ollama.models && data.ollama.models.length
            ? `Models: ${data.ollama.models.join(', ')}` : 'Models: none detected';
        document.getElementById('pill-ollama').textContent = `Ollama: ${ollamaRunning ? 'Running' : 'Not running'}`;
        document.getElementById('sidebar-ollama').textContent = ollamaRunning ? 'Ollama • Running' : 'Ollama • Offline';

        const indexing = data.indexing;
        document.getElementById('stat-index').textContent = indexing.active ? 'Indexing…' : 'Idle';
        document.getElementById('stat-progress').textContent = indexing.active
            ? `${indexing.progress} / ${indexing.total} • ${indexing.current_file}`
            : 'Start a scan to populate results';
        document.getElementById('sidebar-indexing').textContent = indexing.active ? 'Indexing • Active' : 'Indexing • Idle';

        if (indexing.total > 0) {
            const percent = Math.round((indexing.progress / indexing.total) * 100);
            document.getElementById('progress-label').textContent = indexing.active ? `Indexing ${percent}%` : 'Complete';
            document.getElementById('progress-fill').style.width = `${percent}%`;
        }
    } catch (err) {
        console.error('Status error', err);
    }
}

async function loadFiles() {
    const response = await fetch('/api/files?limit=80');
    const data = await response.json();
    state.files = data.results || [];
    renderFileList('file-browser', state.files);
    renderFileList('batch-list', state.files, true);
    renderFileList('recent-list', state.files.slice(0, 12));
}

async function loadTags() {
    const response = await fetch('/api/tags');
    state.tags = await response.json();

    const cloud = document.getElementById('tags-cloud');
    const explorer = document.getElementById('tag-explorer');

    if (!state.tags.length) {
        cloud.innerHTML = '<div class="helper-text">Index some files to see tags.</div>';
        explorer.innerHTML = '<div class="helper-text">No tags yet.</div>';
        return;
    }

    cloud.innerHTML = state.tags.slice(0, 30).map(tag => `<span class="chip" onclick="searchByTag('${tag.tag_name}')">${tag.tag_name} (${tag.usage_count})</span>`).join('');
    explorer.innerHTML = cloud.innerHTML;
}

async function loadSettings() {
    const response = await fetch('/api/settings');
    const settings = await response.json();
    document.getElementById('auto-tag').checked = settings.auto_tag === 'true';
    document.getElementById('auto-summarize').checked = settings.auto_summarize === 'true';
    document.getElementById('ollama-model').value = settings.ollama_model || 'llama3.2:3b';
}

async function saveSettings() {
    const settings = {
        auto_tag: document.getElementById('auto-tag').checked ? 'true' : 'false',
        auto_summarize: document.getElementById('auto-summarize').checked ? 'true' : 'false',
        ollama_model: document.getElementById('ollama-model').value
    };
    const response = await fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings)
    });
    const data = await response.json();
    if (data.success) alert('Settings saved');
}

function renderFileList(targetId, files, selectable = false) {
    const container = document.getElementById(targetId);
    if (!files || !files.length) {
        container.innerHTML = '<div class="list-item empty">No files yet. Start a scan.</div>';
        return;
    }

    container.innerHTML = files.map(file => {
        const tags = file.tags ? file.tags.split(',').map(t => `<span class="tag">${t}</span>`).join('') : '';
        const checkbox = selectable ? `<div class="checkbox-cell"><input type="checkbox" class="batch-checkbox" data-id="${file.id}"><div><h4>${file.filename}</h4><div class="path">${file.path}</div></div></div>` : `<h4>${file.filename}</h4>`;
        return `
            <div class="list-item">
                <header>
                    ${checkbox}
                    <div class="meta">${formatBytes(file.size)} • ${formatDate(file.modified_date)}</div>
                </header>
                <div class="path">${file.path}</div>
                ${file.summary ? `<div class="summary">${file.summary}</div>` : ''}
                <div>${tags}</div>
            </div>
        `;
    }).join('');
}

function selectAllBatch(flag) {
    document.querySelectorAll('.batch-checkbox').forEach(cb => cb.checked = flag);
}

function getSelectedFileIds() {
    return Array.from(document.querySelectorAll('.batch-checkbox:checked')).map(cb => Number(cb.dataset.id));
}

async function searchFiles() {
    const query = document.getElementById('global-search').value.trim();
    if (!query) return;
    showSection('search');
    const results = document.getElementById('search-results');
    results.innerHTML = '<div class="list-item">Searching…</div>';
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        const data = await response.json();
        if (!data.results || !data.results.length) {
            results.innerHTML = '<div class="list-item empty">No matches</div>';
            return;
        }
        renderFileList('search-results', data.results);
    } catch (err) {
        results.innerHTML = '<div class="list-item empty">Search failed</div>';
    }
}

function searchByTag(tag) {
    document.getElementById('global-search').value = tag;
    searchFiles();
}

async function startScan() {
    const folder = document.getElementById('folder-path').value.trim();
    if (!folder) { alert('Enter a folder path'); return; }
    const response = await fetch('/api/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ folder })
    });
    const data = await response.json();
    if (data.status === 'started') {
        document.getElementById('progress-label').textContent = 'Indexing…';
    } else if (data.error) {
        alert(data.error);
    }
}

function quickFolder(key) {
    if (state.defaults[key]) {
        document.getElementById('folder-path').value = state.defaults[key];
        startScan();
    }
}

async function pullModel(model) {
    const btn = event.target;
    btn.disabled = true;
    btn.textContent = 'Pulling…';
    const response = await fetch('/api/ollama/pull', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model })
    });
    const data = await response.json();
    btn.textContent = data.success ? 'Started' : 'Failed';
    setTimeout(() => { btn.disabled = false; btn.textContent = `Pull ${model.split(':')[1].toUpperCase()}`; }, 2500);
}

async function testOllama() {
    const result = document.getElementById('test-result');
    result.textContent = 'Testing…';
    const response = await fetch('/api/status');
    const data = await response.json();
    if (data.ollama.running) {
        result.textContent = `✅ Ollama running. Models: ${data.ollama.models.join(', ') || 'none'}`;
        result.className = 'helper-text success';
    } else {
        result.textContent = '❌ Ollama not reachable. Start the Ollama service.';
        result.className = 'helper-text error';
    }
}

async function categorizeSelected() {
    const ids = getSelectedFileIds();
    if (!ids.length) { alert('Select at least one file'); return; }
    document.getElementById('batch-feedback').textContent = 'Tagging with Ollama…';
    const response = await fetch('/api/files/categorize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_ids: ids })
    });
    const data = await response.json();
    document.getElementById('batch-feedback').textContent = `Tagged ${data.categorized.length} files.`;
    loadFiles();
    loadTags();
}

async function moveSelected() {
    const ids = getSelectedFileIds();
    const category = document.getElementById('batch-category').value.trim();
    const destination = document.getElementById('batch-destination').value.trim();
    if (!ids.length) { alert('Select at least one file'); return; }
    if (!category || !destination) { alert('Provide category and destination'); return; }

    document.getElementById('batch-feedback').textContent = 'Moving files…';
    const response = await fetch('/api/files/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_ids: ids, category, destination_root: destination })
    });
    const data = await response.json();
    const movedCount = data.moved ? data.moved.length : 0;
    const errorCount = data.errors ? data.errors.length : 0;
    document.getElementById('batch-feedback').textContent = `Moved ${movedCount} files${errorCount ? `, ${errorCount} errors` : ''}.`;
    loadFiles();
}

function formatBytes(bytes) {
    if (!bytes) return '0 B';
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`;
}

function formatDate(str) {
    if (!str) return '';
    const d = new Date(str);
    return `${d.toLocaleDateString()} ${d.toLocaleTimeString()}`;
}

window.addEventListener('DOMContentLoaded', () => {
    setupNavigation();
    refreshStatus();
    loadFiles();
    loadTags();
    loadSettings();
    setInterval(refreshStatus, 4000);
});
