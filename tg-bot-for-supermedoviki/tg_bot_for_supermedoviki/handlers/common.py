import logging
from io import BytesIO

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, InputFile, BufferedInputFile

from filtres.role_filter import RoleFilter
from keyboards.simple_row import client_keyboard, admin_keyboard
from services.message_deleter import delete_messages
from handlers.client import send_user_qr_code
from db.database_handler import get_user_coffe_number
from db.database_handler import update_coffe_number, update_user_qr
from services.sender import send_qr_code_to_client

common_router = Router()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@common_router.message(
    Command(commands=["start"]),
    RoleFilter(role='Guest')
)
async def cmd_start(message: Message, state: FSMContext):
    await start_message_main_guest(message, state)


@common_router.message(
    Command(commands=["start"]),
    RoleFilter(role='Client')
)
async def cmd_start(message: Message, state: FSMContext):
    await start_message_main_guest(message, state)


@common_router.message(
    Command(commands=["start"]),
    RoleFilter(role='Administrator')
)
async def cmd_start(message: Message, state: FSMContext):
    await start_message_main_admin(message, state)


# async def start_message_main_client(message: Message):
#     await message.answer(
#         text=f"Вы находитесь в <b>Главном меню</b>.\nВыберите действие 👇",
#         parse_mode='HTML',
#         reply_markup=client_keyboard()
#     )


async def start_message_main_admin(message: Message, state: FSMContext):
    full_text = message.text
    command, *args = full_text.split()

    if args:
        coffe_number = await get_user_coffe_number(args[0])
        if coffe_number is not None:
            text = f"QR-код клиента <i>{args[0]}</i> <b>принят</b>.\nСтатус <b>{coffe_number + 1}/8</b> кофе."
            await update_coffe_number(args[0])
            # отправка карточки клиенту
            new_qr_image = await update_user_qr(args[0], coffe_number)
            caption = f"Ваша бонусная карточка успешно принята! 🎉\nНа данный момент у вас собрано <b>{coffe_number + 1} из 8</b> кофе.\n" \
                      f"Еще немного, и вы сможете получить бесплатный напиток! 😍"
            await send_qr_code_to_client(args[0], caption, new_qr_image)
        else:
            text = f"Пользователь с ID <i>{args[0]}</i> не найден."

        await start_message_main_admin_null(message, text=text)


async def start_message_main_admin_null(message: Message, text=f"Вы находитесь в <b>Главном меню</b>."):
    await message.answer(
        text=text,
        parse_mode='HTML',
        reply_markup=admin_keyboard()
    )


# вызов по нажатию на Информация
async def start_message_main_guest(message: Message, state: FSMContext):
    text = "👋 Добро пожаловать в <b>Super Medovik!</b> Мы рады видеть вас среди наших гостей.\n\n" \
           "🎂 У нас вы можете насладиться классическими и оригинальными вкусами медовиков, приготовленных вручную по советскому рецепту. " \
           "А также попробовать наш ассортимент кофе и чая.\n\n" \
           "💳 Присоединяйтесь к нашей программе лояльности! " \
           "Отметьте <b>7 чашек кофе</b> <i>(исключая кофе за 2 руб.)</i>, и получите 8-й кофе или медовик <b>в подарок</b>!"

    keyboard_remove = ReplyKeyboardRemove()

    await message.answer(
        text=text,
        parse_mode='HTML',
        reply_markup=keyboard_remove
    )

    await send_user_qr_code(message, state)

    text = "📍 <b>Наши адреса: </b>\n" \
           "• Якуба Коласа, 25/1\n" \
           "• Ложинская, 22 - 2\n" \
           "• Уманская, 54 (ТЦ «Глобо»)\n\n" \
           "Спасибо, что выбираете нас! Приятного чаепития! 🍰☕"

    await message.answer(
        text=text,
        parse_mode='HTML',
        reply_markup=client_keyboard()
    )


async def handle_unhandled_message(message: Message):
    message_ids_to_delete = [message.message_id - i for i in range(1)]
    await delete_messages(message.chat.id, message_ids_to_delete)
