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

    def generate_article(self, source_context: str, style: str = "blog", custom_prompt: str = "", media_path: str = None) -> dict:
        """
        Kompilasi prompt terstruktur dan kirim ke API LLM (Gemini atau Hugging Face)
        Bisa menerima teks (source_context) atau file media (media_path)
        """
        if not self.api_key:
            return "**Error:** API Key tidak disetel atau tidak valid."
        
        if self.provider in ["huggingface", "groq"] and media_path:
            raise Exception(f"{self.provider.capitalize()} API saat ini tidak mendukung pemrosesan file media (Video/Audio) secara langsung. Harap gunakan Gemini untuk sumber media.")

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
        models_to_try = [self.model_name]
        
        if self.model_name == "auto" or not self.model_name:
            available_models = self.get_available_models(self.provider, self.api_key)
            valid_models = [m["name"] for m in available_models if m["name"] != "auto" and m.get("is_supported", True)]
            models_to_try = valid_models[:3]
            
            if not models_to_try:
                raise Exception(f"Tidak ada model cadangan yang tersedia untuk provider {self.provider.capitalize()}")

        last_error = None
        for i, current_model in enumerate(models_to_try):
            try:
                if self.model_name == "auto" or not self.model_name:
                    if self.provider == "gemini":
                        self.model = genai.GenerativeModel(current_model)
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
                    
                    content_parts.append(base_prompt)
                    response = self.model.generate_content(content_parts)
                    generated_text = response.text
                    token_count = response.usage_metadata.total_token_count
                    
                elif self.provider == "huggingface":
                    try:
                        messages = [{"role": "user", "content": base_prompt}]
                        response = self.hf_client.chat_completion(messages=messages, max_tokens=2048)
                        generated_text = response.choices[0].message.content
                    except Exception as e:
                        error_str = str(e).lower()
                        if "not a chat model" in error_str or "model_not_supported" in error_str:
                            try:
                                formatted_prompt = f"[INST] {base_prompt} [/INST]"
                                generated_text = self.hf_client.text_generation(prompt=formatted_prompt, max_new_tokens=2048)
                            except Exception as inner_e:
                                raise Exception(f"Chat error: {str(e)} | Teks error: {str(inner_e)}")
                        else:
                            raise e
                    token_count = int(len(base_prompt.split()) * 1.3)
                    
                elif self.provider == "groq":
                    response = self.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": base_prompt}],
                        model=current_model,
                        max_tokens=2048
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
                print(f"Model {current_model} gagal: {last_error}. Mencoba model selanjutnya...")
                continue
                
        raise Exception(f"Gagal melakukan generasi artikel dengan {self.provider.capitalize()} setelah mencoba semua model cadangan. Error terakhir: {last_error}")

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
    def get_available_models(provider: str, api_key: str = "") -> list:
        provider = provider.lower()
        auto_option = {"name": "auto", "display_name": "✨ Otomatis (Rekomendasi Terbaik)", "is_supported": True}
        
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
            return [
                auto_option,
                {"name": "mistralai/Mistral-7B-Instruct-v0.3", "display_name": "Mistral 7B Instruct v0.3"},
                {"name": "mistralai/Mixtral-8x7B-Instruct-v0.1", "display_name": "Mixtral 8x7B Instruct"},
                {"name": "meta-llama/Meta-Llama-3-8B-Instruct", "display_name": "Llama 3 (8B Instruct)"},
                {"name": "Qwen/Qwen2-72B-Instruct", "display_name": "Qwen2 72B Instruct"},
                {"name": "google/gemma-1.1-7b-it", "display_name": "Gemma 1.1 7B IT"}
            ]
        elif provider == "groq":
            try:
                client = Groq(api_key=api_key)
                models = [auto_option]
                for m in client.models.list().data:
                    # Filter model audio (whisper) agar tidak bisa dipilih
                    is_supported = "whisper" not in m.id.lower()
                    
                    display_name = m.id
                    if not is_supported:
                        display_name += " (Hanya Audio - Tidak Didukung)"
                        
                    models.append({
                        "name": m.id,
                        "display_name": display_name,
                        "is_supported": is_supported
                    })
                
                # Urutkan: auto selalu di atas, lalu yang didukung, lalu abjad
                models.sort(key=lambda x: (x["name"] != "auto", not x["is_supported"], x["name"]))
                return models
            except Exception:
                return [auto_option]
        return [auto_option]
