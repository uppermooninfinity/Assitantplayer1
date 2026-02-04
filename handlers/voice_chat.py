from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types import AudioPiped, VideoParameters, AudioParameters
from pytgcalls.exceptions import GroupCallNotFound, NotInGroupCallError
import asyncio
import logging
from config import config
from database.mongodb import db
from utils.logger import log_to_group

logger = logging.getLogger(__name__)

active_calls = {}
pytgcalls_instances = {}

async def assiststart_handler(client: Client, message: Message):
    await db.increment_command_usage("assiststart")
    chat_id = message.chat.id

    try:
        status_msg = await message.reply_text("Starting assistant...")

        try:
            assistant = client.assistant
            await assistant.join_chat(chat_id)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            logger.error(f"Error joining chat: {e}")

        await db.add_chat(chat_id, message.chat.title)

        if chat_id not in pytgcalls_instances:
            pytgcalls = PyTgCalls(assistant)
            pytgcalls_instances[chat_id] = pytgcalls
            await pytgcalls.start()

        await status_msg.edit_text(
            "Assistant joined successfully!\n\n"
            "Joining you in voice chat... Just speak and I'll go through your orders!\n\n"
            "Use /play [song name] to play music or just speak your request."
        )

        await log_to_group(
            client,
            f"**Assistant Started**\n"
            f"Chat: {message.chat.title}\n"
            f"Chat ID: {chat_id}\n"
            f"Started by: {message.from_user.mention}"
        )

    except Exception as e:
        logger.error(f"Error in assiststart: {e}")
        await message.reply_text(f"Error starting assistant: {str(e)}")

async def assistclose_handler(client: Client, message: Message):
    await db.increment_command_usage("assistclose")
    chat_id = message.chat.id

    try:
        if chat_id in pytgcalls_instances:
            pytgcalls = pytgcalls_instances[chat_id]
            try:
                await pytgcalls.leave_group_call(chat_id)
            except (GroupCallNotFound, NotInGroupCallError):
                pass

            del pytgcalls_instances[chat_id]

        if chat_id in active_calls:
            del active_calls[chat_id]

        await db.remove_chat(chat_id)

        await message.reply_text("Assistant left the voice chat. Goodbye!")

        await log_to_group(
            client,
            f"**Assistant Stopped**\n"
            f"Chat: {message.chat.title}\n"
            f"Chat ID: {chat_id}\n"
            f"Stopped by: {message.from_user.mention}"
        )

    except Exception as e:
        logger.error(f"Error in assistclose: {e}")
        await message.reply_text(f"Error closing assistant: {str(e)}")

async def join_voice_chat(assistant: Client, chat_id: int, audio_path: str):
    try:
        if chat_id not in pytgcalls_instances:
            pytgcalls = PyTgCalls(assistant)
            pytgcalls_instances[chat_id] = pytgcalls
            await pytgcalls.start()

        pytgcalls = pytgcalls_instances[chat_id]

        await pytgcalls.join_group_call(
            chat_id,
            AudioPiped(audio_path),
            stream_type=StreamType().pulse_stream
        )

        active_calls[chat_id] = True
        return True

    except Exception as e:
        logger.error(f"Error joining voice chat: {e}")
        return False

async def leave_voice_chat(chat_id: int):
    try:
        if chat_id in pytgcalls_instances:
            pytgcalls = pytgcalls_instances[chat_id]
            await pytgcalls.leave_group_call(chat_id)

        if chat_id in active_calls:
            del active_calls[chat_id]

        return True

    except Exception as e:
        logger.error(f"Error leaving voice chat: {e}")
        return False

def setup_handlers(bot: Client, assistant: Client):
    bot.assistant = assistant

    bot.add_handler(filters.command("assiststart") & filters.group, assiststart_handler)
    bot.add_handler(filters.command("assistclose") & filters.group, assistclose_handler)
