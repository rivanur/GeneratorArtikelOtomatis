import json
import os

SETTINGS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "settings.json")

class SettingsManager:
    @staticmethod
    def _ensure_file_exists():
        if not os.path.exists(SETTINGS_FILE):
            default_settings = {
                "api_key": "",
                "ai_model": "gemini-2.5-flash",
                "wp_url": "",
                "wp_username": "",
                "wp_app_password": ""
            }
            os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(default_settings, f, indent=4)

    @staticmethod
    def get_settings() -> dict:
        SettingsManager._ensure_file_exists()
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    @staticmethod
    def save_settings(new_settings: dict) -> bool:
        SettingsManager._ensure_file_exists()
        try:
            current_settings = SettingsManager.get_settings()
            current_settings.update(new_settings)
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(current_settings, f, indent=4)
            return True
        except Exception:
            return False

    @staticmethod
    def get_api_key() -> str:
        return SettingsManager.get_settings().get("api_key", "")
