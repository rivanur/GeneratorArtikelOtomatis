from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Konfigurasi Koneksi MySQL Laragon
# Format: mysql+pymysql://<username>:<password>@<host>:<port>/<database>
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/letterwrap"

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
