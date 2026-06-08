document.addEventListener('DOMContentLoaded', () => {
    // --- Tab Switching Logic ---
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
    const copyBtn = document.getElementById('copyBtn');
    
    let currentMarkdown = '';

    generateBtn.addEventListener('click', async () => {
        const apiKey = document.getElementById('apiKey').value.trim();
        if (!apiKey) {
            showToast('Silakan masukkan Gemini API Key terlebih dahulu di pojok kanan atas.');
            return;
        }

        const formData = new FormData();
        formData.append('api_key', apiKey);
        formData.append('source_type', currentSourceType);
        formData.append('style', document.getElementById('article_style').value);

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
            formData.append('file', fileInput.files[0]);
        } else if (currentSourceType === 'local_video') {
            const fileInput = document.getElementById('input_local_video');
            if (fileInput.files.length === 0) return showToast('Pilih file video terlebih dahulu.');
            formData.append('file', fileInput.files[0]);
        }

        // Set Loading State
        generateBtn.disabled = true;
        btnText.classList.add('hidden');
        loader.classList.remove('hidden');
        resultContainer.innerHTML = '<div class="empty-state"><p>Sedang memproses dengan AI... Mohon tunggu.</p></div>';
        copyBtn.disabled = true;

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Terjadi kesalahan pada server');
            }

            // Success
            currentMarkdown = data.data;
            resultContainer.innerHTML = marked.parse(currentMarkdown);
            copyBtn.disabled = false;
            
        } catch (error) {
            console.error('Error:', error);
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

    // --- Copy Logic ---
    copyBtn.addEventListener('click', () => {
        if (!currentMarkdown) return;
        navigator.clipboard.writeText(currentMarkdown).then(() => {
            showToast('Markdown artikel berhasil disalin ke clipboard!', true);
        }).catch(err => {
            showToast('Gagal menyalin teks.');
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
