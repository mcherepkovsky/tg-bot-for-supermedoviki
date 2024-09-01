import logging

from aiogram import Bot
from aiogram.types import BufferedInputFile

from config_reader import config
from services.message_deleter import delete_last_qr_msg

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


async def send_qr_code_to_client(tg_id, caption, photo_bytes):
    await delete_last_qr_msg(tg_id)

    try:
        photo = BufferedInputFile(photo_bytes, filename='qr_code.png')

        await bot.send_photo(
            chat_id=tg_id,
            photo=photo,
            caption=caption,
            parse_mode='HTML',
            disable_notification=True,
            show_caption_above_media=True
        )

        logger.info("Карта отправлена пользователю.")
    except Exception as e:
        logger.error(f"Ошибка при отправке карты пользователю: {e}")
