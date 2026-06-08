from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from typing import Optional
from core.extractor import ContentExtractor
from core.ai_generator import AIGenerator

router = APIRouter()

@router.post("/generate")
async def generate_article(
    api_key: str = Form(...),
    source_type: str = Form(...), # manual_text, web_url, youtube_url, document, local_video
    style: str = Form("blog"),
    manual_text: Optional[str] = Form(None),
    url: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    try:
        # 1. Pilih & Konfigurasi API LLM
        generator = AIGenerator(api_key=api_key)
        
        # 2. Ekstraksi & Parsing Teks Otomatis
        extracted_text = ""
        
        if source_type == "manual_text":
            if not manual_text:
                raise HTTPException(status_code=400, detail="Teks manual tidak boleh kosong")
            extracted_text = f"Teks Manual: {manual_text}"
            
        elif source_type == "web_url":
            if not url:
                raise HTTPException(status_code=400, detail="URL Web tidak boleh kosong")
            extracted_text = ContentExtractor.extract_from_url(url)
            
        elif source_type == "youtube_url":
            if not url:
                raise HTTPException(status_code=400, detail="URL YouTube tidak boleh kosong")
            extracted_text = ContentExtractor.extract_youtube_info(url)
            
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
            extracted_text = ContentExtractor.extract_local_video_info(file.filename)
            
        else:
            raise HTTPException(status_code=400, detail="Tipe sumber tidak valid")

        # 3. Kompilasi & Pengiriman ke LLM
        if not extracted_text:
            raise HTTPException(status_code=400, detail="Gagal mengekstrak teks dari sumber")

        result_markdown = generator.generate_article(source_context=extracted_text, style=style)

        return {
            "status": "success",
            "data": result_markdown
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
