from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from services.information_handlers import information_message_admin, information_message_success, \
    information_message_entry
from keyboards.simple_row import admin_keyboard
from handlers.common import start_message_main_admin_null


admin_router = Router()


class ActionState(StatesGroup):
    start_state = State()
    inf_msg = State()
    inf_msg_entr = State()
    inf_msg_success = State()


@admin_router.message(F.text.lower() == "📢 рассылка")
async def information_message(message: Message, state: FSMContext):
    await information_message_admin(message, state, ActionState)


@admin_router.message(
    F.text.lower() == "❌ отмена",
    ActionState.inf_msg
)
@admin_router.message(
    F.text.lower() == "❌ отмена",
    ActionState.inf_msg_entr
)
@admin_router.message(
    F.text.lower() == "❌ отмена",
    ActionState.inf_msg_success
)
async def employees_buttons(message: Message, state: FSMContext):
    await state.clear()

    await start_message_main_admin_null(message)


@admin_router.message(ActionState.inf_msg_entr, F.text)
async def sup_admin_information_message_entry(message: Message, state: FSMContext):
    await information_message_entry(message, state, ActionState)


@admin_router.message(ActionState.inf_msg_success, F.text.lower() == "✅ подтвердить")
async def sup_admin_information_message_success(message: Message, state: FSMContext):
    await information_message_success(message, state, ActionState)


@admin_router.message(ActionState.inf_msg_success, F.text.lower() == "🔄 изменить")
async def information_message_re_enter(message: Message, state: FSMContext):
    await information_message(message, state)
