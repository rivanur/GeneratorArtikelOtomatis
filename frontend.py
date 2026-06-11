import os
import http.server
import socketserver

PORT = 5500
DIRECTORY = "frontend"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    if not os.path.exists(DIRECTORY):
        print(f"Error: Folder '{DIRECTORY}' tidak ditemukan!")
        return

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"===================================================")
        print(f"   MEMULAI SERVER FRONTEND (ANTARMUKA WEB)")
        print(f"===================================================")
        print(f"\nFrontend berjalan di: http://localhost:{PORT}")
        print(f"Tekan CTRL+C untuk mematikan.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nMematikan server frontend...")

if __name__ == "__main__":
    start_server()
