import os
from cryptography.fernet import Fernet

# Simpan master key di folder data agar aman dan di-ignore oleh Git
KEY_FILE = os.path.join(os.path.dirname(__file__), "..", "data", ".encryption_key")

def get_or_create_key():
    env_key = os.getenv("ENCRYPTION_KEY")
    if env_key:
        return env_key.encode('utf-8')

    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key
    else:
        with open(KEY_FILE, "rb") as f:
            return f.read()

class CryptoManager:
    _key = get_or_create_key()
    _fernet = Fernet(_key)

    @staticmethod
    def encrypt(data: str) -> str:
        if not data:
            return ""
        return CryptoManager._fernet.encrypt(data.encode('utf-8')).decode('utf-8')

    @staticmethod
    def decrypt(encrypted_data: str) -> str:
        if not encrypted_data:
            return ""
        try:
            return CryptoManager._fernet.decrypt(encrypted_data.encode('utf-8')).decode('utf-8')
        except Exception:
            return ""
