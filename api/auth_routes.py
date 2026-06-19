from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from core.database import get_db
from core.models import User
from core.auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

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
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Cek apakah email sudah terdaftar
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email sudah terdaftar. Silakan gunakan email lain atau masuk."
        )
    
    # Enkripsi password dan simpan user baru
    hashed_password = get_password_hash(user.password)
    new_user = User(name=user.name, email=user.email, hashed_password=hashed_password)
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"status": "success", "message": "Pendaftaran berhasil!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Gagal mendaftar: {str(e)}")

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
