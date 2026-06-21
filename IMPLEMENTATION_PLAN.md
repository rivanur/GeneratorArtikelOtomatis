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
