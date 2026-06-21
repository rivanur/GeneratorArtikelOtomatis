from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

# Konfigurasi Koneksi MySQL Laragon atau Cloud (Northflank)
# Mengambil dari Environment Variable "DATABASE_URL" jika sedang di server
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://root:@localhost:3306/letterwrap"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=3600 # Menjaga koneksi tetap hidup
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency untuk FastAPI agar setiap request dapat session database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
