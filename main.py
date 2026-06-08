import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
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

# Include API Router
app.include_router(router, prefix="/api")

# Mount frontend static files
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
if not os.path.exists(frontend_dir):
    os.makedirs(frontend_dir)
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

if __name__ == "__main__":
    print("Memulai server di http://localhost:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
