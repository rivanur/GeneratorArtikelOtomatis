# Rencana Implementasi: Fitur Masa Depan & Catatan Arsitektur

Dokumen ini mencatat cetak biru untuk pengembangan fitur di masa mendatang serta catatan arsitektur penting untuk menangani limitasi infrastruktur awan (*Cloud*).

---

## 1. Fitur Manajemen Email & OTP (Masa Depan)

Mengingat email digunakan sebagai ID sandi utama, pengamanan ekstra untuk proses pergantian email sangat diperlukan. Berikut adalah opsi arsitektur yang direncanakan:

### A. Tingkat Dasar: *Direct Overwrite* (Tanpa Pengaman)
*   **Pendekatan:** Pengguna dapat mengetik email baru dan sistem langsung menimpanya.
*   **Risiko:** Rentan terhadap kesalahan ketik (*typo*). Jika pengguna salah ketik, mereka akan kehilangan akses *login* selamanya.

### B. Tingkat Menengah: Konfirmasi Kata Sandi Lama
*   **Pendekatan:** Mewajibkan verifikasi *password* saat ini sebelum menyimpan email baru.
*   **Kelebihan:** Melindungi akun dari pengambilalihan perangkat (*browser hijacking*).
*   **Kelemahan:** Tetap rentan terhadap *typo* email tujuan.

### C. Tingkat Profesional: Verifikasi OTP via Email (Standar Industri)
*   **Alur Kerja:**
    1. Pengguna mengetik email baru.
    2. *Frontend* memanggil `POST /api/auth/request-email-change`.
    3. *Backend* (menggunakan `smtplib` dan *Gmail App Password*) mengirimkan 6 Digit OTP ke email baru tersebut.
    4. Pengguna memasukkan OTP.
    5. *Backend* memvalidasi OTP di Redis/Tabel DB sementara.
    6. Jika valid, alamat email diperbarui.
*   **Kelebihan:** 100% aman dari *typo* dan peretasan.

---

## 2. Manajemen Ketersediaan Fitur (Penanganan Pemblokiran Bot)

*   **Latar Belakang Masalah:** Mesin komputasi awan (seperti Render) sering kali di-daftarhitamkan (*blacklisted*) atau dicurigai oleh layanan pihak ketiga (terutama YouTube) karena lalu lintas data terdeteksi berasal dari robot/bot. Hal ini menyebabkan kegagalan unduhan media (`HTTP 400: Sign in to confirm you're not a bot`).
*   **Solusi Sementara (Telah Diimplementasikan):** Menyembunyikan antarmuka (*tab* fitur) yang diblokir tersebut secara dinamis khusus di lingkungan *Production*, namun tetap membukanya di lingkungan *Localhost*.
*   **Mekanisme:**
    *   *Frontend* (melalui `app.js`) mendeteksi `window.location.hostname`.
    *   Jika aplikasi berjalan di luar `localhost` atau `127.0.0.1` (contoh: diakses melalui Cloudflare Pages), tombol tab "YouTube" (`data-target="youtube_url"`) akan diubah menjadi `display: none`.
    *   Hal ini mencegah pengguna *Production* berhadapan dengan pesan *error* yang tidak dapat dihindari, namun tetap memberikan keleluasaan penuh bagi pengembang untuk melakukan uji coba di komputer lokal mereka.
*   **Rencana Solusi Jangka Panjang:**
    *   Mengeksplorasi penggunaan *Proxy Rotator* atau manajemen penyuapan *Cookies* (ekspor *cookies* peramban asli) ke dalam konfigurasi `yt-dlp` di sisi *Backend* untuk mengelabui deteksi bot YouTube saat berjalan di *server Cloud*.

---

## 3. Integrasi API Pencarian Gambar Resmi (Anti-Blokir)

*   **Latar Belakang Masalah:** Saat ini pencarian gambar ilustrasi menggunakan *library* `duckduckgo-search` (teknik *scraping*). Sama seperti kasus YouTube, mesin pencari seperti DuckDuckGo sering memblokir permintaan atau memperlambat koneksi hingga *Timeout* saat mendeteksi *traffic* yang berasal dari peladen komputasi awan (Render IP).
*   **Rencana Solusi (Masa Depan):** Mengganti teknik *scraping* DuckDuckGo dengan menggunakan jalur resmi (*Official API*) dari penyedia gambar berlisensi gratis. Penggunaan API resmi membutuhkan *API Key* sehingga akses dari *Server Cloud* akan dikenali sebagai *developer* sah dan terhindar dari blokir 100%.
*   **Kandidat Penyedia API:**
    1.  **Unsplash API:** Kualitas foto estetik dan premium. Kuota gratis: 50 *request*/jam. (Paling direkomendasikan).
    2.  **Pexels API:** Mirip Unsplash dengan resolusi tinggi. Kuota gratis cukup besar.
    3.  **Pixabay API:** Cocok untuk gambar ilustrasi vektor atau grafis selain foto.
