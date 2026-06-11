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
        api_key = SettingsManager.get_api_key()
        settings = SettingsManager.get_settings()
        ai_model = settings.get("ai_model", "gemini-2.5-flash")
        
        if not api_key:
            raise HTTPException(status_code=400, detail="Gemini API Key belum diatur. Silakan buka menu Pengaturan ⚙️.")
            
        generator = AIGenerator(api_key=api_key, model_name=ai_model)
        
        # 2. Ekstraksi & Parsing Teks Otomatis
        extracted_text = ""
        media_path = None
        temp_dir = os.path.join(os.path.dirname(__file__), "..", "data", "temp")
        os.makedirs(temp_dir, exist_ok=True)
        
        if source_type == "manual_text":
            if not manual_text:
                raise HTTPException(status_code=400, detail="Teks manual tidak boleh kosong")
            extracted_text = manual_text
            
        elif source_type == "web_url":
            if not url:
                raise HTTPException(status_code=400, detail="URL Web tidak boleh kosong")
            extracted_text = ContentExtractor.extract_from_url(url)
            
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
            except subprocess.CalledProcessError as e:
                raise HTTPException(status_code=400, detail=f"Gagal mengunduh audio YouTube: {e.stderr.decode('utf-8', errors='ignore')}")
            
        elif source_type == "document":
            if not file:
                raise HTTPException(status_code=400, detail="File dokumen tidak dilampirkan")
            content = await file.read()
            if file.filename.endswith(".pdf"):
                extracted_text = ContentExtractor.extract_from_pdf(content)
            else:
                extracted_text = content.decode('utf-8', errors='ignore')
                
        elif source_type == "local_video":
            if not file:
                raise HTTPException(status_code=400, detail="File video lokal tidak dilampirkan")
            # Simpan file sementara untuk diproses Gemini
            ext = os.path.splitext(file.filename)[1] or '.mp4'
            temp_filepath = os.path.join(temp_dir, f"{uuid.uuid4()}{ext}")
            
            async with aiofiles.open(temp_filepath, 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)
                
            media_path = temp_filepath
            extracted_text = f"Tolong tonton video terlampir dan buatkan artikel berdasarkan kontennya. Nama file asli: {file.filename}"
            
        else:
            raise HTTPException(status_code=400, detail="Tipe sumber tidak valid")

        # 3. Kompilasi & Pengiriman ke LLM
        if not extracted_text and not media_path:
            raise HTTPException(status_code=400, detail="Gagal mengekstrak teks atau media dari sumber")

        result_data = generator.generate_article(source_context=extracted_text, style=style, media_path=media_path)

        # Bersihkan file temp lokal
        if media_path and os.path.exists(media_path):
            try:
                os.remove(media_path)
            except:
                pass

        return {
            "status": "success",
            "data": result_data["text"],
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
async def publish_to_wordpress(title: str = Form(...), content: str = Form(...)):
    settings = SettingsManager.get_settings()
    wp_url = settings.get("wp_url")
    username = settings.get("wp_username")
    app_pwd = settings.get("wp_app_password")
    
    if not wp_url or not username or not app_pwd:
        raise HTTPException(status_code=400, detail="Kredensial WordPress belum diisi. Silakan cek menu Pengaturan ⚙️.")
        
    publisher = WordPressPublisher(wp_url, username, app_pwd)
    result = publisher.publish_article(title=title, markdown_content=content, status="draft")
    
    if result.get("success"):
        return {"status": "success", "message": "Artikel berhasil di-draft di WordPress!"}
    else:
        raise HTTPException(status_code=500, detail=result.get("error"))

@router.post("/test-key")
async def test_api_key(payload: dict = Body(...)):
    api_key = payload.get("api_key")
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key kosong")
    
    is_valid = AIGenerator.test_api_key(api_key)
    if is_valid:
        return {"status": "success", "message": "Koneksi API Key Berhasil!"}
    raise HTTPException(status_code=400, detail="API Key Tidak Valid atau Kuota Habis")

@router.post("/models")
async def get_models(payload: dict = Body(...)):
    api_key = payload.get("api_key")
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key kosong")
        
    models = AIGenerator.get_available_models(api_key)
    return {"status": "success", "models": models}
