# 🎓 Rencana Pengembangan Fitur untuk Jurnal Magang

Dokumen ini berisi rangkuman ide, analisis status fitur saat ini, dan rekomendasi tindak lanjut agar proyek **Generator Artikel Otomatis** ini layak diangkat menjadi jurnal ilmiah tingkat lanjut.

---

## 🔍 Analisis Status Fitur Saat Ini

> [!WARNING]
> Beberapa fitur yang terlihat sudah ada di antarmuka (UI) ternyata belum sepenuhnya beroperasi di *backend*.

### 1. Integrasi WordPress Asli (Auto-Posting)
- **Status:** ⚠️ **Belum Selesai**
- **Analisis:** Di layar (UI) sudah terdapat menu Pengaturan WordPress dan tombol "Publish", bahkan kode di *frontend* (`app.js`) sudah siap mengirim data. Namun, di *backend* (`routes.py`), fungsi (API Endpoint) untuk benar-benar mengunggah artikel ke server WordPress menggunakan *WordPress REST API* **belum ada sama sekali**.
- **Nilai Jurnal:** Menyelesaikan fitur ini akan menjadi inti jurnal yang luar biasa dengan judul seperti *"Otomatisasi Penuh Pembuatan hingga Publikasi Artikel Berbasis AI ke CMS WordPress"*.

### 2. Pencarian Web Otomatis / RAG (Retrieval-Augmented Generation)
- **Status:** ⚠️ **Belum Selesai**
- **Analisis:** Saat ini, sistem memang sudah menggunakan DuckDuckGo, tetapi hanya untuk mencari **Gambar Cover (Ilustrasi)** saja, bukan untuk membaca atau mencari teks berita. Jika pengguna memasukkan "Topik: Berita MotoGP", AI hanya menebak berdasarkan data internal lamanya, bukan berdasarkan berita terbaru dari internet.
- **Nilai Jurnal:** Mengubah sistem ini menjadi RAG sungguhan (sistem mencari referensi teks berita terbaru secara otomatis di web lalu menyuruh AI merangkumnya) adalah teknologi AI tingkat lanjut yang sangat disukai di dunia akademis.

### 3. Pilihan Bahasa Output (Multi-Language)
- **Status:** ❌ **Belum Ada Sama Sekali**
- **Analisis:** Fitur pemilihan bahasa ini belum diimplementasikan.
- **Nilai Jurnal:** Ini adalah *"Low Hanging Fruit"* (fitur yang sangat mudah dibuat namun terlihat sangat keren). LLM sangat pintar menerjemahkan dan merangkum lintas bahasa (misal: sumber referensi video YouTube berbahasa Inggris, diubah menjadi artikel berbahasa Indonesia atau Sunda secara otomatis).

---

## 🚀 Action Plan (Rekomendasi Eksekusi)

Untuk menghasilkan "Fitur Wow" yang bisa segera dinikmati dengan tingkat kesulitan yang terukur, berikut adalah urutan pengerjaan yang direkomendasikan:

1. **Tambahkan Fitur Pilihan Bahasa (Prioritas 1 - Mudah & Cepat)**
   - Menambahkan menu *dropdown* "Bahasa Output: Indonesia / Inggris / Sunda / Jawa" di tampilan awal.
   - Mengubah *prompt backend* agar menginstruksikan AI untuk menulis dalam bahasa yang dipilih.

2. **Selesaikan Integrasi API WordPress (Prioritas 2 - Menjual & Kompleks)**
   - Membangun *endpoint* API di `routes.py`.
   - Menghubungkan sistem ke server WordPress sungguhan via REST API agar artikel beserta metadatanya (Draft/Publish) mendarat dengan mulus di CMS.

3. **Fitur RAG Pencarian Topik (Prioritas 3 - Tingkat Lanjut)**
   - Jika sisa waktu magang masih panjang, bangun fungsi agar AI dapat melakukan *browsing* teks referensi secara mandiri menggunakan `DuckDuckGo Search` khusus untuk mode input "Pencarian Topik".
