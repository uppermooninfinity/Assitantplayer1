import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    STRING_SESSION = os.getenv("STRING_SESSION", "")

    LOGGER_GROUP_ID = int(os.getenv("LOGGER_GROUP_ID", "0"))

    MONGODB_URI = os.getenv("MONGODB_URI", "")

    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
    YOUTUBE_COOKIES_PATH = os.getenv("YOUTUBE_COOKIES_PATH", "cookies.txt")

    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")

    OWNER_ID = int(os.getenv("OWNER_ID", "0"))

    MUSIC_CACHE_DIR = "cache/music"
    VOICE_CACHE_DIR = "cache/voice"

config = Config()
