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
        Konversi basic markdown ke HTML untuk dipublish.
        (Di produksi nyata, bisa gunakan library Python-Markdown, 
        tapi kita gunakan Regex sederhana untuk prototipe ini)
        """
        html = markdown_text
        
        # Headers
        html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # Bold and Italic
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        
        # Paragraphs (simple split by double newline)
        paragraphs = html.split('\n\n')
        html = ""
        for p in paragraphs:
            if not p.strip().startswith('<h'):
                html += f"<p>{p.strip().replace(chr(10), '<br>')}</p>\n"
            else:
                html += f"{p.strip()}\n"
                
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
