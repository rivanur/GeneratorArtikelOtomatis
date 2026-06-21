from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

# Konfigurasi Koneksi MySQL Laragon atau Cloud (Northflank)
# Mengambil dari Environment Variable "DATABASE_URL" atau "MYSQL_URI" (injeksi otomatis Northflank)
raw_db_url = os.getenv("DATABASE_URL") or os.getenv("MYSQL_URI") or "mysql+pymysql://root:@localhost:3306/letterwrap"

# Jika Northflank menyuntikkan mysql:// standar, kita ubah ke mysql+pymysql:// agar dikenali SQLAlchemy
if raw_db_url.startswith("mysql://"):
    raw_db_url = raw_db_url.replace("mysql://", "mysql+pymysql://", 1)

SQLALCHEMY_DATABASE_URL = raw_db_url

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
