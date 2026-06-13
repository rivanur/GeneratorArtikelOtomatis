import google.generativeai as genai
from huggingface_hub import InferenceClient
from groq import Groq
import os
import time

class AIGenerator:
    def __init__(self, provider: str, api_key: str, model_name: str):
        self.provider = provider.lower()
        self.api_key = api_key
        self.model_name = model_name
        self.model = None
        self.hf_client = None
        self.groq_client = None

        if api_key:
            if self.provider == "gemini":
                genai.configure(api_key=self.api_key)
                if self.model_name and self.model_name != "auto":
                    self.model = genai.GenerativeModel(self.model_name)
            elif self.provider == "huggingface":
                if self.model_name and self.model_name != "auto":
                    self.hf_client = InferenceClient(model=self.model_name, token=self.api_key)
            elif self.provider == "groq":
                self.groq_client = Groq(api_key=self.api_key)

    @staticmethod
    def _search_web(query: str, max_results: int = 6) -> str:
        try:
            from ddgs import DDGS
            import requests
            from bs4 import BeautifulSoup
            import concurrent.futures
            
            results = DDGS().text(query, max_results=max_results)
            if not results:
                return "Tidak ada hasil pencarian terbaru."
                
            search_context = f"HASIL PENCARIAN WEB UNTUK '{query}':\n\n"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                'Referer': 'https://www.google.com/'
            }
            
            def fetch_and_parse(res):
                title = res.get('title', '')
                snippet = res.get('body', '')
                href = res.get('href', '')
                
                full_text = snippet # Fallback to snippet
                
                if href:
                    try:
                        response = requests.get(href, headers=headers, timeout=5)
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.text, 'html.parser')
                            paragraphs = soup.find_all('p')
                            article_text = " ".join([p.get_text(strip=True) for p in paragraphs])
                            words = article_text.split()
                            if len(words) > 20:
                                full_text = " ".join(words[:150]) # Batasi 150 kata per artikel agar tidak melebihi limit token AI
                    except Exception:
                        pass # Abaikan error timeout/blokir, kembali ke snippet
                
                return f"Sumber ({title}) [URL: {href}]:\n{full_text}\n\n"
                
            # Gunakan ThreadPoolExecutor agar scraping puluhan website bisa berjalan paralel (bersamaan)
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                scraped_results = list(executor.map(fetch_and_parse, results))
                
            for res_text in scraped_results:
                search_context += res_text
                
            return search_context
        except Exception as e:
            print(f"Web search error: {str(e)}")
            return f"Gagal melakukan pencarian web: {str(e)}"

    def generate_article(self, source_context: str, style: str = "blog", custom_prompt: str = "", media_path: str = None) -> dict:
        """
        Kompilasi prompt terstruktur dan kirim ke API LLM (Gemini atau Hugging Face)
        Bisa menerima teks (source_context) atau file media (media_path)
        """
        if not self.api_key:
            return "**Error:** API Key tidak disetel atau tidak valid."
        
        if self.provider == "huggingface" and media_path:
            raise Exception("Huggingface API saat ini tidak mendukung pemrosesan file media karena limitasi server. Harap gunakan Gemini atau Groq.")

        if self.provider == "groq" and media_path:
            try:
                import os
                config = AIGenerator._load_models_config()
                whisper_model = config.get("groq_whisper_model", "whisper-large-v3")
                
                with open(media_path, "rb") as audio_file:
                    transcription = self.groq_client.audio.transcriptions.create(
                        file=(os.path.basename(media_path), audio_file.read()),
                        model=whisper_model,
                        response_format="text"
                    )
                # Ambil teks transkripsi
                transcribed_text = str(transcription)
                source_context = f"{source_context}\n\n[HASIL TRANSKRIPSI VIDEO/AUDIO DARI GROQ WHISPER]:\n{transcribed_text}"
                media_path = None # Set None agar tidak memicu logika media upload Gemini di bawah
            except Exception as e:
                raise Exception(f"Gagal memproses media menggunakan Groq Whisper: {str(e)}")

        # Deteksi apakah source_context terlalu pendek (kata kunci pencarian)
        words = source_context.split()
        if len(words) < 20 and not source_context.startswith("http"):
            search_results = self._search_web(source_context)
            source_context = f"Topik Kueri: {source_context}\n\n{search_results}"
            
        import datetime
        current_date = datetime.datetime.now().strftime("%d %B %Y")
            
        system_prompt = f"""
INSTRUKSI GAYA PENULISAN:
Tulis artikel ini dengan gaya bahasa: {style}

KONTEKS WAKTU:
Hari ini adalah tanggal: {current_date}

=== PENGATURAN TAMBAHAN (WAJIB DIPATUHI) ===
- Instruksi Khusus: {custom_prompt if custom_prompt else "Tidak ada."}

1. FORMAT & STRUKTUR (GAYA JURNALISTIK):
   - Baris pertama WAJIB berupa Judul Utama menggunakan H1 (`# Judul Artikel yang Menarik`).
   - Tulis layaknya artikel berita/blog profesional dengan paragraf pembuka (lead), isi (body) yang mengalir, dan paragraf penutup yang natural.
   - Gunakan paragraf yang panjang dan mengalir dengan baik. Jangan membuat artikel yang terlihat seperti poin-poin presentasi.
   - Gunakan subjudul (## H2 atau ### H3) HANYA untuk memisahkan bagian utama yang panjang (jangan gunakan subjudul untuk setiap 1-2 kalimat).
   - Gunakan cetak tebal (**bold**) pada entitas penting (nama pemain, tim, skor, stadion).

2. KUALITAS TULISAN & SEO:
   - Tulis ulang informasi secara natural (parafrase), jangan menyalin mentah-mentah dari sumber referensi.
   - HINDARI kata-kata klise khas AI seperti "Kesimpulannya", "Pada akhirnya", "Penting untuk dicatat", atau "Sebagai kesimpulan".
   - HINDARI identitas AI seperti "Sebagai asisten AI", "Berikut adalah artikelnya", atau "Berdasarkan referensi di atas".

3. ATURAN ANTI-HALUSINASI (KODE MERAH):
   - JIKA data referensi TIDAK memuat informasi (misal skor atau jadwal belum ada), Anda WAJIB menyatakan bahwa "Informasi detail belum tersedia saat ini".
   - DILARANG KERAS mengarang, menebak, atau memalsukan fakta/skor demi melengkapi artikel!

4. ISOLASI OUTPUT:
   - HANYA keluarkan hasil artikel dalam format Markdown mentah.
   - JANGAN ADA teks pembuka sebelum judul utama.
   - JANGAN ADA teks penutup/basa-basi setelah kalimat terakhir artikel.
"""

        user_prompt = f"""
TUGAS ANDA:
Tulis artikel SEO-friendly yang terstruktur dengan baik berdasarkan sumber referensi berikut:

SUMBER REFERENSI:
{source_context[:10000]}
========================
--- MULAI ARTIKEL DI BAWAH INI ---
"""
        models_to_try = [self.model_name]
        
        if self.model_name == "auto" or not self.model_name:
            available_models = self.get_available_models(self.provider, self.api_key)
            valid_models = [m["name"] for m in available_models if m["name"] != "auto" and m.get("is_supported", True)]
            models_to_try = valid_models
            
            if not models_to_try:
                raise Exception(f"Tidak ada model cadangan yang tersedia untuk provider {self.provider.capitalize()}")

        last_error = None
        primary_error = None
        for i, current_model in enumerate(models_to_try):
            try:
                if self.model_name == "auto" or not self.model_name:
                    if self.provider == "gemini":
                        self.model = genai.GenerativeModel(current_model, system_instruction=system_prompt)
                    elif self.provider == "huggingface":
                        self.hf_client = InferenceClient(model=current_model, token=self.api_key)
                        
                generated_text = ""
                token_count = 0
                
                if self.provider == "gemini":
                    content_parts = []
                    if media_path:
                        try:
                            # Gemini Media Upload Logic
                            mime_type = "video/mp4" if media_path.endswith('.mp4') else "audio/mpeg"
                            uploaded_file = genai.upload_file(path=media_path, mime_type=mime_type)
                            while uploaded_file.state.name == "PROCESSING":
                                time.sleep(2)
                                uploaded_file = genai.get_file(uploaded_file.name)
                            if uploaded_file.state.name == "FAILED":
                                raise Exception("Pemrosesan file media di server Gemini gagal.")
                            content_parts.append(uploaded_file)
                        except Exception as me:
                            raise Exception(f"Gagal mengunggah/memproses media: {str(me)}")
                    
                    content_parts.append(user_prompt)
                    response = self.model.generate_content(content_parts)
                    generated_text = response.text
                    token_count = response.usage_metadata.total_token_count
                    
                elif self.provider == "huggingface":
                    try:
                        messages = [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ]
                        response = self.hf_client.chat_completion(messages=messages, max_tokens=2048)
                        generated_text = response.choices[0].message.content
                    except Exception as e:
                        error_str = str(e).lower()
                        if "not a chat model" in error_str or "model_not_supported" in error_str:
                            try:
                                formatted_prompt = f"[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{user_prompt} [/INST]"
                                generated_text = self.hf_client.text_generation(prompt=formatted_prompt, max_new_tokens=2048)
                            except Exception as inner_e:
                                raise Exception(f"Chat error: {str(e)} | Teks error: {str(inner_e)}")
                        else:
                            raise e
                    token_count = int(len((system_prompt + user_prompt).split()) * 1.3)
                    
                elif self.provider == "groq":
                    response = self.groq_client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        model=current_model,
                        max_tokens=2048,
                        temperature=0.5
                    )
                    generated_text = response.choices[0].message.content
                    token_count = response.usage.total_tokens
                    
                if i > 0 and (self.model_name == "auto" or not self.model_name):
                    generated_text += f"\n\n*(Catatan Sistem: Artikel dihasilkan secara dinamis menggunakan model cadangan `{current_model}` karena model utama sedang sibuk atau ditarik dari peredaran).*"
                    
                return {
                    "text": generated_text,
                    "tokens_used": token_count
                }
            except Exception as e:
                last_error = str(e)
                if i == 0:
                    primary_error = last_error
                print(f"Model {current_model} gagal: {last_error}. Mencoba model selanjutnya...")
                continue
                
        error_to_show = primary_error if primary_error else last_error
        raise Exception(f"Gagal melakukan generasi artikel dengan {self.provider.capitalize()}. Error utama: {error_to_show}")

    @staticmethod
    def test_api_key(provider: str, api_key: str) -> bool:
        provider = provider.lower()
        if provider == "gemini":
            try:
                genai.configure(api_key=api_key)
                models = list(genai.list_models())
                return len(models) > 0
            except Exception:
                return False
        elif provider == "huggingface":
            try:
                from huggingface_hub import whoami
                whoami(token=api_key)
                return True
            except Exception as e:
                print(f"HF Test Error: {e}")
                return False
        elif provider == "groq":
            try:
                client = Groq(api_key=api_key)
                client.models.list()
                return True
            except Exception:
                return False
        return False

    @staticmethod
    def _load_models_config():
        import json
        import os
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'models.json')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Gagal memuat config/models.json: {e}")
            return {
                "huggingface": [
                    {"name": "mistralai/Mistral-7B-Instruct-v0.3", "display_name": "Mistral 7B Instruct v0.3"},
                    {"name": "meta-llama/Meta-Llama-3-8B-Instruct", "display_name": "Llama 3 (8B Instruct)"}
                ],
                "groq_priority_keywords": [
                    "llama-3.3", "llama-3.1", "llama3", "mixtral", "gemma2"
                ]
            }

    @staticmethod
    def get_available_models(provider: str, api_key: str = "") -> list:
        provider = provider.lower()
        auto_option = {"name": "auto", "display_name": "✨ Otomatis (Rekomendasi Terbaik)", "is_supported": True}
        
        config = AIGenerator._load_models_config()
        
        if provider == "gemini":
            try:
                genai.configure(api_key=api_key)
                models = [auto_option]
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        models.append({
                            "name": m.name.replace('models/', ''),
                            "display_name": m.display_name
                        })
                return models
            except Exception:
                return [auto_option]
        elif provider == "huggingface":
            hf_models = config.get("huggingface", [])
            return [auto_option] + hf_models
        elif provider == "groq":
            try:
                client = Groq(api_key=api_key)
                models = [auto_option]
                
                priority_keywords = config.get("groq_priority_keywords", ["llama-3.3", "llama-3.1", "llama3", "mixtral"])
                
                def get_priority(model_name):
                    model_name_lower = model_name.lower()
                    for i, keyword in enumerate(priority_keywords):
                        if keyword in model_name_lower:
                            return i
                    return 999
                
                fetched_models = []
                for m in client.models.list().data:
                    # Filter model audio (whisper) agar tidak bisa dipilih
                    is_supported = "whisper" not in m.id.lower()
                    
                    display_name = m.id
                    if not is_supported:
                        display_name += " (Hanya Audio - Tidak Didukung)"
                        
                    fetched_models.append({
                        "name": m.id,
                        "display_name": display_name,
                        "is_supported": is_supported
                    })
                
                # Urutkan: prioritas keyword > didukung > abjad
                fetched_models.sort(key=lambda x: (
                    get_priority(x["name"]),
                    not x["is_supported"],
                    x["name"]
                ))
                
                models.extend(fetched_models)
                return models
            except Exception:
                return [auto_option]
        return [auto_option]
