from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from .. filtres.role_filter import RoleFilter
from .. keyboards.simple_row import client_keyboard, admin_keyboard
from .. services.message_deleter import delete_messages

common_router = Router()


@common_router.message(
    Command(commands=["start"]),
)
async def cmd_start(message: Message):
    if await RoleFilter('Guest')(message):
        await start_message_main_guest(message)
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


async def start_message_main_guest(message: Message):
    # await message.answer(
    #     text=f"Вы находитесь в <b>Главном меню</b>.\nВыберите действие 👇",
    #     parse_mode='HTML',
    #     reply_markup=client_keyboard()
    #
    pass


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
