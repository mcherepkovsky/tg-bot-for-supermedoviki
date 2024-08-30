import logging
from aiogram import Bot

from config_reader import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(config.bot_token.get_secret_value())

async def send_to(tg_id, message):
    try:
        await bot.send_message(
            chat_id=tg_id,
            parse_mode='HTML',
            text=message,
        )

        logger.info("Сообщение отправлено пользователю.")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения пользователю: {e}")
