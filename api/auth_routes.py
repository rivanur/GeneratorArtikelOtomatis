from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Request, BackgroundTasks
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from core.database import get_db
from core.models import User
from core.auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from datetime import timedelta, datetime
import os
import aiofiles
import uuid
import secrets
from core.email_service import send_verification_email

router = APIRouter()

# Schema Pydantic untuk validasi input
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
def register_user(request: Request, user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Cek apakah email sudah terdaftar
    db_user = db.query(User).filter(User.email == user.email).first()
    
    verification_token = secrets.token_urlsafe(32)
    hashed_password = get_password_hash(user.password)
    
    if db_user:
        if db_user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email sudah terdaftar. Silakan gunakan email lain atau masuk."
            )
        else:
            # Belum diverifikasi, cek apakah token masih aktif
            if db_user.verification_expires and db_user.verification_expires > datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email sedang dalam proses verifikasi. Silakan cek inbox Anda, atau tunggu 15 menit untuk mendaftar ulang."
                )
            else:
                # Token sudah kedaluwarsa, timpa (overwrite) data lama
                db_user.name = user.name
                db_user.hashed_password = hashed_password
                db_user.verification_token = verification_token
                db_user.verification_expires = datetime.utcnow() + timedelta(minutes=15)
                
                new_user = db_user # Re-use existing row
    else:
        # Akun benar-benar baru
        new_user = User(
            name=user.name, 
            email=user.email, 
            hashed_password=hashed_password,
            is_verified=False,
            verification_token=verification_token,
            verification_expires=datetime.utcnow() + timedelta(minutes=15)
        )
        db.add(new_user)
        
    try:
        db.commit()
        db.refresh(new_user)
        
        # Kirim email verifikasi di latar belakang agar response instan
        request_url_base = str(request.base_url).rstrip('/')
        background_tasks.add_task(send_verification_email, user.email, verification_token, request_url_base)
        
        return {"status": "success", "message": "Pendaftaran berhasil! Silakan periksa email Anda untuk verifikasi."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Gagal mendaftar: {str(e)}")

@router.get("/verify")
def verify_email(request: Request, token: str, db: Session = Depends(get_db)):
    # Tentukan base URL frontend
    frontend_url = os.getenv("FRONTEND_URL")
    if not frontend_url:
        host = request.url.hostname
        if host in ("localhost", "127.0.0.1"):
            # Asumsi Live Server atau frontend.py
            frontend_url = "http://127.0.0.1:5500"
        else:
            frontend_url = os.getenv("FRONTEND_URL", "https://arsa-27v.pages.dev")
            
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        return RedirectResponse(url=f"{frontend_url}/login.html?verified=invalid")
        
    if user.verification_expires and user.verification_expires < datetime.utcnow():
        return RedirectResponse(url=f"{frontend_url}/login.html?verified=expired")
        
    user.is_verified = True
    user.verification_token = None
    user.verification_expires = None
    db.commit()
    
    return RedirectResponse(url=f"{frontend_url}/login.html?verified=success")

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    # Cari user berdasarkan email
    db_user = db.query(User).filter(User.email == user.email).first()
    
    # Validasi user dan password
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Validasi status verifikasi email
    if not db_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email belum diverifikasi. Silakan periksa kotak masuk/spam email Anda.",
        )
    
    # Buat JWT Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email, "name": db_user.name}, expires_delta=access_token_expires
    )
    
    return {
        "status": "success",
        "access_token": access_token,
        "token_type": "bearer",
        "user_name": db_user.name
    }

@router.get("/me")
def get_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "name": current_user.name,
        "email": current_user.email,
        "profile_picture": current_user.profile_picture
    }

@router.put("/profile")
def update_profile(name: str = Form(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.name = name
    db.commit()
    return {"status": "success", "message": "Profil berhasil diperbarui", "name": name}

@router.put("/change-password")
def change_password(
    old_password: str = Form(...), 
    new_password: str = Form(...), 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    if not verify_password(old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Password lama salah")
        
    current_user.hashed_password = get_password_hash(new_password)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return {"status": "success", "message": "Password berhasil diubah"}

@router.post("/avatar")
async def upload_avatar(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File harus berupa gambar")
        
    uploads_dir = os.path.join(os.path.dirname(__file__), "..", "data", "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Hapus avatar lama jika ada
    if current_user.profile_picture:
        old_path = os.path.join(os.path.dirname(__file__), "..", current_user.profile_picture.lstrip('/'))
        if os.path.exists(old_path):
            try:
                os.remove(old_path)
            except Exception:
                pass
                
    ext = os.path.splitext(file.filename)[1]
    filename = f"avatar_{current_user.id}_{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(uploads_dir, filename)
    
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
        
    avatar_url = f"/api/uploads/{filename}"
    current_user.profile_picture = avatar_url
    db.commit()
    
    return {"status": "success", "profile_picture": avatar_url}
