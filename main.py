import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.routes import router

app = FastAPI(title="Generator Artikel Otomatis", description="Standalone Article Writer System")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Konfigurasi CORS agar frontend terpisah bisa mengakses API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Mengizinkan semua origin untuk development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    print("Memulai server di http://localhost:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
