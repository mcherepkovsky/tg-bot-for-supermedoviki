from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from services.information_handlers import information_message_admin, information_message_success, \
    information_message_entry
from handlers.common import start_message_main_admin_null
from keyboards.simple_row import make_row_keyboard, make_row_inline_keyboard_mutiple, make_row_keyboard_mutiple, \
    admin_keyboard
from services.message_deleter import delete_messages
from db.database_handler import update_position_id

admin_router = Router()


class ActionState(StatesGroup):
    start_state = State()
    inf_msg = State()
    inf_msg_entr = State()
    inf_msg_success = State()

    user_change_role = State()
    user_change_role_success = State()


@admin_router.message(F.text.lower() == "🎭 изменить роль пользователя")
async def emloyee_role_change(message: Message, state: FSMContext):
    await state.set_state(ActionState.user_change_role)

    await message.answer(
        text="Введите <b>Telegram ID</b> пользователя, роль которого хотите изменить 👇",
        reply_markup=make_row_keyboard(["❌ Отмена"]),
        parse_mode='HTML'
    )


@admin_router.message(ActionState.user_change_role, F.text)
async def emloyee_role_change_role(message: Message, state: FSMContext):
    await state.update_data(
        id_change_msg=message.text
    )

    keyboard_items = [
        [{'text': 'Администратор',
          'callback_data': "setAdminRole"}],
        [{'text': 'Клиент',
          'callback_data': "setClientRole"}],
    ]

    await message.answer(
        text="Выберите роль, на которую хотите изменить 👇",
        reply_markup=make_row_inline_keyboard_mutiple(keyboard_items),
    )


@admin_router.callback_query(F.data == "setAdminRole")
async def set_admin_role(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(
        role_change_msg="Administrator"
    )
    await user_change_role_success(callback, state)


@admin_router.callback_query(F.data == "setClientRole")
async def set_client_role(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(
        role_change_msg="Client"
    )
    await user_change_role_success(callback, state)


async def user_change_role_success(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ActionState.user_change_role_success)

    data = await state.get_data()
    id = data.get('id_change_msg')
    role = data.get('role_change_msg')

    await callback.message.answer(
        text=f"Вы собираетесь изменить роль пользователя <i>{id}</i> на <i>{role}</i>\nВсё верно?",
        parse_mode='HTML',
        reply_markup=make_row_keyboard_mutiple([
            ["✅ Подтвердить", "🔄 Изменить"],
            ["❌ Отмена"]]
        )
    )


@admin_router.message(ActionState.user_change_role_success, F.text.lower() == "✅ подтвердить")
async def user_change_role_success_change(message: Message, state: FSMContext):
    data = await state.get_data()
    tg_id = data.get('id_change_msg')
    role = data.get('role_change_msg')

    message_ids_to_delete = [message.message_id - i for i in range(5)]
    await delete_messages(message.chat.id, message_ids_to_delete)

    result = await update_position_id(tg_id, role)
    text = f"Роль пользователя <i>{tg_id}</i> успешно изменена на <i>{role}</i>." if result else f"Не удалось изменить роль пользователя <i>{tg_id}</i>."

    await message.answer(
        text=text,
        parse_mode='HTML',
        reply_markup=admin_keyboard()
    )

    await state.clear()
    await start_message_main_admin_null(message)


@admin_router.message(ActionState.user_change_role_success, F.text.lower() == "🔄 изменить")
async def information_message_re_enter(message: Message, state: FSMContext):
    await emloyee_role_change(message, state)


@admin_router.message(F.text.lower() == "📢 рассылка")
async def information_message(message: Message, state: FSMContext):
    await information_message_admin(message, state, ActionState)


@admin_router.message(
    F.text.lower().startswith("❌ отмена"),
    ActionState.user_change_role_success
)
@admin_router.message(
    F.text.lower() == "❌ отмена",
    ActionState.user_change_role
)
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
async def users_buttons(message: Message, state: FSMContext):
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
