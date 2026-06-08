# Panduan Menjalankan Sistem Generator Artikel Otomatis

Dokumen ini berisi panduan lengkap langkah demi langkah untuk menjalankan prototipe sistem **Generator Artikel Otomatis** di komputer lokal Anda. Sistem ini dibangun menggunakan Python (FastAPI) untuk logika pemrosesan dan antarmuka web modern berbasis HTML/CSS/JS.

---

## 📋 Prasyarat Sistem

Sebelum memulai, pastikan komputer Anda telah memenuhi persyaratan berikut:

1. **Python:** Komputer Anda harus sudah terinstal Python (disarankan versi 3.9 ke atas).
   *   *Cara cek:* Buka Terminal/Command Prompt (CMD) lalu ketik `python --version`. Jika muncul versinya, berarti sudah terinstal.
2. **Koneksi Internet:** Dibutuhkan untuk mengunduh pustaka (*library*), membaca artikel dari *website*, dan mengirim instruksi ke API Google Gemini.
3. **Google Gemini API Key:** Anda harus memiliki API Key gratis dari Google AI Studio.
   *   *Cara mendapatkan:* Kunjungi [Google AI Studio](https://aistudio.google.com/), masuk dengan akun Google, lalu klik **"Get API key"** dan buat kunci baru. Salin teks kunci tersebut.

---

## 🛠️ Langkah Instalasi

Ikuti langkah-langkah di bawah ini untuk memasang seluruh kebutuhan aplikasi.

### Langkah 1: Buka Terminal di Folder Proyek
1. Buka File Explorer dan masuk ke folder `d:\GeneratorArtikelOtomatis`.
2. Klik *address bar* (baris lokasi) di bagian atas File Explorer, hapus teksnya, ketik `cmd`, lalu tekan **Enter**. Ini akan membuka *Command Prompt* yang langsung mengarah ke folder proyek Anda.

### Langkah 2: Buat Virtual Environment (Sangat Disarankan)
Untuk menjaga agar instalasi aplikasi ini tidak mengganggu Python di sistem Anda yang lain, buat lingkungan virtual (*virtual environment*).
Di *Command Prompt*, jalankan perintah:
```bash
python -m venv venv
```
Setelah selesai, aktifkan *virtual environment* tersebut:
*   **Untuk pengguna Windows:**
    ```bash
    venv\Scripts\activate
    ```
*(Tanda `(venv)` akan muncul di awal baris Command Prompt Anda jika berhasil).*

### Langkah 3: Instal Pustaka (Library) yang Dibutuhkan
Instal semua dependensi sistem dengan perintah berikut:
```bash
pip install -r requirements.txt
```
Tunggu hingga proses unduhan dan instalasi selesai.

---

## 🚀 Cara Menjalankan Server Aplikasi

Setelah semua pustaka terinstal, Anda siap untuk menyalakan *backend* server.

1. Di terminal yang sama (pastikan posisi masih di folder `d:\GeneratorArtikelOtomatis`), jalankan perintah:
   ```bash
   python main.py
   ```
2. Terminal akan menampilkan tulisan:
   `🚀 Memulai server di http://localhost:8000`
   *(Jangan tutup jendela terminal ini selama Anda masih menggunakan aplikasi).*

---

## 💻 Cara Menggunakan Aplikasi

1. Buka peramban internet (*browser*) seperti Google Chrome, Microsoft Edge, atau Firefox.
2. Ketik alamat berikut di kolom URL dan tekan Enter:
   **http://localhost:8000**
3. Anda akan disambut oleh antarmuka premium "Generator Artikel AI".
4. **Masukkan API Key:** Di pojok kanan atas, masukkan (atau *paste*) **Google Gemini API Key** yang sudah Anda siapkan sebelumnya.
5. **Pilih Sumber:** Di panel sebelah kiri, pilih tipe sumber teks (Misal: Teks Manual, URL Web, atau unggah dokumen PDF).
   *   *Contoh termudah:* Pilih tab **"URL Web"**, lalu tempel *link* ke suatu berita atau artikel Wikipedia.
6. **Pilih Gaya:** Pilih gaya penulisan yang diinginkan pada menu *dropdown* (Misal: Gaya Blog, Gaya Berita).
7. Klik tombol **"Generate Artikel"**.
8. Sistem akan menampilkan animasi *loading* sementara AI sedang bekerja. Dalam beberapa detik, artikel lengkap dengan *formatting* yang rapi (Markdown) akan muncul di panel sebelah kanan!
9. Anda dapat menyalin (*copy*) hasilnya dengan menekan tombol **Copy** di sudut kanan atas panel hasil artikel.

---

## 🛑 Cara Menghentikan Aplikasi
Jika Anda sudah selesai menggunakan aplikasi:
1. Kembali ke *Command Prompt* tempat server berjalan.
2. Tekan kombinasi *keyboard* `Ctrl + C` untuk mematikan server.
3. Anda boleh menutup jendela *Command Prompt* tersebut.
