import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.routes import router

app = FastAPI(title="Generator Artikel Otomatis", description="Standalone Article Writer System")

# Konfigurasi CORS agar frontend terpisah bisa mengakses API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Mengizinkan semua origin untuk development
    allow_credentials=False, # HARUS False jika allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles

uploads_dir = os.path.join(os.path.dirname(__file__), "data", "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/api/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Include API Routers
app.include_router(router, prefix="/api")

# Setup Database & Auth Routes
from core.database import Base, engine
from api.auth_routes import router as auth_router

# Buat tabel database secara otomatis jika belum ada
Base.metadata.create_all(bind=engine)

# Injeksi otomatis kolom baru tanpa menghapus data lama
try:
    with engine.begin() as conn:
        from sqlalchemy import text
        conn.execute(text("ALTER TABLE users ADD COLUMN profile_picture VARCHAR(255) NULL"))
except Exception:
    pass

try:
    with engine.begin() as conn:
        from sqlalchemy import text
        conn.execute(text("ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT FALSE"))
        conn.execute(text("ALTER TABLE users ADD COLUMN verification_token VARCHAR(255) NULL"))
except Exception:
    pass

try:
    with engine.begin() as conn:
        from sqlalchemy import text
        conn.execute(text("ALTER TABLE users ADD COLUMN verification_expires DATETIME NULL"))
except Exception:
    pass

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])

if __name__ == "__main__":
    print("Memulai server di http://localhost:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
