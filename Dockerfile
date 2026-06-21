# Menggunakan base image Python 3.11 yang ringan
FROM python:3.11-slim

# Mengatur environment variables untuk Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Mengatur working directory di dalam container
WORKDIR /app

# Menginstal dependensi sistem yang mungkin diperlukan oleh beberapa library
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev-compat \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Menyalin file requirements.txt
COPY requirements.txt .

# Menginstal paket Python
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh kode proyek ke dalam container
COPY . .

# Membuat folder data/uploads jika belum ada
RUN mkdir -p data/uploads

# Mengekspos port yang akan digunakan oleh FastAPI
EXPOSE 8000

# Perintah untuk menjalankan server menggunakan Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
