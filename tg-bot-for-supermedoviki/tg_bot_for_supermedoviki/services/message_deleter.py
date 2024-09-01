import logging

from aiogram import Bot
from config_reader import config
from db.database_handler import get_last_qr_msg

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(config.bot_token.get_secret_value())


async def delete_messages(chat_id: int, message_ids: list[int]):
    for message_id in message_ids:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
            logger.info(f"Сообщение {message_id} в чате {chat_id} успешно удалено.")
        except Exception as e:
            logger.error(f"Ошибка при удалении сообщения {message_id} в чате {chat_id}: {e}")


async def delete_last_qr_msg(chat_id: int):
    message_id = await get_last_qr_msg(chat_id)
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id+1)
        logger.info(f"Сообщение {message_id} в чате {chat_id} успешно удалено.")
    except Exception as e:
        logger.error(f"Ошибка при удалении сообщения {message_id} в чате {chat_id}: {e}")
