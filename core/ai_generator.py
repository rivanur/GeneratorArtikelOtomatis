import google.generativeai as genai
import os
import time

class AIGenerator:
    def __init__(self, api_key: str, model_name: str = 'gemini-2.5-flash'):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(model_name)
        else:
            self.model = None

    def generate_article(self, source_context: str, style: str = "blog", custom_prompt: str = "", media_path: str = None) -> dict:
        """
        Kompilasi prompt terstruktur dan kirim ke API LLM (Gemini)
        Bisa menerima teks (source_context) atau file media (media_path)
        """
        if not self.model:
            return "**Error:** API Key Gemini tidak disetel atau tidak valid."

        # Tentukan Persona berdasarkan Gaya
        style_lower = style.lower()
        if "blog" in style_lower or "santai" in style_lower:
            persona = "seorang blogger kreatif dan *storyteller* yang asyik. Gunakan gaya bahasa kasual, bersahabat, sedikit humoris, dan menggunakan istilah kekinian yang mudah dipahami (seperti sapaan santai)."
        elif "akademik" in style_lower or "analitis" in style_lower:
            persona = "seorang peneliti akademis bergelar Profesor. Gunakan bahasa Indonesia baku yang sangat formal, objektif, logis, terstruktur ketat, dan gunakan istilah ilmiah yang relevan."
        elif "seo" in style_lower or "optimasi" in style_lower:
            persona = "seorang pakar SEO Copywriter kelas atas. Tulisan Anda harus persuasif, mudah dipindai mata (*scannable*), mengoptimalkan kepadatan kata kunci secara natural, dan sangat memikat audiens."
        else: # Default (Berita/Formal)
            persona = "seorang jurnalis investigatif senior berkaliber tinggi. Gunakan bahasa Indonesia jurnalistik yang lugas, padat, netral, objektif, dan informatif tanpa opini pribadi."

        base_prompt = f"""
PERAN ANDA:
Anda adalah {persona}

TUGAS:
Buatlah sebuah artikel berkualitas tinggi dalam Bahasa Indonesia berdasarkan data referensi berikut.

=== REFERENSI SUMBER ===
{source_context[:10000]}
========================

=== PENGATURAN TAMBAHAN ===
- Instruksi Khusus: {custom_prompt if custom_prompt else "Tidak ada."}

=== INSTRUKSI MUTLAK & FORMAT ===
1. PERTahankan peran Anda ({persona}) dari awal hingga akhir tulisan! JANGAN gunakan gaya bahasa robotik atau *template* standar AI. Buat tulisan senatural mungkin seperti buatan manusia.
2. Buat satu judul (maksimal 70 karakter) yang sangat memikat di baris PALING PERTAMA dengan format Heading 1 (# Judul).
3. Tulis isi artikel dengan format Markdown lengkap yang rapi dan terstruktur. Gunakan paragraf pendek agar mudah dibaca.
4. Gunakan heading (## atau ###), cetak tebal (**bold**), dan list peluru/angka jika diperlukan untuk menonjolkan poin penting.
5. Artikel harus komprehensif, mengalir secara natural, dan sesuai dengan data referensi.
6. HANYA berikan hasil artikelnya saja (Markdown mentah), JANGAN ADA teks pengantar, penutup, atau basa-basi AI (seperti "Berikut adalah artikelnya...").
"""
        try:
            prompt_parts = [base_prompt]
            uploaded_file = None
            
            # Jika ada media lokal, unggah ke Gemini
            if media_path and os.path.exists(media_path):
                uploaded_file = genai.upload_file(media_path)
                
                # Tunggu jika file butuh proses (misal video besar)
                while uploaded_file.state.name == 'PROCESSING':
                    time.sleep(2)
                    uploaded_file = genai.get_file(uploaded_file.name)
                    
                if uploaded_file.state.name == 'FAILED':
                    raise Exception("Gagal memproses video di server Gemini.")
                    
                prompt_parts.append(uploaded_file)
            
            # Count tokens before generation to show estimate
            token_count = self.model.count_tokens(prompt_parts).total_tokens
            response = self.model.generate_content(prompt_parts)
            
            # Bersihkan file dari server Google setelah dipakai
            if uploaded_file:
                genai.delete_file(uploaded_file.name)
                
            return {
                "text": response.text,
                "tokens_used": token_count
            }
        except Exception as e:
            raise Exception(f"Gagal melakukan generasi artikel dengan Gemini AI: {str(e)}")

    @staticmethod
    def test_api_key(api_key: str) -> bool:
        try:
            genai.configure(api_key=api_key)
            # Fetch models as a quick test
            models = list(genai.list_models())
            return len(models) > 0
        except Exception:
            return False

    @staticmethod
    def get_available_models(api_key: str) -> list:
        try:
            genai.configure(api_key=api_key)
            models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    models.append({
                        "name": m.name.replace('models/', ''),
                        "display_name": m.display_name
                    })
            return models
        except Exception:
            return []
