import PyPDF2
from bs4 import BeautifulSoup
import requests
import io
import docx

class ContentExtractor:
    @staticmethod
    def extract_image_from_url(url: str) -> str:
        """Ekstrak URL gambar utama dari web (og:image)"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Coba cari og:image
            og_image = soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                return og_image['content']
                
            # Coba cari twitter:image
            twitter_image = soup.find('meta', property='twitter:image')
            if twitter_image and twitter_image.get('content'):
                return twitter_image['content']
                
            # Fallback ke img pertama yang masuk akal
            for img in soup.find_all('img'):
                src = img.get('src')
                if src and ('http' in src) and not any(x in src.lower() for x in ['logo', 'icon', 'avatar']):
                    return src
        except:
            pass
        return None

    @staticmethod
    def extract_from_url(url: str) -> str:
        """Ekstrak teks dari URL web dengan sistem Multi-Layer Fallback"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        
        try:
            # Layer 1: Identifikasi Tipe Konten (Cek PDF)
            try:
                head_resp = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
                content_type = head_resp.headers.get('Content-Type', '').lower()
                
                if 'application/pdf' in content_type:
                    # Jika URL adalah PDF, unduh file dan gunakan extract_from_pdf
                    pdf_resp = requests.get(url, headers=headers, timeout=30)
                    pdf_resp.raise_for_status()
                    text = ContentExtractor.extract_from_pdf(pdf_resp.content)
                    if text and len(text) > 50:
                        return text
            except Exception as e:
                pass # Lanjut ke metode biasa jika pengecekan gagal

            # Layer 2: Jina Reader API (Primary Scraper)
            text = ""
            try:
                jina_headers = headers.copy()
                jina_headers['Accept'] = 'text/plain'
                jina_url = f"https://r.jina.ai/{url}"
                jina_resp = requests.get(jina_url, headers=jina_headers, timeout=25)
                jina_resp.raise_for_status()
                text = jina_resp.text
            except Exception as e:
                print(f"Jina API gagal: {str(e)}. Beralih ke Fallback.")

            # Layer 3: BeautifulSoup Fallback (Secondary Scraper)
            if not text or len(text.strip()) < 50:
                try:
                    bs_resp = requests.get(url, headers=headers, timeout=15)
                    bs_resp.raise_for_status()
                    soup = BeautifulSoup(bs_resp.text, 'html.parser')
                    
                    # Hapus tag script dan style
                    for script in soup(["script", "style", "nav", "footer", "header"]):
                        script.extract()
                        
                    raw_text = soup.get_text()
                    lines = (line.strip() for line in raw_text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = '\n'.join(chunk for chunk in chunks if chunk)
                except Exception as e:
                    print(f"BeautifulSoup Fallback gagal: {str(e)}")

            # Layer 4: Validasi Konten Akhir
            if not text or len(text.strip()) < 50:
                raise Exception("Konten terlalu pendek, kosong, atau URL dilindungi dengan sangat ketat (CAPTCHA/Paywall).")

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
    def extract_from_docx(file_bytes: bytes) -> str:
        """Ekstrak teks dari bytes DOCX"""
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            text = []
            for para in doc.paragraphs:
                if para.text.strip():
                    text.append(para.text.strip())
            return "\n\n".join(text)
        except Exception as e:
            raise Exception(f"Gagal membaca file Word: {str(e)}")
