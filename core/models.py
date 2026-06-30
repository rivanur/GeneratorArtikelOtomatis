from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    profile_picture = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(255), nullable=True)

    settings = relationship("UserSettings", back_populates="user", uselist=False)

class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True)
    
    # AI Settings
    ai_provider = Column(String(50), default="gemini")
    ai_model = Column(String(100), default="auto")
    encrypted_gemini_key = Column(Text, nullable=True)
    
    hf_model = Column(String(100), default="auto")
    encrypted_hf_key = Column(Text, nullable=True)
    
    groq_model = Column(String(100), default="auto")
    encrypted_groq_key = Column(Text, nullable=True)
    
    # WordPress Settings
    wp_url = Column(String(255), nullable=True)
    wp_username = Column(String(100), nullable=True)
    encrypted_wp_password = Column(Text, nullable=True)

    user = relationship("User", back_populates="settings")
