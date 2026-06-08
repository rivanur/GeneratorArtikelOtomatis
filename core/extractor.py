import PyPDF2
from bs4 import BeautifulSoup
import requests
import io
import re

class ContentExtractor:
    @staticmethod
    def extract_from_url(url: str) -> str:
        """Ekstrak teks dari URL web"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Hapus tag script dan style
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.extract()
                
            text = soup.get_text()
            # Bersihkan spasi kosong berlebih
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            return text
            
        except Exception as e:
            raise Exception(f"Gagal mengekstrak teks dari URL: {str(e)}")

    @staticmethod
    def extract_from_pdf(file_bytes: bytes) -> str:
        """Ekstrak teks dari bytes PDF"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Gagal membaca PDF: {str(e)}")

    @staticmethod
    def extract_youtube_info(url: str) -> str:
        """
        Versi dummy untuk prototipe jurnal.
        Pada sistem asli, ini akan mengunduh audio dan menjalankan Speech-to-Text.
        """
        # Ekstrak ID video
        video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        video_id = video_id_match.group(1) if video_id_match else "unknown"
        
        return f"[Transkrip Simulasi untuk Video YouTube ID: {video_id}]\nIni adalah simulasi teks hasil ekstraksi audio (Speech-to-Text) dari video YouTube {url}. Di lingkungan produksi, teks ini berasal dari FFmpeg dan model STT seperti Whisper."

    @staticmethod
    def extract_local_video_info(filename: str) -> str:
        """
        Versi dummy untuk prototipe jurnal.
        """
        return f"[Transkrip Simulasi untuk Video Lokal: {filename}]\nIni adalah simulasi teks hasil ekstraksi audio dari file video lokal. Di lingkungan produksi, audio diekstrak menggunakan FFmpeg dan diproses dengan STT."
