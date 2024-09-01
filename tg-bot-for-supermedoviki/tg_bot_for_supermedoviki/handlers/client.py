from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from db.database_handler import get_user_personal_qr_code
from aiogram.types import Message
from keyboards.simple_row import make_row_inline_keyboard_mutiple, make_row_inline_keyboard, menu_keyboard
from config_reader import config, menu_data
from services.sender import send_qr_code_to_client

client_router = Router()


@client_router.message(F.text.lower() == "💳 моя карта")
async def send_user_qr_code(
        message: Message,
        state: FSMContext,
        caption = "🔗 Вот ваша бонусная карточка с QR-кодом, для участия в программе:"
    ):
    await state.update_data(
        tg_id=message.from_user.id,
        tg_username=message.from_user.username
    )
    user_data = await state.get_data()

    # Получаем QR-код из базы данных
    qrCode = await get_user_personal_qr_code(user_data)

    if qrCode:
        # Отправляем фото
        await send_qr_code_to_client(message.from_user.id, caption, qrCode)
    else:
        await message.reply("QR-код не найден.")


@client_router.message(F.text.lower() == "📋 меню")
async def send_menu(message: Message):
    keyboard_items = menu_keyboard()
    await message.answer(
        text="Выберите категорию из нашего меню:",
        parse_mode='HTML',
        reply_markup=make_row_inline_keyboard_mutiple(keyboard_items)
    )


async def get_menu(message: Message, category):
    keyboard_items = [
        [{'text': '👈',
          'callback_data': f"getLeftCategory_{category}"},
         {'text': '👉',
          'callback_data': f"getRightCategory_{category}"}
         ],
        [{'text': '💁‍♂️ Назад 💁‍♀️',
          'callback_data': "getBackToMenu"}
         ]
    ]

    items = menu_data.get("menu", {}).get(category, [])

    if items:
        response = f"Меню для категории <b>{category}</b>:\n"
        for item in items:
            response += f"• <i>{item['название']}</i> "
            if 'цены' in item:
                response += f"\n"
                for size, price in item['цены'].items():
                    response += f" — {size.capitalize()} - {price} руб.\n"
            else:
                response += f"{item['цена']} руб.\n"

        await message.edit_text(
            text=response,
            parse_mode='HTML',
            reply_markup=make_row_inline_keyboard_mutiple(keyboard_items)
        )
    else:
        keyboard_items = [
            {'text': '‍💁‍♂️ Назад 💁‍',
             'callback_data': "getBackToMenu"},
        ]

        await message.edit_text(
            text=f"Категория '{category}' пока что пуста.",
            parse_mode='HTML',
            reply_markup=make_row_inline_keyboard(keyboard_items)
        )


@client_router.callback_query(lambda c: c.data and c.data.startswith(('getRightCategory_', 'getLeftCategory_')))
async def get_next_category(callback: types.CallbackQuery):
    await callback.answer()
    action, current_category = callback.data.split('_')

    categories = {1: "Медовики", 2: "Десерты", 3: "Кофе", 4: "Некофе", 5: "Чай", 6: "Торты на заказ", 7: "Добавки"}

    # Поиск текущего индекса
    current_index = None
    for index, name in categories.items():
        if name == current_category:
            current_index = index
            break

    next_category = categories[1]

    if action == "getRightCategory":
        # Определение следующей категории
        if current_index is not None:
            next_index = current_index + 1
            if next_index in categories:
                next_category = categories[next_index]
    elif action == "getLeftCategory":
        # Определение следующей категории
        if current_index is not None:
            next_index = current_index - 1
            if next_index in categories:
                next_category = categories[next_index]

    await get_menu(callback.message, next_category)


@client_router.callback_query(F.data == "getBackToMenu")
async def get_medoviki(callback: types.CallbackQuery):
    keyboard_items = menu_keyboard()
    await callback.answer()
    await callback.message.edit_text(
        text="Выберите категорию из нашего меню:",
        parse_mode='HTML',
        reply_markup=make_row_inline_keyboard_mutiple(keyboard_items)
    )


@client_router.callback_query(F.data == "getMedoviki")
async def get_medoviki(callback: types.CallbackQuery):
    await callback.answer()
    await get_menu(callback.message, "Медовики")


@client_router.callback_query(F.data == "getDesserts")
async def get_desserts(callback: types.CallbackQuery):
    await callback.answer()
    await get_menu(callback.message, "Десерты")


@client_router.callback_query(F.data == "getCoffe")
async def get_coffe(callback: types.CallbackQuery):
    await callback.answer()
    await get_menu(callback.message, "Кофе")


@client_router.callback_query(F.data == "getNekofe")
async def get_nekofe(callback: types.CallbackQuery):
    await callback.answer()
    await get_menu(callback.message, "Некофе")


@client_router.callback_query(F.data == "getTea")
async def get_tea(callback: types.CallbackQuery):
    await callback.answer()
    await get_menu(callback.message, "Чай")


@client_router.callback_query(F.data == "getCakesToOrder")
async def get_cakes_to_order(callback: types.CallbackQuery):
    await callback.answer()
    await get_menu(callback.message, "Торты на заказ")


@client_router.callback_query(F.data == "getAdditives")
async def get_additives(callback: types.CallbackQuery):
    await callback.answer()
    await get_menu(callback.message, "Добавки")
