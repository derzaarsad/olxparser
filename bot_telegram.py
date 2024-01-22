from telegram import Bot
from read_config import get_telegram_api_key
import asyncio

bot_token = get_telegram_api_key()

async def send_message(chat_id, message):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

async def send_message_to_all(chat_id_list, message):
    # Define a delay between messages to different chats (in seconds)
    delay = 1  # Adjust this value based on your needs and Telegram's rate limits

    # Asynchronously send messages to all chat IDs
    tasks = [asyncio.create_task(send_message_with_delay(chat_id, message, delay)) for chat_id in chat_id_list]
    await asyncio.gather(*tasks)

async def send_message_with_delay(chat_id, message, delay):
    await send_message(chat_id, message)
    await asyncio.sleep(delay)
