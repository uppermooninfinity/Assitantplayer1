from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
import psutil
import time
from datetime import datetime

from database.mongodb import db
from config import config

start_time = time.time()

# ─── COMMAND HANDLERS ─────────────────────────────────────

async def start_handler(client: Client, message: Message):
    await db.increment_command_usage("start")
    await message.reply_text(
        f"Hello {message.from_user.mention}!\n\n"
        "I'm a powerful music bot with voice chat listening capabilities!\n\n"
        "**Available Commands:**\n"
        "/start - Start the bot\n"
        "/help - Get help\n"
        "/stats - View bot statistics\n"
        "/ping - Check bot latency\n"
        "/assiststart - Start assistant in voice chat\n"
        "/assistclose - Stop assistant from voice chat\n"
        "/play [song name] - Play a song\n\n"
        "**Voice Control:**\n"
        "Say 'Assistant play [song name]' in voice chat and I'll play it!\n"
        "The assistant listens continuously when active."
    )


async def help_handler(client: Client, message: Message):
    await db.increment_command_usage("help")
    await message.reply_text(
        """
**Music Bot Help**

**Basic Commands:**
/start - Start the bot
/help - Show this help message
/stats - View bot statistics
/ping - Check bot response time

**Music Commands:**
/assiststart - Start assistant and activate voice listening
/assistclose - Stop assistant from voice chat
/play [song name] - Play a song in voice chat
"""
    )


async def stats_handler(client: Client, message: Message):
    await db.increment_command_usage("stats")

    uptime_seconds = int(time.time() - start_time)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent

    total_plays = await db.get_total_plays()
    command_stats = await db.get_stats()
    active_chats = await db.get_active_chats()

    stats_text = f"""
**Bot Statistics**

**System:**
Uptime: {hours}h {minutes}m {seconds}s
CPU Usage: {cpu_percent}%
Memory Usage: {memory_percent}%

**Usage:**
Total Songs Played: {total_plays}
Active Chats: {len(active_chats)}
Commands Used: {sum(command_stats.values())}
"""
    await message.reply_text(stats_text)


async def ping_handler(client: Client, message: Message):
    await db.increment_command_usage("ping")
    start = time.time()
    msg = await message.reply_text("Pinging...")
    latency = int((time.time() - start) * 1000)
    await msg.edit_text(f"**Pong!**\nLatency: `{latency} ms`")


# ─── REGISTER HANDLERS (THIS WAS BROKEN BEFORE) ───────────

def setup_handlers(bot: Client, assistant: Client = None):
    bot.add_handler(
        MessageHandler(start_handler, filters.command("start") & filters.private)
    )
    bot.add_handler(
        MessageHandler(help_handler, filters.command("help"))
    )
    bot.add_handler(
        MessageHandler(stats_handler, filters.command("stats"))
    )
    bot.add_handler(
        MessageHandler(ping_handler, filters.command("ping"))
    )
