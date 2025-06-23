from dotenv import load_dotenv
import os


load_dotenv()


API_KEYS = os.getenv("GEMINI_API_KEYS", "").split(",")

class GeminiKeyManager:
    def __init__(self, keys):
        self.keys = [k.strip() for k in keys if k.strip()]
        self.current_index = 0

    def get_key(self):
        return self.keys[self.current_index]

    def rotate_key(self):
        self.current_index = (self.current_index + 1) % len(self.keys)
        print(f"[INFO] Rotated to API key #{self.current_index + 1}")
