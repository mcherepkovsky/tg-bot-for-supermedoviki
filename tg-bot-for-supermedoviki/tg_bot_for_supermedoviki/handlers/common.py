from io import BytesIO

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, InputFile, BufferedInputFile

from filtres.role_filter import RoleFilter
from keyboards.simple_row import client_keyboard, admin_keyboard
from services.message_deleter import delete_messages
from db.database_handler import get_user_personal_qr_code


common_router = Router()


@common_router.message(
    Command(commands=["start"]),
)
async def cmd_start(message: Message, state: FSMContext):
    if await RoleFilter('Guest')(message):
        await start_message_main_guest(message, state)
    else:
        if RoleFilter('Client'):
            keyboard = client_keyboard()
        elif RoleFilter('Administrator'):
            keyboard = admin_keyboard()
        else:
            keyboard = ReplyKeyboardRemove()

        await message.reply(f"Приветствую.", parse_mode='HTML')
        await message.answer("Выберите действие 👇",
                             reply_markup=keyboard,
                             disable_notification=True)


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

    await state.update_data(
        tg_id=message.from_user.id,
        tg_username=message.from_user.username
    )
    user_data = await state.get_data()

    caption = "🔗 Вот ваша бонусная карточка с QR-кодом, чтобы начать участие в программе:"

    await send_user_qr_code(message, user_data, caption)

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


async def send_user_qr_code(message, user_data, caption):
    # Получаем QR-код из базы данных
    qrCode = await get_user_personal_qr_code(user_data)
    if qrCode:
        # Преобразуем байты в InputFile для отправки фото
        photo = BufferedInputFile(qrCode, filename='qr_code.png')

        # Отправляем фото
        await message.answer_photo(
            photo=photo,
            caption=caption,
            show_caption_above_media=True,
            disable_notification=True,
            parse_mode='HTML'
        )
    else:
        await message.reply("QR-код не найден.")



async def handle_unhandled_message(message: Message):
    message_ids_to_delete = [message.message_id - i for i in range(1)]
    await delete_messages(message.chat.id, message_ids_to_delete)


async def start_message_main_client(message: Message):
    await message.answer(
        text=f"Вы находитесь в <b>Главном меню</b>.\nВыберите действие 👇",
        parse_mode='HTML',
        reply_markup=client_keyboard()
    )


async def start_message_main_admin(message: Message):
    await message.answer(
        text=f"Вы находитесь в <b>Главном меню</b>.\nВыберите действие 👇",
        parse_mode='HTML',
        reply_markup=admin_keyboard()
    )
