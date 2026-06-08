import google.generativeai as genai

class AIGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None

    def generate_article(self, source_context: str, style: str = "blog", custom_prompt: str = "") -> str:
        """
        Kompilasi prompt terstruktur dan kirim ke API LLM (Gemini)
        """
        if not self.model:
            return "**Error:** API Key Gemini tidak disetel atau tidak valid."

        base_prompt = f"""
Anda adalah seorang penulis dan jurnalis profesional berkaliber tinggi. Buatlah artikel berkualitas tinggi dalam Bahasa Indonesia berdasarkan data referensi berikut.

=== REFERENSI SUMBER ===
{source_context[:10000]} # Batasi konteks agar tidak melampaui token limit
========================

=== PENGATURAN ===
- Gaya Penulisan: {style.upper()} (Sesuaikan tone: berita = formal, blog = santai, akademik = analitis)
{f'- Instruksi Tambahan: {custom_prompt}' if custom_prompt else ''}

=== INSTRUKSI MUTLAK ===
1. Buat satu judul (maksimal 70 karakter) di baris PALING PERTAMA dan beri format Heading 1 (# Judul).
2. Tulis isi artikel dengan format Markdown lengkap yang rapi dan terstruktur.
3. Gunakan paragraf yang proporsional, heading (## atau ###), dan list peluru/angka jika diperlukan.
4. Artikel harus komprehensif, kaya informasi, dan mengalir secara natural.
5. HANYA berikan hasil artikelnya saja (Markdown), JANGAN ADA teks pengantar.
"""
        try:
            response = self.model.generate_content(base_prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Gagal melakukan generasi artikel dengan Gemini AI: {str(e)}")
