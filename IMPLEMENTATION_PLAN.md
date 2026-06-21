# Rencana Implementasi: Fitur Manajemen Email & OTP (Masa Depan)

Dokumen ini juga mencatat cetak biru untuk pengembangan fitur **Penggantian Email** di masa mendatang jika skala keamanan sistem ditingkatkan. Mengingat email digunakan sebagai ID sandi utama, pengamanan sangat diperlukan.

## Tiga Opsi Arsitektur Penggantian Email

### 1. Tingkat Dasar: *Direct Overwrite* (Tanpa Pengaman)
*   **Pendekatan:** Pengguna dapat mengetik email baru dan sistem langsung menimpanya.
*   **Implementasi:** Membuka fungsi atribut `disabled` pada input HTML `account_email` dan menambahkan pembaruan di API `PUT /api/auth/profile`.
*   **Risiko:** Rentan terhadap kesalahan ketik (*typo*). Jika pengguna salah ketik (contoh: `gmai.com`), mereka akan kehilangan akses *login* untuk selamanya.

### 2. Tingkat Menengah: Konfirmasi Kata Sandi Lama
*   **Pendekatan:** Sama seperti Tingkat Dasar, namun sebelum tombol "Simpan" diproses, server mewajibkan verifikasi *password* saat ini.
*   **Kelebihan:** Melindungi akun agar email tidak diganti diam-diam oleh orang lain yang meminjam *browser* pengguna.
*   **Kelemahan:** Tetap tidak ada validasi apakah alamat email yang diketik *typo* atau tidak valid.

### 3. Tingkat Profesional: Verifikasi OTP via Email (Standar Industri)
*   **Pendekatan:** Implementasi standar tertinggi (seperti sistem Google/SaaS modern).
*   **Alur Kerja:**
    1. Pengguna mengetik email baru di kolom pengaturan.
    2. *Frontend* menghubungi `POST /api/auth/request-email-change`.
    3. *Backend* (menggunakan library `smtplib` di Python dan *App Password* milik akun Gmail sistem/admin) mengirim email berisi 6 Digit Kode OTP ke alamat email yang baru.
    4. Pengguna melihat layar *Pop-up Modal* yang meminta kode OTP tersebut.
    5. Pengguna mengetik 6 digit OTP. *Frontend* mengirimkannya ke `POST /api/auth/verify-email-change`.
    6. *Backend* mencocokkan OTP (biasanya disimpan sementera menggunakan Redis atau di tabel DB terpisah dengan masa kadaluarsa 5 menit).
    7. Jika cocok, alamat email di database akan diperbarui menjadi yang baru.
*   **Kelebihan:** 100% aman anti-*typo* dan terhindar dari pengambilalihan akun.
*   **Kebutuhan Ekstra:** Mewajibkan penambahan dan konfigurasi akun email SMTP pada server (misalnya *Gmail SMTP*).

---

# Rencana Implementasi: Kesiapan Deployment (Production-Ready)

Mencatat strategi untuk memastikan aplikasi berjalan mulus baik saat dikembangkan secara lokal maupun saat di-*deploy* ke server internet.

## Variabel Cerdas (Smart Router API Base URL)
*   **Masalah Saat Ini:** Semua fungsi `fetch()` di dalam *file* `frontend/app.js` menggunakan *hardcode* `http://localhost:8000/api/...`. Jika *frontend* di-*deploy* ke domain publik (contoh: `arsa-app.com`), *browser* pengguna akan mencoba mencari API dari `localhost` milik komputer mereka sendiri sehingga terjadi *error* koneksi.
*   **Solusi yang Direncanakan:**
    *   Mendeklarasikan variabel penunjuk cerdas di awal *file* `app.js`:
        ```javascript
        const API_BASE_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') && window.location.port === '5500' 
            ? 'http://localhost:8000' 
            : ''; 
        ```
    *   Mengubah semua teks `fetch('http://localhost:8000/api/...')` menjadi `fetch(API_BASE_URL + '/api/...')`.
*   **Keuntungan:** 
    *   Pengembang dapat terus menggunakan Server Lokal (Port 5500 + 8000) tanpa masalah.
    *   Saat kode yang sama persis diunggah ke *server* publik (menggunakan *Reverse Proxy* seperti Nginx atau *FastAPI Static Mount*), aplikasi otomatis menyadari lingkungannya dan menggunakan jalur relatif (`/api/...`), sehingga bebas dari masalah *Cross-Origin (CORS)* dan hilangnya koneksi peladen.
