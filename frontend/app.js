// --- Theme Initialization ---
const savedTheme = localStorage.getItem('app_theme') || 'system';

function applyTheme(theme) {
    if (theme === 'system') {
        const isLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
        if (isLight) {
            document.documentElement.setAttribute('data-theme', 'light');
        } else {
            document.documentElement.removeAttribute('data-theme');
        }
    } else if (theme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
    } else {
        document.documentElement.removeAttribute('data-theme');
    }
}

applyTheme(savedTheme);

// Listen to OS theme changes if 'system' is selected
if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', () => {
        const currentTheme = localStorage.getItem('app_theme') || 'system';
        if (currentTheme === 'system') {
            applyTheme('system');
        }
    });
}

// --- Token Check ---
const authToken = localStorage.getItem('ARSA_token');
if (!authToken) {
    window.location.href = 'login.html';
}

// --- UI Localization logic moved to lang.js ---

document.addEventListener('DOMContentLoaded', () => {
    // --- Theme Selector Logic ---
    const themeSelect = document.getElementById('setting_theme');
    if (themeSelect) {
        themeSelect.value = savedTheme;
        themeSelect.addEventListener('change', (e) => {
            const newTheme = e.target.value;
            applyTheme(newTheme);
            localStorage.setItem('app_theme', newTheme);
        });
    }

    // --- UI Language Selector Logic ---
    const uiLangSelect = document.getElementById('ui_language');
    if (uiLangSelect) {
        uiLangSelect.value = savedUiLang;
        uiLangSelect.addEventListener('change', (e) => {
            const newLang = e.target.value;
            applyUILanguage(newLang);
            localStorage.setItem('app_ui_lang', newLang);
        });
    }

    // --- Fetch Initial Settings ---
    let savedAiModel = "gemini-2.5-flash";
    let savedHfModel = "mistralai/Mistral-7B-Instruct-v0.3";
    let savedGroqModel = "llama-3.1-8b-instant";

    fetch('http://localhost:8000/api/settings', {
        headers: { 'Authorization': `Bearer ${authToken}` }
    })
    .then(res => res.json())
    .then(data => {
        if (data.ai_provider) {
            document.getElementById('setting_ai_provider').value = data.ai_provider;
            toggleProviderSettings(data.ai_provider);
        }
        if (data.api_key) {
            document.getElementById('setting_api_key').value = data.api_key;
            if (data.ai_model) savedAiModel = data.ai_model;
            if (data.ai_provider === 'gemini') loadAvailableModels(data.api_key, savedAiModel, 'gemini');
        }
        if (data.hf_api_key) {
            document.getElementById('setting_hf_api_key').value = data.hf_api_key;
            if (data.hf_model) savedHfModel = data.hf_model;
            if (data.ai_provider === 'huggingface') loadAvailableModels(data.hf_api_key, savedHfModel, 'huggingface');
        }
        if (data.groq_api_key) {
            document.getElementById('setting_groq_api_key').value = data.groq_api_key;
            if (data.groq_model) savedGroqModel = data.groq_model;
            if (data.ai_provider === 'groq') loadAvailableModels(data.groq_api_key, savedGroqModel, 'groq');
        }
        if (data.wp_url) document.getElementById('setting_wp_url').value = data.wp_url;
        if (data.wp_username) document.getElementById('setting_wp_user').value = data.wp_username;
        if (data.wp_app_password) document.getElementById('setting_wp_pwd').value = data.wp_app_password;
    }).catch(err => console.error("Gagal memuat pengaturan", err));

    // --- Tab Switching Logic (Main) ---
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    let currentSourceType = 'manual_text';

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            // Add active class to clicked
            btn.classList.add('active');
            const targetId = btn.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active');

            currentSourceType = targetId;
        });
    });

    // --- Generate Logic ---
    const generateBtn = document.getElementById('generateBtn');
    const btnText = generateBtn.querySelector('.btn-text');
    const loader = generateBtn.querySelector('.loader');
    const resultContainer = document.getElementById('result_content');
    const resultEditor = document.getElementById('result_editor');
    const editorWrapper = document.getElementById('editor_wrapper');
    
    // Custom Toolbar Logic
    document.querySelectorAll('.toolbar-btn, .toolbar-dropdown-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            if(!btn.dataset.action) return; // Abaikan tombol toggle dropdown
            e.preventDefault(); // Mencegah link <a> melompat ke atas halaman
            
            const action = btn.dataset.action;
            const start = resultEditor.selectionStart;
            const end = resultEditor.selectionEnd;
            const text = resultEditor.value;
            const selected = text.substring(start, end);
            let replacement = selected;

            switch(action) {
                case 'bold': replacement = `**${selected || 'teks tebal'}**`; break;
                case 'italic': replacement = `*${selected || 'teks miring'}*`; break;
                case 'h1': replacement = `\n# ${selected || 'Judul Utama'}\n`; break;
                case 'h2': replacement = `\n## ${selected || 'Subjudul'}\n`; break;
                case 'link': 
                    const url = prompt("Masukkan Tautan (URL):", "https://");
                    if(url) replacement = `[${selected || 'Teks Tautan'}](${url})`;
                    break;
                case 'image': 
                    const imgUrl = prompt("Masukkan Tautan Gambar (URL):", "https://");
                    if(imgUrl) replacement = `![${selected || 'Deskripsi Gambar'}](${imgUrl})`;
                    break;
                case 'list': replacement = `\n- ${selected || 'Poin 1'}`; break;
                case 'ordered-list': replacement = `\n1. ${selected || 'Poin 1'}`; break;
            }

            resultEditor.focus();
            resultEditor.setSelectionRange(start, end);
            
            // Gunakan execCommand agar perubahan masuk ke history Undo (Ctrl+Z) browser
            if (!document.execCommand('insertText', false, replacement)) {
                // Fallback jika browser tidak mendukung
                resultEditor.setRangeText(replacement, start, end, 'end');
            }

            // Pindahkan kursor ke tengah jika tidak ada teks yang diblok
            if (!selected) {
                let offset = action === 'bold' ? 2 : action === 'italic' ? 1 : 0;
                if(action === 'h1' || action === 'h2' || action === 'list' || action === 'ordered-list') offset = replacement.length;
                if(action === 'link' || action === 'image') offset = replacement.length;
                const newCursorPos = start + offset;
                resultEditor.setSelectionRange(newCursorPos, newCursorPos);
            }
        });
    });

    // Auto-continue lists in the raw textarea
    resultEditor.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            const start = this.selectionStart;
            const text = this.value;
            // Dapatkan baris saat ini
            const lineStart = text.lastIndexOf('\n', start - 1) + 1;
            const lineText = text.substring(lineStart, start);
            
            // Cek apakah baris ini dimulai dengan bullet (- , * , + ) atau angka (1. )
            const match = lineText.match(/^(\s*)([-*+]|\d+\.)\s+(.*)$/);
            
            if (match) {
                e.preventDefault();
                const indent = match[1];
                let bullet = match[2];
                const content = match[3];

                // Jika barisnya hanya bullet kosong, Enter kedua akan menghapus bullet tersebut
                if (!content.trim()) {
                    this.setRangeText('\n', lineStart, start, 'end');
                    return;
                }
                
                // Jika itu list angka, otomatis tambahkan angkanya
                if (/^\d+\.$/.test(bullet)) {
                    bullet = parseInt(bullet, 10) + 1 + '.';
                }
                
                const replacement = `\n${indent}${bullet} `;
                if (!document.execCommand('insertText', false, replacement)) {
                    this.setRangeText(replacement, start, start, 'end');
                }
            }
        }
        
        // Tab key for indentation
        if (e.key === 'Tab') {
            e.preventDefault();
            const start = this.selectionStart;
            const end = this.selectionEnd;
            const replacement = "    "; // 4 spaces
            
            if (!document.execCommand('insertText', false, replacement)) {
                this.setRangeText(replacement, start, end, 'end');
            }
        }
        
        // Ctrl+B for Bold
        if (e.ctrlKey && (e.key === 'b' || e.key === 'B')) {
            e.preventDefault();
            const start = this.selectionStart;
            const end = this.selectionEnd;
            const selected = this.value.substring(start, end);
            const replacement = `**${selected || 'teks tebal'}**`;
            
            if (!document.execCommand('insertText', false, replacement)) {
                this.setRangeText(replacement, start, end, 'end');
            }
            if (!selected) {
                const newPos = start + 2;
                this.setSelectionRange(newPos, newPos);
            }
        }
        
        // Ctrl+I for Italic
        if (e.ctrlKey && (e.key === 'i' || e.key === 'I')) {
            e.preventDefault();
            const start = this.selectionStart;
            const end = this.selectionEnd;
            const selected = this.value.substring(start, end);
            const replacement = `*${selected || 'teks miring'}*`;
            
            if (!document.execCommand('insertText', false, replacement)) {
                this.setRangeText(replacement, start, end, 'end');
            }
            if (!selected) {
                const newPos = start + 1;
                this.setSelectionRange(newPos, newPos);
            }
        }
    });

    const copyBtn = document.getElementById('copyBtn');
    const exportDropdownContainer = document.getElementById('exportDropdownContainer');
    const editBtn = document.getElementById('editBtn');
    const publishWpContainer = document.getElementById('publishWpContainer');
    const uploadFallbackBtn = document.getElementById('uploadFallbackBtn');
    const fallbackImageInput = document.getElementById('fallbackImageInput');

    let currentMarkdown = '';

    generateBtn.addEventListener('click', async () => {
        const formData = new FormData();
        formData.append('source_type', currentSourceType);
        formData.append('style', document.getElementById('article_style').value);
        formData.append('language', document.getElementById('article_language').value);

        // Append input based on active tab
        if (currentSourceType === 'manual_text') {
            const text = document.getElementById('input_manual_text').value.trim();
            if (!text) return showToast('Teks referensi tidak boleh kosong.');
            formData.append('manual_text', text);
        } else if (currentSourceType === 'web_url') {
            const url = document.getElementById('input_web_url').value.trim();
            if (!url) return showToast('URL Web tidak boleh kosong.');
            formData.append('url', url);
        } else if (currentSourceType === 'youtube_url') {
            const url = document.getElementById('input_youtube_url').value.trim();
            if (!url) return showToast('URL YouTube tidak boleh kosong.');
            formData.append('url', url);
        } else if (currentSourceType === 'document') {
            const fileInput = document.getElementById('input_document');
            if (fileInput.files.length === 0) return showToast('Pilih file dokumen terlebih dahulu.');
            const file = fileInput.files[0];
            if (file.size > 20 * 1024 * 1024) return showToast('Ukuran file dokumen maksimal 20 MB.');
            formData.append('file', file);
        } else if (currentSourceType === 'local_video') {
            const fileInput = document.getElementById('input_local_video');
            if (fileInput.files.length === 0) return showToast('Pilih file video terlebih dahulu.');
            const file = fileInput.files[0];
            if (file.size > 500 * 1024 * 1024) return showToast('Ukuran file video maksimal 500 MB.');
            formData.append('file', file);
        }

        // Set Loading State
        generateBtn.disabled = true;
        btnText.classList.add('hidden');
        loader.classList.remove('hidden');

        resultContainer.innerHTML = `
            <div class="empty-state">
                <div class="progress-container">
                    <p id="progress_text" class="progress-text">${(localStorage.getItem('app_ui_lang') || 'id') === 'en' ? 'Preparing data...' : 'Menyiapkan data...'}</p>
                    <div class="progress-bar-bg">
                        <div id="progress_fill" class="progress-fill"></div>
                    </div>
                    <p id="progress_percentage" class="progress-percentage">0%</p>
                </div>
            </div>`;

        resultContainer.classList.remove('hidden');
        editorWrapper.classList.add('hidden');
        copyBtn.disabled = true;
        copyBtn.classList.add('hidden');
        editBtn.classList.add('hidden');
        publishWpContainer.classList.add('hidden');
        exportDropdownContainer.classList.add('hidden');
        uploadFallbackBtn.classList.add('hidden');
        isEditing = false;
        editBtn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg><span>Edit</span>';

        // --- Fake Progress Logic ---
        let progress = 0;
        const progressFill = document.getElementById('progress_fill');
        const progressText = document.getElementById('progress_text');
        const progressPercentage = document.getElementById('progress_percentage');

        const currentUiLang = localStorage.getItem('app_ui_lang') || 'id';
        const statusMessages = currentUiLang === 'en' ? [
            "Extracting reference data...",
            "Understanding sentence context...",
            "Building article framework...",
            "Stringing words together...",
            "Perfecting AI grammar...",
            "Almost done, please be patient..."
        ] : [
            "Menyedot data referensi...",
            "Memahami konteks kalimat...",
            "Membangun kerangka artikel...",
            "Merangkai kata demi kata...",
            "Menyempurnakan tata bahasa AI...",
            "Hampir selesai, mohon bersabar..."
        ];

        let statusIndex = 0;

        // Interval for progress bar
        const progressInterval = setInterval(() => {
            // Asymptotic progress towards 95%
            let increment = Math.random() * 5;
            if (progress > 80) increment = Math.random() * 1;
            if (progress > 90) increment = Math.random() * 0.2;

            progress += increment;
            if (progress > 95) progress = 95;

            progressFill.style.width = `${progress}%`;
            progressPercentage.textContent = `${Math.floor(progress)}%`;
        }, 800);

        // Interval for status text
        const textInterval = setInterval(() => {
            statusIndex = (statusIndex + 1) % statusMessages.length;
            progressText.textContent = statusMessages[statusIndex];
        }, 4000);

        const startTime = performance.now();

        try {
            const response = await fetch('http://localhost:8000/api/generate', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${authToken}` },
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Terjadi kesalahan pada server');
            }

            // Success - Snap to 100%
            clearInterval(progressInterval);
            clearInterval(textInterval);
            progressFill.style.width = '100%';
            progressFill.classList.add('success');
            progressPercentage.textContent = '100%';
            progressText.textContent = 'Selesai! Memuat hasil...';

            // Wait 500ms for user to see 100% completion before showing text
            await new Promise(resolve => setTimeout(resolve, 500));

            currentMarkdown = data.data;
            resultContainer.innerHTML = marked.parse(currentMarkdown);
            copyBtn.disabled = false;
            copyBtn.classList.remove('hidden');
            editBtn.classList.remove('hidden');
            publishWpContainer.classList.remove('hidden');
            exportDropdownContainer.classList.remove('hidden');
            uploadFallbackBtn.classList.remove('hidden');

            const endTime = performance.now();
            const execTimeSeconds = ((endTime - startTime) / 1000).toFixed(1);
            const wordCount = currentMarkdown.trim().split(/\s+/).filter(word => word.length > 0).length;
            const readingTime = Math.ceil(wordCount / 200);

            // Show Metrics
            document.getElementById('wordCount').textContent = wordCount;
            document.getElementById('readingTime').textContent = readingTime;
            document.getElementById('execTime').textContent = execTimeSeconds;
            document.getElementById('tokenCount').textContent = data.tokens_used;
            document.getElementById('metricsIndicator').classList.remove('hidden');

        } catch (error) {
            console.error('Error:', error);
            clearInterval(progressInterval);
            clearInterval(textInterval);
            showToast(error.message);
            resultContainer.innerHTML = `<div class="empty-state" style="color: var(--danger)">
                <p>Gagal menghasilkan artikel: ${error.message}</p>
            </div>`;
        } finally {
            // Reset Loading State
            generateBtn.disabled = false;
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
        }
    });

    // --- Live Edit Logic ---
    let isEditing = false;
    editBtn.addEventListener('click', () => {
        if (!currentMarkdown) return;

        if (!isEditing) {
            // Switch to Edit Mode
            resultContainer.classList.add('hidden');
            editorWrapper.classList.remove('hidden');
            resultEditor.value = currentMarkdown;
            publishWpContainer.classList.add('hidden'); // Sembunyikan publish saat mengedit
            exportDropdownContainer.classList.add('hidden'); // Sembunyikan ekspor

            editBtn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg><span>Save & Preview</span>';
            editBtn.style.background = "var(--primary)";
            editBtn.style.color = "white";
            isEditing = true;
        } else {
            // Save and switch to Preview Mode
            currentMarkdown = resultEditor.value;
            resultContainer.innerHTML = marked.parse(currentMarkdown);
            editorWrapper.classList.add('hidden');
            resultContainer.classList.remove('hidden');
            publishWpContainer.classList.remove('hidden');
            exportDropdownContainer.classList.remove('hidden');

            // Update Metrics based on edited content
            const wordCount = currentMarkdown.trim().split(/\s+/).filter(word => word.length > 0).length;
            const readingTime = Math.ceil(wordCount / 200);
            document.getElementById('wordCount').textContent = wordCount;
            document.getElementById('readingTime').textContent = readingTime;

            editBtn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg><span>Edit</span>';
            editBtn.style.background = "";
            editBtn.style.color = "";
            isEditing = false;
        }
    });

    // --- Copy Logic ---
    copyBtn.addEventListener('click', () => {
        if (!currentMarkdown) return;
        navigator.clipboard.writeText(currentMarkdown).then(() => {
            showToast('Markdown artikel berhasil disalin ke clipboard!', true);
        }).catch(err => {
            showToast('Gagal menyalin teks.');
        });
    });

    // --- Export Logic ---
    const exportDropdownBtn = document.getElementById('exportDropdownBtn');
    
    // Download PDF (Print Method)
    document.getElementById('exportPdfBtn').addEventListener('click', (e) => {
        e.preventDefault();
        window.print();
    });

    // Download Word (.docx)
    document.getElementById('exportWordBtn').addEventListener('click', async (e) => {
        e.preventDefault();
        if (!currentMarkdown) return;

        showToast("Sedang merakit dokumen Word...", true);
        const titleMatch = currentMarkdown.match(/^# (.*)$/m);
        const title = titleMatch ? titleMatch[1] : "Artikel";

        const formData = new FormData();
        formData.append('title', title);
        formData.append('content', currentMarkdown);

        try {
            const response = await fetch('http://localhost:8000/api/export/word', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error("Gagal mengekspor dokumen Word");

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${title.substring(0, 30)}.docx`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            showToast("Berhasil mengunduh dokumen Word!", true);
        } catch (error) {
            console.error(error);
            showToast(error.message);
        }
    });

    // Download TXT
    document.getElementById('exportTxtBtn').addEventListener('click', (e) => {
        e.preventDefault();
        if (!currentMarkdown) return;
        const blob = new Blob([currentMarkdown], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "artikel_mentah.txt";
        a.click();
        window.URL.revokeObjectURL(url);
    });

    // Download MD
    document.getElementById('exportMdBtn').addEventListener('click', (e) => {
        e.preventDefault();
        if (!currentMarkdown) return;
        const blob = new Blob([currentMarkdown], { type: 'text/markdown' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "artikel_mentah.md";
        a.click();
        window.URL.revokeObjectURL(url);
    });

    // --- Upload Fallback Image Logic ---
    uploadFallbackBtn.addEventListener('click', () => {
        fallbackImageInput.click();
    });

    fallbackImageInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            uploadFallbackBtn.disabled = true;
            uploadFallbackBtn.style.opacity = '0.5';

            const response = await fetch('http://localhost:8000/api/upload-image', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || 'Gagal upload gambar');

            const markdownImage = `\n![Gambar Cover](http://localhost:8000${data.image_url})\n`;

            const lines = currentMarkdown.split('\n');
            let insertIndex = 0;
            let foundOldImage = false;
            
            for (let i = 0; i < lines.length; i++) {
                if (lines[i].startsWith('# ')) {
                    insertIndex = i + 1;
                    // Cek 3 baris ke bawah apakah sudah ada gambar lama
                    for (let j = insertIndex; j < insertIndex + 3 && j < lines.length; j++) {
                        if (lines[j].trim().startsWith('![')) {
                            lines[j] = markdownImage; // Timpa gambar lama
                            foundOldImage = true;
                            break;
                        }
                    }
                    break;
                }
            }
            
            // Jika artikel tadinya tidak punya gambar sama sekali, sisipkan baru
            if (!foundOldImage) {
                lines.splice(insertIndex, 0, markdownImage);
            }
            
            currentMarkdown = lines.join('\n');

            if (isEditing) {
                resultEditor.value = currentMarkdown;
            } else {
                resultContainer.innerHTML = marked.parse(currentMarkdown);
            }

            showToast('Gambar berhasil disisipkan!', true);
        } catch (error) {
            console.error(error);
            showToast(error.message);
        } finally {
            uploadFallbackBtn.disabled = false;
            uploadFallbackBtn.style.opacity = '1';
            fallbackImageInput.value = ''; // reset
        }
    });

    // --- Settings Modal Logic ---
    const settingsModal = document.getElementById('settingsModal');
    const settingsBtn = document.getElementById('settingsBtn');
    const settingsDropdownBtn = document.getElementById('settingsDropdownBtn');
    const closeSettingsBtn = document.getElementById('closeSettingsBtn');
    const saveSettingsBtn = document.getElementById('saveSettingsBtn');
    const modalTabBtns = document.querySelectorAll('.modal-tab-btn');
    const modalTabPanes = document.querySelectorAll('.modal-tab-pane');

    if (settingsBtn) settingsBtn.addEventListener('click', () => settingsModal.classList.remove('hidden'));
    if (settingsDropdownBtn) {
        settingsDropdownBtn.addEventListener('click', () => {
            const profileDropdown = document.getElementById('profileDropdown');
            if(profileDropdown) profileDropdown.classList.remove('show');
            settingsModal.classList.remove('hidden');
        });
    }
    
    if (closeSettingsBtn) closeSettingsBtn.addEventListener('click', () => settingsModal.classList.add('hidden'));

    modalTabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            modalTabBtns.forEach(b => b.classList.remove('active'));
            modalTabPanes.forEach(p => p.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(btn.getAttribute('data-target')).classList.add('active');
        });
    });

    // --- AI Provider UI Toggle ---
    const providerSelect = document.getElementById('setting_ai_provider');
    const geminiSettings = document.getElementById('gemini_settings_group');
    const hfSettings = document.getElementById('hf_settings_group');
    const groqSettings = document.getElementById('groq_settings_group');

    function toggleProviderSettings(provider) {
        geminiSettings.classList.add('hidden');
        hfSettings.classList.add('hidden');
        groqSettings.classList.add('hidden');

        if (provider === 'gemini') geminiSettings.classList.remove('hidden');
        else if (provider === 'huggingface') hfSettings.classList.remove('hidden');
        else if (provider === 'groq') groqSettings.classList.remove('hidden');
    }

    providerSelect.addEventListener('change', (e) => {
        toggleProviderSettings(e.target.value);
    });

    // --- API Key & Model Logic ---
    const testApiBtn = document.getElementById('testApiBtn');
    const testStatusText = document.getElementById('testStatusText');
    const modelSelectGroup = document.getElementById('modelSelectGroup');
    const modelSelect = document.getElementById('setting_ai_model');

    const testHfApiBtn = document.getElementById('testHfApiBtn');
    const testHfStatusText = document.getElementById('testHfStatusText');
    const hfModelSelectGroup = document.getElementById('hfModelSelectGroup');
    const hfModelSelect = document.getElementById('setting_hf_model');

    const testGroqApiBtn = document.getElementById('testGroqApiBtn');
    const testGroqStatusText = document.getElementById('testGroqStatusText');
    const groqModelSelectGroup = document.getElementById('groqModelSelectGroup');
    const groqModelSelect = document.getElementById('setting_groq_model');

    testApiBtn.addEventListener('click', async () => {
        const apiKey = document.getElementById('setting_api_key').value.trim();
        if (!apiKey) {
            testStatusText.textContent = "API Key kosong!";
            testStatusText.className = "text-danger";
            return;
        }

        testApiBtn.disabled = true;
        testApiBtn.textContent = "Testing...";
        testStatusText.textContent = "Menghubungi Google...";
        testStatusText.className = "";

        try {
            const res = await fetch('http://localhost:8000/api/test-key', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ api_key: apiKey, provider: "gemini" })
            });
            const data = await res.json();

            if (res.ok) {
                testStatusText.textContent = "✅ Koneksi Berhasil!";
                testStatusText.className = "text-success";
                loadAvailableModels(apiKey, savedAiModel, "gemini");
            } else {
                testStatusText.textContent = "❌ " + (data.detail || "Gagal terkoneksi");
                testStatusText.className = "text-danger";
            }
        } catch (e) {
            testStatusText.textContent = "❌ Gagal jaringan";
            testStatusText.className = "text-danger";
        } finally {
            testApiBtn.disabled = false;
            testApiBtn.textContent = "Test";
        }
    });

    testHfApiBtn.addEventListener('click', async () => {
        const apiKey = document.getElementById('setting_hf_api_key').value.trim();
        if (!apiKey) {
            testHfStatusText.textContent = "Hugging Face Token kosong!";
            testHfStatusText.className = "text-danger";
            return;
        }

        testHfApiBtn.disabled = true;
        testHfApiBtn.textContent = "Testing...";
        testHfStatusText.textContent = "Menghubungi Hugging Face...";
        testHfStatusText.className = "";

        try {
            const res = await fetch('http://localhost:8000/api/test-key', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ api_key: apiKey, provider: "huggingface" })
            });
            const data = await res.json();

            if (res.ok) {
                testHfStatusText.textContent = "✅ Koneksi Token Berhasil!";
                testHfStatusText.className = "text-success";
                loadAvailableModels(apiKey, savedHfModel, "huggingface");
            } else {
                testHfStatusText.textContent = "❌ " + (data.detail || "Gagal terkoneksi");
                testHfStatusText.className = "text-danger";
            }
        } catch (e) {
            testHfStatusText.textContent = "❌ Gagal jaringan";
            testHfStatusText.className = "text-danger";
        } finally {
            testHfApiBtn.disabled = false;
            testHfApiBtn.textContent = "Test";
        }
    });

    testGroqApiBtn.addEventListener('click', async () => {
        const apiKey = document.getElementById('setting_groq_api_key').value.trim();
        if (!apiKey) {
            testGroqStatusText.textContent = "Groq API Key kosong!";
            testGroqStatusText.className = "text-danger";
            return;
        }

        testGroqApiBtn.disabled = true;
        testGroqApiBtn.textContent = "Testing...";
        testGroqStatusText.textContent = "Menghubungi Groq...";
        testGroqStatusText.className = "";

        try {
            const res = await fetch('http://localhost:8000/api/test-key', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ api_key: apiKey, provider: "groq" })
            });
            const data = await res.json();

            if (res.ok) {
                testGroqStatusText.textContent = "✅ Koneksi Berhasil!";
                testGroqStatusText.className = "text-success";
                loadAvailableModels(apiKey, savedGroqModel, "groq");
            } else {
                testGroqStatusText.textContent = "❌ " + (data.detail || "Gagal terkoneksi");
                testGroqStatusText.className = "text-danger";
            }
        } catch (e) {
            testGroqStatusText.textContent = "❌ Gagal jaringan";
            testGroqStatusText.className = "text-danger";
        } finally {
            testGroqApiBtn.disabled = false;
            testGroqApiBtn.textContent = "Test";
        }
    });

    async function loadAvailableModels(apiKey, selectedModel = null, provider = "gemini") {
        try {
            const res = await fetch('http://localhost:8000/api/models', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ api_key: apiKey, provider: provider })
            });
            const data = await res.json();
            if (res.ok && data.models.length > 0) {
                let targetSelect, targetGroup;
                if (provider === "gemini") { targetSelect = modelSelect; targetGroup = modelSelectGroup; }
                else if (provider === "huggingface") { targetSelect = hfModelSelect; targetGroup = hfModelSelectGroup; }
                else if (provider === "groq") { targetSelect = groqModelSelect; targetGroup = groqModelSelectGroup; }

                targetSelect.innerHTML = '';
                data.models.forEach(m => {
                    const opt = document.createElement('option');
                    opt.value = m.name;
                    opt.textContent = m.display_name || m.name;

                    // Menonaktifkan model yang tidak didukung (jika ada flag is_supported dari backend)
                    if (m.hasOwnProperty('is_supported') && !m.is_supported) {
                        opt.disabled = true;
                    }

                    // Hanya tandai selected jika model tersebut didukung
                    if (m.name === selectedModel && (!m.hasOwnProperty('is_supported') || m.is_supported)) {
                        opt.selected = true;
                    }
                    targetSelect.appendChild(opt);
                });
                targetGroup.classList.remove('hidden');
            }
        } catch (e) {
            console.error("Gagal memuat model", e);
        }
    }

    saveSettingsBtn.addEventListener('click', async () => {
        const payload = {
            ai_provider: document.getElementById('setting_ai_provider').value,
            api_key: document.getElementById('setting_api_key').value.trim(),
            ai_model: document.getElementById('setting_ai_model').value || 'gemini-2.5-flash',
            hf_api_key: document.getElementById('setting_hf_api_key').value.trim(),
            hf_model: document.getElementById('setting_hf_model').value || 'mistralai/Mistral-7B-Instruct-v0.3',
            groq_api_key: document.getElementById('setting_groq_api_key').value.trim(),
            groq_model: document.getElementById('setting_groq_model').value || 'llama-3.1-8b-instant',
            wp_url: document.getElementById('setting_wp_url').value.trim(),
            wp_username: document.getElementById('setting_wp_user').value.trim(),
            wp_app_password: document.getElementById('setting_wp_pwd').value.trim()
        };

        saveSettingsBtn.disabled = true;
        saveSettingsBtn.textContent = 'Menyimpan...';

        try {
            const response = await fetch('http://localhost:8000/api/settings', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authToken}`
                },
                body: JSON.stringify(payload)
            });
            const data = await response.json();
            if (response.ok) {
                showToast('Pengaturan berhasil disimpan di Database', true);
                settingsModal.classList.add('hidden');
            } else {
                showToast(data.detail || 'Gagal menyimpan pengaturan');
            }
        } catch (err) {
            showToast('Terjadi kesalahan jaringan.');
        } finally {
            saveSettingsBtn.disabled = false;
            saveSettingsBtn.textContent = 'Simpan Pengaturan';
        }
    });

    // --- WordPress Publish Logic ---
    async function publishToWordPress(status) {
        if (!currentMarkdown) return;

        // Coba ekstrak judul dari markdown (H1)
        const match = currentMarkdown.match(/^# (.*?)$/m);
        let title = match ? match[1].trim() : "Artikel AI Tanpa Judul";

        const statusLabel = status === 'publish' ? 'Langsung (Live)' : 'sebagai Draft';
        // Konfirmasi cepat
        if (!confirm(`Publikasikan artikel ke WordPress ${statusLabel}?\nJudul: ${title}`)) return;

        const publishDropdownBtn = document.getElementById('publishDropdownBtn');
        const originalText = publishDropdownBtn.querySelector('span').textContent;
        publishDropdownBtn.disabled = true;
        publishDropdownBtn.querySelector('span').textContent = 'Mem-publish...';

        const fd = new FormData();
        fd.append('title', title);
        fd.append('content', currentMarkdown);
        fd.append('status', status);

        try {
            const response = await fetch('http://localhost:8000/api/publish/wordpress', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${authToken}` },
                body: fd
            });
            const data = await response.json();

            if (response.ok) {
                showToast(data.message || `Berhasil di-publish ke WordPress (${status})!`, true);
            } else {
                showToast(data.detail || 'Gagal publish.');
            }
        } catch (err) {
            showToast('Gagal terhubung ke server.');
        } finally {
            publishDropdownBtn.disabled = false;
            publishDropdownBtn.querySelector('span').textContent = originalText;
        }
    }

    document.getElementById('publishDraftBtn').addEventListener('click', (e) => {
        e.preventDefault();
        publishToWordPress('draft');
    });

    document.getElementById('publishLiveBtn').addEventListener('click', (e) => {
        e.preventDefault();
        publishToWordPress('publish');
    });

    // --- File Input UI Update ---
    const fileInputs = document.querySelectorAll('.file-upload input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', (e) => {
            const label = e.target.nextElementSibling;
            if (e.target.files.length > 0) {
                label.textContent = e.target.files[0].name;
                label.style.color = "var(--primary)";
                label.style.borderColor = "var(--primary)";
                label.style.background = "rgba(99, 102, 241, 0.05)";
            } else {
                label.textContent = e.target.id === 'input_document' ? 'Pilih File' : 'Pilih Video (Semua Format)';
                label.style.color = "";
                label.style.borderColor = "";
                label.style.background = "";
            }
        });
    });

    // --- Toast Notification ---
    function showToast(message, isSuccess = false) {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.className = `toast ${isSuccess ? 'success' : ''}`;

        setTimeout(() => {
            toast.classList.add('hidden');
        }, 3000);
    }
});
