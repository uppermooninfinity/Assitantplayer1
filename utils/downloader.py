import os
import logging
import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
from config import config
import re

logger = logging.getLogger(__name__)

os.makedirs(config.MUSIC_CACHE_DIR, exist_ok=True)

spotify_client = None
if config.SPOTIFY_CLIENT_ID and config.SPOTIFY_CLIENT_SECRET:
    try:
        spotify_client = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=config.SPOTIFY_CLIENT_ID,
                client_secret=config.SPOTIFY_CLIENT_SECRET
            )
        )
    except Exception as e:
        logger.error(f"Failed to initialize Spotify client: {e}")

async def search_song(query: str):
    try:
        if "spotify.com" in query:
            return await search_spotify(query)

        elif "youtube.com" in query or "youtu.be" in query:
            return {
                "title": "YouTube Video",
                "url": query,
                "platform": "YouTube",
                "duration": "Unknown"
            }

        else:
            videos_search = VideosSearch(query, limit=1)
            result = videos_search.result()

            if result and result['result']:
                video = result['result'][0]
                return {
                    "title": video['title'],
                    "url": video['link'],
                    "platform": "YouTube",
                    "duration": video.get('duration', 'Unknown'),
                    "thumbnail": video.get('thumbnails', [{}])[0].get('url', '')
                }

        return None

    except Exception as e:
        logger.error(f"Error searching song: {e}")
        return None

async def search_spotify(spotify_url: str):
    try:
        if not spotify_client:
            logger.error("Spotify client not initialized")
            return None

        track_id = re.search(r'track/([a-zA-Z0-9]+)', spotify_url)
        if track_id:
            track = spotify_client.track(track_id.group(1))
            query = f"{track['name']} {track['artists'][0]['name']}"

            videos_search = VideosSearch(query, limit=1)
            result = videos_search.result()

            if result and result['result']:
                video = result['result'][0]
                return {
                    "title": f"{track['name']} - {track['artists'][0]['name']}",
                    "url": video['link'],
                    "platform": "Spotify",
                    "duration": f"{track['duration_ms'] // 60000}:{(track['duration_ms'] // 1000) % 60:02d}"
                }

        return None

    except Exception as e:
        logger.error(f"Error searching Spotify: {e}")
        return None

async def download_song(url: str):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{config.MUSIC_CACHE_DIR}/%(id)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        if config.YOUTUBE_COOKIES_PATH and os.path.exists(config.YOUTUBE_COOKIES_PATH):
            ydl_opts['cookiefile'] = config.YOUTUBE_COOKIES_PATH

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_id = info['id']
            audio_file = f"{config.MUSIC_CACHE_DIR}/{video_id}.mp3"

            if os.path.exists(audio_file):
                return audio_file

            for ext in ['m4a', 'webm', 'opus']:
                alt_file = f"{config.MUSIC_CACHE_DIR}/{video_id}.{ext}"
                if os.path.exists(alt_file):
                    return alt_file

        return None

    except Exception as e:
        logger.error(f"Error downloading song: {e}")
        return None
