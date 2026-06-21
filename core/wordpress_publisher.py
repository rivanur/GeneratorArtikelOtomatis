import requests
import base64
import re

class WordPressPublisher:
    def __init__(self, wp_url: str, username: str, app_password: str):
        self.wp_url = wp_url.rstrip('/')
        self.username = username
        self.app_password = app_password

    def _get_auth_header(self):
        clean_pwd = self.app_password.replace(" ", "").strip()
        credentials = f"{self.username}:{clean_pwd}"
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

    def _upload_media(self, local_file_path: str) -> str:
        """
        Uploads a local image file to WordPress Media Library.
        Returns the remote URL if successful, otherwise None.
        """
        import mimetypes
        import os

        if not os.path.exists(local_file_path):
            print(f"File tidak ditemukan: {local_file_path}")
            return None

        media_url = f"{self.wp_url}/wp-json/wp/v2/media"
        mime_type, _ = mimetypes.guess_type(local_file_path)
        if not mime_type:
            mime_type = "image/jpeg"

        file_name = os.path.basename(local_file_path)
        
        headers = self._get_auth_header()
        headers["Content-Disposition"] = f'attachment; filename="{file_name}"'
        headers["Content-Type"] = mime_type

        try:
            with open(local_file_path, "rb") as f:
                response = requests.post(media_url, headers=headers, data=f, timeout=30)
                
            if response.status_code in [200, 201]:
                return response.json().get("source_url")
            else:
                print(f"Gagal upload media: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Exception saat upload media: {e}")
            return None

    def publish_article(self, title: str, markdown_content: str, status: str = "draft") -> dict:
        """Publikasikan artikel ke WordPress REST API"""
        import os
        import re

        if not self.wp_url or not self.username or not self.app_password:
            return {"success": False, "error": "Kredensial WordPress belum diatur di Pengaturan."}

        # 1. Pindai tautan localhost dan unggah ke WordPress
        local_image_matches = re.finditer(r'!\[.*?\]\((.*?/api/uploads/([^)]+))\)', markdown_content)
        images_to_delete = []
        
        for match in local_image_matches:
            full_url = match.group(1)
            filename = match.group(2)
            # Asumsikan path data/uploads/
            local_path = os.path.abspath(os.path.join("data", "uploads", filename))
            
            if os.path.exists(local_path):
                # Upload ke WP
                wp_url = self._upload_media(local_path)
                if wp_url:
                    # Ganti tautan di Markdown
                    markdown_content = markdown_content.replace(full_url, wp_url)
                    images_to_delete.append(local_path)

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
                # Operasi Sapu Bersih (Auto-Cleanup)
                for path in images_to_delete:
                    try:
                        os.remove(path)
                    except Exception as e:
                        print(f"Gagal menghapus file sisa: {e}")
                
                return {"success": True, "data": response.json()}
            else:
                return {
                    "success": False, 
                    "error": f"Gagal mempublikasikan: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
