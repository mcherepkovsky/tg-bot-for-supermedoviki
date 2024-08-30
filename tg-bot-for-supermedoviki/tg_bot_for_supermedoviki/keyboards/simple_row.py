from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton


def menu_keyboard():
    menu_button = [
        [{'text': '🥮 Медовики',
          'callback_data': "getMedoviki"},
         {'text': '🍮 Десерты',
          'callback_data': "getDesserts"}
         ],
        [{'text': '☕ Кофе',
          'callback_data': "getCoffe"},
         {'text': '🥤 Некофе',
          'callback_data': "getNekofe"},
         {'text': '🍵 Чай',
          'callback_data': "getTea"}
         ],
        [{'text': '🍰 Торты на заказ 🍰',
          'callback_data': "getCakesToOrder"}
         ],
        [{'text': '➕ Добавки ➕',
          'callback_data': "getAdditives"}
         ],
    ]
    return menu_button


def admin_keyboard():
    first_button = [
        [KeyboardButton(text="📢 Рассылка")],
        [KeyboardButton(text="✏️ Редактировать меню")],
        [KeyboardButton(text="🎭 Изменить роль пользователя")],
    ]
    markup = ReplyKeyboardMarkup(keyboard=first_button, resize_keyboard=True)
    return markup


def client_keyboard():
    first_button = [
        [KeyboardButton(text="💳 Моя карта")],
        [KeyboardButton(text="📋 Меню")]
    ]
    markup = ReplyKeyboardMarkup(keyboard=first_button, resize_keyboard=True)
    return markup


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_row_keyboard_mutiple_2(items: list[list[str]]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    keyboard = [
        [
            KeyboardButton(
                text=item,
            )
            for item in row
        ]
        for row in items
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def make_row_keyboard_mutiple(items: list[list[str]]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    keyboard = [
        [
            KeyboardButton(
                text=item,
            )
            for item in row
        ]
        for row in items
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# inline keyboard
def make_row_inline_keyboard(items: list[dict]) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру с кнопками в один ряд
    :param items: список словарей с текстами для кнопок и callback_data
    :return: объект инлайн-клавиатуры
    """
    row = [
        InlineKeyboardButton(
            text=item['text'],
            callback_data=item.get('callback_data', item['text'])
        )
        for item in items
    ]
    return InlineKeyboardMarkup(inline_keyboard=[row])


def make_row_inline_keyboard_mutiple(items: list[list[dict]]) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру с кнопками в несколько рядов
    :param items: список списков словарей с текстами для кнопок и callback_data
    :return: объект инлайн-клавиатуры
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text=item['text'],
                callback_data=item.get('callback_data', item['text'])
            )
            for item in row
        ]
        for row in items
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
