from motor.motor_asyncio import AsyncIOMotorClient
from config import config
import logging

logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(config.MONGODB_URI)
            self.db = self.client.telegram_music_bot
            await self.client.admin.command('ping')
            logger.info("Connected to MongoDB successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False

    async def close(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

    async def add_chat(self, chat_id, chat_title):
        await self.db.chats.update_one(
            {"chat_id": chat_id},
            {"$set": {"chat_title": chat_title, "active": True}},
            upsert=True
        )

    async def remove_chat(self, chat_id):
        await self.db.chats.update_one(
            {"chat_id": chat_id},
            {"$set": {"active": False}}
        )

    async def get_active_chats(self):
        cursor = self.db.chats.find({"active": True})
        return await cursor.to_list(length=None)

    async def increment_command_usage(self, command):
        await self.db.stats.update_one(
            {"type": "commands"},
            {"$inc": {f"commands.{command}": 1}},
            upsert=True
        )

    async def get_stats(self):
        stats = await self.db.stats.find_one({"type": "commands"})
        return stats.get("commands", {}) if stats else {}

    async def add_song_play(self, song_title, platform, chat_id):
        await self.db.plays.insert_one({
            "song_title": song_title,
            "platform": platform,
            "chat_id": chat_id,
            "timestamp": None
        })

    async def get_total_plays(self):
        return await self.db.plays.count_documents({})

db = MongoDB()
