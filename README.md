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
2. Anda akan melihat *Landing Page* (Halaman Utama) dari **ARSA**. Klik tombol **Login** di pojok kanan atas.
3. Untuk masuk ke Dasbor, Anda wajib menggunakan **Kredensial Login Akses Khusus** (Mock Auth) berikut:
   * **Email:** `admin@ARSA.com`
   * **Password:** `admin123`
4. Setelah berhasil masuk ke Dasbor, klik tombol **⚙️ Pengaturan** (ikon roda gigi) di pojok kanan atas.
   *   Masukkan **Google Gemini API Key** (atau API dari Provider lain yang didukung).
   *   (Opsional) Masukkan URL WordPress, Username, dan Application Password jika ingin memublikasikan artikel langsung ke *website* Anda.
   *   Klik **Simpan Pengaturan**.
5. **Pilih Sumber:** Di panel sebelah kiri, pilih tipe sumber data yang ingin diekstrak (Misal: Teks Manual, URL Web, YouTube, Dokumen PDF, atau Video Lokal).
   *   *Fitur Unggulan:* Pilih tab **"YouTube"** dan masukkan *link* video. Sistem akan otomatis mengunduh audionya dengan `yt-dlp` dan didengarkan langsung oleh AI.
5. **Pilih Gaya:** Pilih gaya penulisan yang diinginkan pada menu *dropdown* (Misal: Gaya Blog, Gaya Berita).
6. Klik tombol **"Generate Artikel"**.
7. Sistem akan menampilkan animasi *loading* sementara AI sedang bekerja. Dalam beberapa detik, artikel lengkap dengan *formatting* yang rapi (Markdown) akan muncul di panel sebelah kanan!
8. Anda dapat menyalin (*copy*) hasilnya dengan menekan tombol **Copy** di sudut kanan atas panel hasil artikel.

## 🗄️ Manajemen Database (TiDB Cloud)

Bagi Anda yang menggunakan TiDB Cloud sebagai database serverless di _Production_, Anda dapat mengelola data Anda melalui **SQL Editor** bawaan mereka.

### Cara Melihat Isi Tabel Pengguna
1. Buka *dashboard* TiDB Cloud Anda lalu pilih **SQL Editor** di panel sebelah kiri.
2. Di lembar kerja *query* hitam, ketik perintah berikut:
   ```sql
   SELECT * FROM users;
   ```
3. Klik tombol **Run** di pojok kanan atas.
4. Anda akan melihat daftar semua pengguna, termasuk status `is_verified` mereka di panel *Result* bawah.

### Cara Mengosongkan/Menghapus Tabel (Hard Reset)
> **Peringatan:** Lakukan ini HANYA jika Anda ingin mengulang sistem (*testing*) atau jika ada pembaruan arsitektur tabel yang menyebabkan error.

1. Buka **SQL Editor** di TiDB Cloud.
2. Ketikkan perintah ini (akan menghapus tabel secara permanen):
   ```sql
   DROP TABLE user_settings;
   DROP TABLE users;
   ```
3. Klik tombol **Run**.
4. **PENTING:** Setelah tabel dihapus, Anda WAJIB me-*restart* (menyalakan ulang) server *backend* Anda (misal di Render) agar SQLAlchemy secara otomatis merakit/membangun tabel yang baru.

### Cara Menghapus Satu Akun Tertentu (Jika Nyangkut)
Jika ada akun yang gagal diverifikasi dan Anda ingin menghapusnya agar orang tersebut bisa mendaftar ulang, gunakan perintah ini:
1. Buka **SQL Editor** di TiDB Cloud.
2. Ketikkan perintah berikut (ubah alamat email sesuai target):
   ```sql
   DELETE FROM users WHERE email = 'email_target@gmail.com';
   ```
3. Klik tombol **Run**. Akun tersebut akan terhapus tanpa mengganggu data pengguna lainnya.

---

## 🛑 Cara Menghentikan Aplikasi
Jika Anda sudah selesai menggunakan aplikasi:
1. Kembali ke *Command Prompt* tempat server berjalan.
2. Tekan kombinasi *keyboard* `Ctrl + C` untuk mematikan server.
3. Anda boleh menutup jendela *Command Prompt* tersebut.