*   **Langkah Implementasi Kelak:**
    1.  Mendaftarkan akun developer di Unsplash/Pexels dan mengenerate *API Key*.
    2.  Menyimpan *API Key* tersebut ke dalam *Environment Variables* di mesin Render.
    3.  Merombak kode di `core/ai_generator.py` dan `api/routes.py` (bagian fungsi pencarian gambar) untuk melakukan `HTTP GET` langsung ke *endpoint* API penyedia tersebut alih-alih menggunakan `ddgs`.

---

## 4. Penyimpanan Objek Permanen (Cloudinary untuk Media)

*   **Latar Belakang Masalah:** Mesin awan gratis (*Free Tier*) seperti Render menggunakan sistem *Ephemeral Filesystem* (Sistem File Sementara). Artinya, setiap *file* yang diunggah pengguna (seperti foto profil ke dalam direktori `/uploads`) akan **terhapus secara fisik** setiap kali mesin tertidur (*sleep* karena *idle*) atau dimuat ulang (*restart/deploy*). Hal ini menyebabkan *link* gambar rusak (*broken image*) pada tampilan UI pengguna.
*   **Rencana Solusi (Masa Depan):** Menghilangkan kebergantungan pada penyimpanan lokal mesin peladen dan beralih menggunakan layanan *Cloud Object Storage* pihak ketiga, seperti **Cloudinary**.
*   **Langkah Implementasi Kelak:**
    1.  Mendaftarkan akun di Cloudinary (memberikan kuota gratis penyimpanan dan *bandwidth* yang sangat besar untuk media).
    2.  Menambahkan kredensial *API Key*, *API Secret*, dan *Cloud Name* milik Cloudinary ke dalam *Environment Variables* di Render.
    3.  Menambahkan *library* `cloudinary` ke dalam `requirements.txt`.
    4.  Merombak fungsi unggah gambar (contoh: `POST /api/auth/profile-picture` di `routes.py`) agar mengirim aliran data gambar (`bytes`) langsung ke *endpoint* unggah Cloudinary.
    5.  Cloudinary akan membalas dengan memberikan URL publik (contoh: `https://res.cloudinary.com/.../foto_rivan.jpg`).
    6.  URL publik inilah yang kelak disimpan secara permanen di dalam kolom `profile_picture` di *database* TiDB.

---

## 5. Arsitektur Komponen Frontend (Mencegah Duplikasi Kode)

*   **Latar Belakang Masalah:** Saat ini aplikasi menggunakan arsitektur *Vanilla HTML Statis*. Artinya, komponen umum seperti `Navbar` (Menu Atas) dan `Footer` (Menu Bawah) di- *copy-paste* secara manual ke dalam setiap *file* (`index.html`, `help.html`, `terms.html`, dll). Jika ada 1 perubahan desain di Navbar, *programmer* harus mengingat dan mengedit semua *file* tersebut satu per satu. Kelalaian manusia (*Human Error*) dalam mengubah 1 file saja akan menyebabkan tampilan rusak/berbeda (*Inconsistent UI*).
*   **Rencana Solusi (Masa Depan):** Kita harus beralih ke arsitektur berbasis Komponen (*Component-Based*) agar satu kode dapat dipakai ulang (*Reusability*).
*   **Opsi Implementasi:**
    *   **Opsi A (JavaScript Injection - Paling Mudah):** 
        Membuat *file* khusus bernama `navbar.html`. Di setiap halaman lainnya, kita cukup meletakkan `<div id="navbar-placeholder"></div>`. Lalu, kita menggunakan JavaScript `fetch('navbar.html')` untuk secara otomatis menyuntikkan menu tersebut ke semua halaman saat dimuat. 
        *Kelebihan:* Sangat mudah diterapkan tanpa mengubah infrastruktur Cloudflare Pages.
    *   **Opsi B (Static Site Generator / Vite - Standar Industri):**
        Memasukkan alat *Build* otomatis seperti ViteJS. Kita membuat komponen terpisah, dan sistem akan merakitnya secara otomatis menjadi *file* HTML utuh sebelum di-*push* ke Cloudflare.
        *Kelebihan:* Performa sangat cepat dan profesional, namun butuh *setup* Node.js.
    *   **Opsi C (Jinja2 / Server-Side Rendering):**
        Memindahkan tugas *rendering* HTML dari Cloudflare kembali ke mesin Python (FastAPI Render) menggunakan teknologi Jinja2 Templates (`{% extends 'base.html' %}`).
        *Kelebihan:* Sangat rapi ala kerangka kerja Python (Django/Flask), namun membebani mesin Render Anda.
