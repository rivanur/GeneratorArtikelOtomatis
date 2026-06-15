from fastapi import APIRouter, Form, UploadFile, File, HTTPException, Body
from typing import Optional
from core.extractor import ContentExtractor
from core.ai_generator import AIGenerator
from core.settings_manager import SettingsManager
from core.wordpress_publisher import WordPressPublisher
import os
import aiofiles
import uuid
import subprocess

router = APIRouter()

@router.post("/generate")
async def generate_article(
    source_type: str = Form(...), # manual_text, web_url, youtube_url, document, local_video
    style: str = Form("blog"),
    manual_text: Optional[str] = Form(None),
    url: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    try:
        # 1. Pilih & Konfigurasi API LLM
        settings = SettingsManager.get_settings()
        ai_provider = settings.get("ai_provider", "gemini")
        
        if ai_provider == "gemini":
            api_key = settings.get("api_key", "")
            ai_model = settings.get("ai_model", "auto")
        elif ai_provider == "huggingface":
            api_key = settings.get("hf_api_key", "")
            ai_model = settings.get("hf_model", "auto")
        elif ai_provider == "groq":
            api_key = settings.get("groq_api_key", "")
            ai_model = settings.get("groq_model", "auto")
        else:
            raise HTTPException(status_code=400, detail="Provider AI tidak valid.")
            
        if not api_key:
            raise HTTPException(status_code=400, detail=f"{ai_provider.capitalize()} API Key belum diatur. Silakan buka menu Pengaturan ⚙️.")
            
        generator = AIGenerator(provider=ai_provider, api_key=api_key, model_name=ai_model)
        
        # 2. Ekstraksi & Parsing Teks Otomatis
        extracted_text = ""
        media_path = None
        extracted_image_url = None
        temp_dir = os.path.join(os.path.dirname(__file__), "..", "data", "temp")
        uploads_dir = os.path.join(os.path.dirname(__file__), "..", "data", "uploads")
        os.makedirs(temp_dir, exist_ok=True)
        os.makedirs(uploads_dir, exist_ok=True)
        
        if source_type == "manual_text":
            if not manual_text:
                raise HTTPException(status_code=400, detail="Teks manual tidak boleh kosong")
            extracted_text = manual_text
            
        elif source_type == "web_url":
            if not url:
                raise HTTPException(status_code=400, detail="URL Web tidak boleh kosong")
            extracted_text = ContentExtractor.extract_from_url(url)
            extracted_image_url = ContentExtractor.extract_image_from_url(url)
            
        elif source_type == "youtube_url":
            if not url:
                raise HTTPException(status_code=400, detail="URL YouTube tidak boleh kosong")
                
            temp_audio_path = os.path.join(temp_dir, f"{uuid.uuid4()}.m4a")
            try:
                # Unduh audio via yt-dlp
                subprocess.run(
                    [
                        "yt-dlp",
                        "-f", "bestaudio[ext=m4a]/bestaudio",
                        "--extract-audio",
                        "--audio-format", "m4a",
                        "-o", temp_audio_path,
                        url
                    ],
                    check=True,
                    capture_output=True
                )
                media_path = temp_audio_path
                extracted_text = f"Tolong dengarkan audio dari video YouTube terlampir dan buatkan artikel berdasarkan kontennya. URL asli: {url}"
                
                # Unduh URL thumbnail via yt-dlp
                try:
                    thumb_result = subprocess.run(
                        ["yt-dlp", "--get-thumbnail", url],
                        check=True, capture_output=True, text=True
                    )
                    if thumb_result.stdout:
                        extracted_image_url = thumb_result.stdout.strip()
                except:
                    pass
            except subprocess.CalledProcessError as e:
                raise HTTPException(status_code=400, detail=f"Gagal mengunduh audio YouTube: {e.stderr.decode('utf-8', errors='ignore')}")
            
        elif source_type == "document":
            if not file:
                raise HTTPException(status_code=400, detail="File dokumen tidak dilampirkan")
            content = await file.read()
            if file.filename.lower().endswith(".pdf"):
                extracted_text = ContentExtractor.extract_from_pdf(content)
            elif file.filename.lower().endswith(".docx"):
                extracted_text = ContentExtractor.extract_from_docx(content)
            elif file.filename.lower().endswith(".txt") or file.filename.lower().endswith(".md"):
                extracted_text = content.decode('utf-8', errors='ignore')
            else:
                raise HTTPException(status_code=400, detail="Format dokumen tidak didukung. Harap gunakan PDF, DOCX, TXT, atau MD.")
                
        elif source_type == "local_video":
            if not file:
                raise HTTPException(status_code=400, detail="File video lokal tidak dilampirkan")
            
            allowed_extensions = (".mp4", ".mov", ".avi", ".webm", ".mpeg", ".mpg", ".wmv", ".flv")
            ext = os.path.splitext(file.filename)[1].lower()
            if ext not in allowed_extensions:
                raise HTTPException(status_code=400, detail="Format video tidak didukung. Harap gunakan MP4, MOV, AVI, dll.")
            
            # Simpan file sementara untuk diproses Gemini dengan Streaming Chunk untuk hemat RAM
            temp_filepath = os.path.join(temp_dir, f"{uuid.uuid4()}{ext}")
            
            async with aiofiles.open(temp_filepath, 'wb') as out_file:
                while chunk := await file.read(1024 * 1024):  # Baca 1MB per iterasi
                    await out_file.write(chunk)
                
            media_path = temp_filepath
            extracted_text = f"Tolong tonton video terlampir dan buatkan artikel berdasarkan kontennya. Nama file asli: {file.filename}"
            
            # Ekstrak 1 frame sebagai gambar
            thumb_filename = f"{uuid.uuid4()}_thumb.jpg"
            thumb_path = os.path.join(uploads_dir, thumb_filename)
            try:
                subprocess.run(
                    ["ffmpeg", "-i", media_path, "-vframes", "1", "-ss", "00:00:03", "-y", thumb_path],
                    check=True, capture_output=True
                )
                if os.path.exists(thumb_path):
                    extracted_image_url = f"http://localhost:8000/api/uploads/{thumb_filename}"
            except:
                pass
            
        else:
            raise HTTPException(status_code=400, detail="Tipe sumber tidak valid")

        # 3. Kompilasi & Pengiriman ke LLM
        if not extracted_text and not media_path:
            raise HTTPException(status_code=400, detail="Gagal mengekstrak teks atau media dari sumber")

        result_data = generator.generate_article(
            source_context=extracted_text, 
            style=style, 
            media_path=media_path
        )

        final_text = result_data["text"]
        
        # 1. Pembersihan Regex: Hapus tag <think>...</think> (Sering digunakan oleh model DeepSeek di Groq/HuggingFace)
        import re
        final_text = re.sub(r'<think>.*?</think>', '', final_text, flags=re.DOTALL).strip()
        
        # 2. Pembersihan Isolasi: Hapus semua basa-basi AI sebelum Judul Utama (H1)
        # Karena kita sudah memerintahkan AI agar baris pertama WAJIB '# ', semua teks sebelum '# ' adalah sampah/gumaman.
        if '# ' in final_text:
            final_text = final_text[final_text.find('# '):]
            
        # 3. Fallback Gambar: Jika gambar gagal ditarik dari sumber, cari ilustrasi di DuckDuckGo!
        if not extracted_image_url:
            article_title = "Ilustrasi Artikel"
            for line in final_text.split('\n'):
                if line.startswith('# '):
                    article_title = line.replace('# ', '').strip()
                    # Bersihkan karakter aneh dari judul agar pencarian aman
                    article_title = re.sub(r'[^\w\s-]', '', article_title)
                    break
            
            try:
                from ddgs import DDGS
                print(f"Mencari gambar ilustrasi untuk: {article_title}")
                results = list(DDGS().images(article_title, max_results=1))
                if results and len(results) > 0:
                    extracted_image_url = results[0].get('image')
                    print(f"Gambar ditemukan: {extracted_image_url}")
            except Exception as e:
                print(f"Gagal mencari gambar ilustrasi: {e}")
            
        # 4. Injeksi Gambar Langsung (Bypass AI)
        if extracted_image_url:
            lines = final_text.split('\n')
            insert_index = 0
            for i, line in enumerate(lines):
                if line.startswith('# '):
                    insert_index = i + 1
                    break
            lines.insert(insert_index, f"\n![Gambar Utama]({extracted_image_url})\n")
            final_text = "\n".join(lines)

        # Bersihkan file temp lokal
        if media_path and os.path.exists(media_path):
            try:
                os.remove(media_path)
            except:
                pass

        return {
            "status": "success",
            "data": final_text,
            "tokens_used": result_data["tokens_used"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/settings")
async def get_settings():
    return SettingsManager.get_settings()

@router.post("/settings")
async def update_settings(settings: dict = Body(...)):
    success = SettingsManager.save_settings(settings)
    if success:
        return {"status": "success", "message": "Pengaturan berhasil disimpan"}
    raise HTTPException(status_code=500, detail="Gagal menyimpan pengaturan")

@router.post("/publish/wordpress")
async def publish_to_wordpress(title: str = Form(...), content: str = Form(...), status: str = Form("draft")):
    settings = SettingsManager.get_settings()
    wp_url = settings.get("wp_url")
    username = settings.get("wp_username")
    app_pwd = settings.get("wp_app_password")
    
    if not wp_url or not username or not app_pwd:
        raise HTTPException(status_code=400, detail="Kredensial WordPress belum diisi. Silakan cek menu Pengaturan ⚙️.")
        
    publisher = WordPressPublisher(wp_url, username, app_pwd)
    result = publisher.publish_article(title=title, markdown_content=content, status=status)
    
    if result.get("success"):
        status_msg = "di-publish (Live)" if status == "publish" else "disimpan sebagai draf"
        return {"status": "success", "message": f"Artikel berhasil {status_msg} di WordPress!"}
    else:
        raise HTTPException(status_code=500, detail=result.get("error"))

@router.post("/test-key")
async def test_api_key(payload: dict = Body(...)):
    api_key = payload.get("api_key")
    provider = payload.get("provider", "gemini")
    
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key kosong")
    
    is_valid = AIGenerator.test_api_key(provider, api_key)
    if is_valid:
        return {"status": "success", "message": "Koneksi API Key Berhasil!"}
    raise HTTPException(status_code=400, detail="API Key Tidak Valid atau Kuota Habis")

@router.post("/models")
async def get_models(payload: dict = Body(...)):
    api_key = payload.get("api_key")
    provider = payload.get("provider", "gemini")
    
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key kosong")
        
    models = AIGenerator.get_available_models(provider, api_key)
    return {"status": "success", "models": models}

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        uploads_dir = os.path.join(os.path.dirname(__file__), "..", "data", "uploads")
        os.makedirs(uploads_dir, exist_ok=True)
        
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
            raise HTTPException(status_code=400, detail="Format gambar tidak didukung")
            
        filename = f"{uuid.uuid4()}{ext}"
        filepath = os.path.join(uploads_dir, filename)
        
        async with aiofiles.open(filepath, 'wb') as out_file:
            while chunk := await file.read(1024 * 1024):
                await out_file.write(chunk)
                
        return {"status": "success", "image_url": f"/api/uploads/{filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from core.document_exporter import DocumentExporter
from fastapi.responses import FileResponse
from fastapi import BackgroundTasks

def remove_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

@router.post("/export/word")
async def export_word(background_tasks: BackgroundTasks, title: str = Form(...), content: str = Form(...)):
    try:
        filepath = DocumentExporter.export_to_word(title, content)
        if not os.path.exists(filepath):
            raise HTTPException(status_code=500, detail="Gagal membuat dokumen Word")
            
        background_tasks.add_task(remove_file, filepath)
        
        return FileResponse(
            path=filepath,
            filename=os.path.basename(filepath),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))