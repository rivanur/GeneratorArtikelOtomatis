import requests
import base64
import re

class WordPressPublisher:
    def __init__(self, wp_url: str, username: str, app_password: str):
        self.wp_url = wp_url.rstrip('/')
        self.username = username
        self.app_password = app_password

    def _get_auth_header(self):
        credentials = f"{self.username}:{self.app_password}"
        token = base64.b64encode(credentials.encode()).decode('utf-8')
        return {"Authorization": f"Basic {token}"}

    def _markdown_to_html(self, markdown_text: str) -> str:
        """
        Konversi markdown ke HTML menggunakan library yang stabil untuk WordPress.
        Juga menghapus Judul (H1) pertama agar tidak bentrok (double) dengan Judul Pos bawaan WordPress.
        """
        try:
            from markdown_it import MarkdownIt
        except ImportError:
            raise Exception("Library markdown-it-py tidak ditemukan. Harap pastikan sudah terinstall.")

        # 1. Hapus Judul H1 Pertama (Karena sudah diisi ke field 'title' di WP)
        lines = markdown_text.split('\n')
        if lines and lines[0].startswith('# '):
            lines = lines[1:]  # Buang baris pertama (Judul)
        
        cleaned_markdown = '\n'.join(lines).strip()

        # 2. Konversi sisa Markdown ke HTML yang sempurna
        md = MarkdownIt()
        html = md.render(cleaned_markdown)
        
        # 3. Batasi ukuran gambar agar rapi di WordPress
        html = html.replace('<img ', '<img style="max-width: 100%; height: auto; border-radius: 8px; display: block; margin: 0 auto;" ')
        
        return html

    def publish_article(self, title: str, markdown_content: str, status: str = "draft") -> dict:
        """Publikasikan artikel ke WordPress REST API"""
        if not self.wp_url or not self.username or not self.app_password:
            return {"success": False, "error": "Kredensial WordPress belum diatur di Pengaturan."}

        api_url = f"{self.wp_url}/wp-json/wp/v2/posts"
        html_content = self._markdown_to_html(markdown_content)

        data = {
            "title": title,
            "content": html_content,
            "status": status,
            "comment_status": "closed"
        }

        try:
            response = requests.post(
                api_url,
                headers=self._get_auth_header(),
                json=data,
                timeout=15
            )
            
            if response.status_code in [200, 201]:
                return {"success": True, "data": response.json()}
            else:
                return {
                    "success": False, 
                    "error": f"Gagal mempublikasikan: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
