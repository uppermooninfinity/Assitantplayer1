from pyrogram import Client
from datetime import datetime
from config import config
import logging
import platform
import psutil

logger = logging.getLogger(__name__)


async def send_startup_log(bot: Client, bot_info, assistant_info, start_time):
    """
    Sends startup log to logger group.
    This function is FAIL-SAFE:
    - If chat_id is invalid
    - If bot has no permission
    - If bot is not in group
    - If Telegram errors
    Bot will continue running normally.
    """
    try:
        # safely resolve chat id
        try:
            chat_id = int(config.LOGGER_GROUP_ID)
        except Exception:
            logger.warning("LOGGER_GROUP_ID is invalid or not set, skipping startup log")
            return

        system_info = (
            "**Bot Started Successfully**\n\n"
            "**Bot Information:**\n"
            f"Name: {bot_info.first_name}\n"
            f"Username: @{bot_info.username}\n"
            f"ID: `{bot_info.id}`\n\n"
            "**Assistant Information:**\n"
            f"Name: {assistant_info.first_name}\n"
            f"Username: @{assistant_info.username}\n"
            f"ID: `{assistant_info.id}`\n\n"
            "**System Information:**\n"
            f"Platform: {platform.system()} {platform.release()}\n"
            f"Python: {platform.python_version()}\n"
            f"CPU Cores: {psutil.cpu_count()}\n"
            f"RAM: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB\n\n"
            "**Start Time:**\n"
            f"{start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
            "Bot is now running and ready to serve!"
        )

        await bot.send_message(
            chat_id=chat_id,
            text=system_info,
            parse_mode="markdown"
        )

        logger.info("Startup log sent successfully")

    except Exception as e:
        # swallow ALL telegram-related errors
        logger.warning(f"Startup log skipped: {e}")


async def log_to_group(bot: Client, message: str):
    """
    Generic logger.
    Will NEVER crash the bot.
    """
    try:
        try:
            chat_id = int(config.LOGGER_GROUP_ID)
        except Exception:
            return

        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="markdown"
        )

    except Exception:
        # silently ignore all errors
        pass
