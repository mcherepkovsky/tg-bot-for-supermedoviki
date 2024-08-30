import logging

from peewee import IntegrityError, DoesNotExist

from client_card.qrbackgen import QRGen
from db.models import Users, Positions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_all_employees_from_db():
    try:
        employees = Users.select().join(Positions).where(Positions.title.in_(["Administrator", "Client"]))
        return employees
    except DoesNotExist:
        return None


async def get_user_personal_qr_code(user_data):
    tg_id = user_data.get('tg_id')
    try:
        user = Users.get(Users.tg_id == tg_id)
        return user.personalQRCode
    except Exception:
        logger.error(f"Пользователь {tg_id} не найден.")
        user = await add_user(user_data)
        return user.personalQRCode


async def get_user_coffe_number(tg_id):
    try:
        user = Users.get(Users.tg_id == tg_id)
        return user.coffe_number
    except Exception:
        logger.error(f"Пользователь {tg_id} не найден.")
        return None


async def add_user(user_data):
    try:
        # Генерация QR-кода
        qr_image_bytes = QRGen.generate(id=user_data.get('tg_id'))
        # Создание записи пользователя с сохранением QR-кода
        user = Users.create(
            tg_id=user_data.get('tg_id'),
            tg_username=user_data.get('tg_username'),
            personalQRCode=qr_image_bytes  # Сохранение байтового представления QR-кода
        )
        logger.info(f"Пользователь {user.tg_id} успешно добавлен. || {qr_image_bytes}")
        return user
    except IntegrityError:
        logger.error(f"Пользователь {user_data.get('tg_id')} уже существует.")
        return None


async def update_coffe_number(tg_id):
    try:
        user = Users.get(Users.tg_id == tg_id)

        user.coffe_number += 1
        user.save()

        logger.info(f"Coffe_number пользователя {tg_id} успешно обновлён на '{user.coffe_number}'.")
        return True
    except DoesNotExist:
        logger.error(f"Пользователь с TG_ID {tg_id} не найден.")
        return False


async def update_position_id(tg_id, position_title):
    try:
        position = Positions.get(Positions.title == position_title)
        user = Users.get(Users.tg_id == tg_id)

        user.position_id = position.id
        user.save()

        logger.info(f"Position пользователя {tg_id} успешно обновлён на '{position}'.")

        return True
    except DoesNotExist:
        logger.error(f"Пользователь с TG_ID {tg_id} не найден.")
        return False
