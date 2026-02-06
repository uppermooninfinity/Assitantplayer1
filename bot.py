import asyncio
import logging
import os
from datetime import datetime

from pyrogram import Client

from config import config
from database.mongodb import db
from handlers import commands, voice_chat, music
from utils.logger import send_startup_log
from utils.generate_silence import generate_silence_file


# ─── LOGGING ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ─── BOT CLASS ────────────────────────────────────────────
class MusicBot:
    def __init__(self):
        self.bot = Client(
            name="music_bot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            workers=50
        )

        self.assistant = Client(
            name="assistant",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=config.STRING_SESSION,
            workers=50
        )

        self.start_time = datetime.now()

    async def start(self):
        try:
            # directories
            os.makedirs(config.MUSIC_CACHE_DIR, exist_ok=True)
            os.makedirs(config.VOICE_CACHE_DIR, exist_ok=True)

            logger.info("Generating silence audio file...")
            generate_silence_file()

            logger.info("Connecting to database...")
            await db.connect()

            logger.info("Starting bot client...")
            await self.bot.start()

            logger.info("Starting assistant client...")
            await self.assistant.start()

            # register handlers AFTER clients are started
            commands.setup_handlers(self.bot, self.assistant)
            voice_chat.setup_handlers(self.bot, self.assistant)
            music.setup_handlers(self.bot, self.assistant)

            bot_info = await self.bot.get_me()
            assistant_info = await self.assistant.get_me()

            await send_startup_log(
                self.bot,
                bot_info,
                assistant_info,
                self.start_time
            )

            logger.info(f"Bot started as @{bot_info.username}")
            logger.info(f"Assistant started as @{assistant_info.username}")
            logger.info("Bot is now running and listening for commands")

            # keep alive
            await asyncio.Event().wait()

        except Exception as e:
            logger.exception("Failed to start bot")
            raise e

    async def stop(self):
        logger.info("Stopping bot...")
        await self.bot.stop()
        await self.assistant.stop()
        await db.close()
        logger.info("Bot stopped cleanly")


# ─── ENTRY POINT ──────────────────────────────────────────
if __name__ == "__main__":
    music_bot = MusicBot()

    try:
        asyncio.run(music_bot.start())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
