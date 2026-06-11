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

## 🚀 Cara Menjalankan Aplikasi (Arsitektur Terpisah)

Sistem ini menggunakan arsitektur modern di mana **Backend** (API) dan **Frontend** (Antarmuka Web) berjalan secara terpisah. Anda harus menyalakan keduanya.

### Langkah 1: Menyalakan Backend (API Server)
1. Di terminal yang sama (pastikan posisi masih di folder `d:\GeneratorArtikelOtomatis` dan *virtual environment* aktif), jalankan perintah:
   ```bash
   python main.py
   ```
2. Terminal akan menampilkan tulisan:
   `Memulai server di http://localhost:8000`
   *(Jangan tutup jendela terminal ini selama Anda masih menggunakan aplikasi).*

### Langkah 2: Menyalakan Frontend (Antarmuka Web)
Buka Terminal (Command Prompt) **BARU**, arahkan ke folder `d:\GeneratorArtikelOtomatis`, lalu jalankan:
```bash
python frontend.py
```
Aplikasi akan langsung terbuka di alamat **http://localhost:5500**.
*(Seperti Backend, jangan tutup terminal ini selama Anda masih menggunakannya).*

---

## 💻 Cara Menggunakan Aplikasi

1. Pastikan **Langkah 1 (Backend)** dan **Langkah 2 (Frontend)** di atas sudah dijalankan.
2. Anda akan disambut oleh antarmuka premium "Generator Artikel AI" di layar *browser* Anda.
3. **Pengaturan API Key & WordPress:** Klik tombol **⚙️ Pengaturan** (ikon roda gigi) di pojok kanan atas.
   *   Masukkan **Google Gemini API Key**.
   *   (Opsional) Masukkan URL WordPress, Username, dan Application Password jika ingin memublikasikan artikel langsung ke *website* Anda.
   *   Klik **Simpan Pengaturan**.
4. **Pilih Sumber:** Di panel sebelah kiri, pilih tipe sumber data yang ingin diekstrak (Misal: Teks Manual, URL Web, YouTube, Dokumen PDF, atau Video Lokal).
   *   *Fitur Unggulan:* Pilih tab **"YouTube"** dan masukkan *link* video. Sistem akan otomatis mengunduh audionya dengan `yt-dlp` dan didengarkan langsung oleh AI.
5. **Pilih Gaya:** Pilih gaya penulisan yang diinginkan pada menu *dropdown* (Misal: Gaya Blog, Gaya Berita).
6. Klik tombol **"Generate Artikel"**.
7. Sistem akan menampilkan animasi *loading* sementara AI sedang bekerja. Dalam beberapa detik, artikel lengkap dengan *formatting* yang rapi (Markdown) akan muncul di panel sebelah kanan!
8. Anda dapat menyalin (*copy*) hasilnya dengan menekan tombol **Copy** di sudut kanan atas panel hasil artikel.

---

## 🛑 Cara Menghentikan Aplikasi
Jika Anda sudah selesai menggunakan aplikasi:
1. Kembali ke *Command Prompt* tempat server berjalan.
2. Tekan kombinasi *keyboard* `Ctrl + C` untuk mematikan server.
3. Anda boleh menutup jendela *Command Prompt* tersebut.
