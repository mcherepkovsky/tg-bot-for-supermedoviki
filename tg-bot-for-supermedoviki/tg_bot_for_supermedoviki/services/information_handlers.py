from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from services.sender import send_to
from keyboards.simple_row import admin_keyboard
from handlers.common import start_message_main_admin_null
from db.database_handler import get_all_employees_from_db
from keyboards.simple_row import make_row_keyboard, make_row_keyboard_mutiple

async def information_message_admin(message: Message, state: FSMContext, ActionState):
    await state.set_state(ActionState.inf_msg_entr)

    await message.answer(
        text="Введите сообщение для отправки пользователям 👇",
        reply_markup=make_row_keyboard(["❌ Отмена"])
    )


async def information_message_entry(message: Message, state: FSMContext, ActionState):
    await state.update_data(
        inf_msg=message.text
    )

    data = await state.get_data()
    inf_msg = data.get('inf_msg')

    await message.answer(
        text=f"Вы собираетесь отправить сообщение:\n\n<i>{inf_msg}</i>\n\nВсё верно?",
        parse_mode='HTML',
        reply_markup=make_row_keyboard_mutiple([
            ["✅ Подтвердить", "🔄 Изменить"],
            ["❌ Отмена"]]
        )
    )

    await state.set_state(ActionState.inf_msg_success)


async def information_message_success(message: Message, state: FSMContext, ActionState):
    data = await state.get_data()
    inf_msg = data.get('inf_msg')

    await state.set_state(ActionState.start_state)

    await message.answer(
        text="Сообщение отправлено.",
        reply_markup=admin_keyboard()
    )

    employees = await get_all_employees_from_db()

    for employee in employees:
        await send_to(employee.tg_id, inf_msg)

    await start_message_main_admin_null(message)
