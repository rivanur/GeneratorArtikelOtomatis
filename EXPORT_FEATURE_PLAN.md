# Rencana Implementasi: Fitur Ekspor Komprehensif (4-in-1)

Dokumen ini berisi cetak biru (*blueprint*) untuk pengembangan fitur unduhan (ekspor) artikel di masa mendatang. Fitur ini dirancang untuk mendukung 4 format standar industri: **PDF, Microsoft Word (.docx), Plain Text (.txt), dan Markdown (.md)**.

## 1. Arsitektur Ekspor ke Microsoft Word (.docx)
*   **Pendekatan:** *Backend Processing* (Meniru arsitektur *StudioFlow*)
*   **Library:** `python-docx` (penulis file Word) & `BeautifulSoup4` (HTML Parser)
*   **Alur Kerja:**
    1.  Teks *Markdown* di-*generate* oleh AI.
    2.  *Frontend* mengirimkan teks *Markdown* ke *endpoint* baru: `POST /api/export/word`.
    3.  *Backend* mengubah *Markdown* menjadi elemen HTML sementara.
    4.  `BeautifulSoup` membedah elemen HTML (misal: tag `<h1>` dikonversi menjadi *Heading 1* di Word).
    5.  `python-docx` merakit elemen-elemen tersebut menjadi sebuah dokumen biner `.docx` yang bersih dan terstruktur.
    6.  *Backend* mengirim *File Response* kembali ke *Browser* agar pengguna langsung mengunduhnya.

## 2. Arsitektur Ekspor ke PDF (.pdf)
*   **Pendekatan:** *Frontend Print Mode* (Lebih efisien & bebas instalasi library raksasa seperti Playwright)
*   **Alur Kerja:**
    1.  Tambahkan instruksi CSS `@media print` di `index.css`. Aturan ini akan di-set agar menyembunyikan (*display: none*) seluruh elemen UI pembantu (navigasi, latar gelap, *sidebar*, *progress bar*).
    2.  Saat tombol "Download PDF" ditekan, JavaScript akan memanggil fungsi bawaan peramban `window.print()`.
    3.  Peramban (seperti Chrome/Edge) akan secara otomatis meluncurkan dialog cetak dengan opsi *Save as PDF*, menampilkan kertas putih bersih yang hanya berisi teks artikel dan gambar.

## 3. Arsitektur Ekspor ke Plain Text & Markdown (.txt / .md)
*   **Pendekatan:** *Frontend In-Memory Blob* (Sangat cepat & 0 *server request*)
*   **Alur Kerja:**
    1.  Teks hasil akhir dari AI sudah tersimpan di dalam variabel JavaScript (`currentMarkdown`).
    2.  Saat tombol ditekan, buat objek `Blob` dari variabel teks tersebut.
    3.  Buat URL sementara menggunakan `URL.createObjectURL(blob)`.
    4.  Ciptakan elemen tautan tak terlihat (`<a href>`), tempelkan nama file (*e.g.,* `Artikel.md`), lalu paksa tautan tersebut untuk ter-klik secara otomatis. 
    5.  File langsung terunduh seketika.

## 4. Perubahan Antarmuka Pengguna (UI) yang Diperlukan
*   Grup tombol baru di bilah atas "Hasil Artikel", berdampingan dengan tombol "Copy" dan "Edit".
*   Grup ini sebaiknya dikelompokkan ke dalam satu tombol menu (*Dropdown*) bertajuk **"Unduh Sebagai ⬇️"** untuk menjaga kebersihan visual antarmuka pengguna.
