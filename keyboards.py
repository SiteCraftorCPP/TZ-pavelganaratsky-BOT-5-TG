from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def get_welcome_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="ЗАПРОС", callback_data="request_access")]]
    )


def get_timezone_keyboard():
    buttons = [
        [InlineKeyboardButton(text="+1 Берлин, Монтенегро", callback_data="tz_+1")],
        [InlineKeyboardButton(text="+2 Киев, Таллинн", callback_data="tz_+2")],
        [InlineKeyboardButton(text="+3 Москва, Анкара", callback_data="tz_+3")],
        [InlineKeyboardButton(text="+4 Баку, Тбилиси", callback_data="tz_+4")],
        [InlineKeyboardButton(text="+5 Екатеринбург, Ташкент", callback_data="tz_+5")],
        [InlineKeyboardButton(text="+6 Алматы, Бишкек", callback_data="tz_+6")],
        [InlineKeyboardButton(text="+7 Красноярск, Ханой", callback_data="tz_+7")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_admin_reply_keyboard():
    # Кнопка над клавиатурой, которая шлёт /admin
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Админ-панель")]],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def get_language_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 RU", callback_data="lang_ru"),
                InlineKeyboardButton(text="🇬🇧 EN", callback_data="lang_en"),
            ]
        ]
    )


def get_admin_keyboard():
    buttons = [
        [InlineKeyboardButton(text="📋 Сообщения рассылки", callback_data="admin_list")],
        [InlineKeyboardButton(text="➕ Добавить сообщение", callback_data="admin_add")],
        [InlineKeyboardButton(text="✏️ Приветственное сообщение", callback_data="admin_edit_welcome")],
        [InlineKeyboardButton(text="✏️ Ответ после выбора", callback_data="admin_edit_after_tz")],
        [InlineKeyboardButton(text="🧹 Удалить все сообщения", callback_data="admin_delete_all_confirm")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_request_actions_keyboard(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Одобрить", callback_data=f"approve_{user_id}"),
                InlineKeyboardButton(text="Отклонить", callback_data=f"reject_{user_id}"),
            ]
        ]
    )


def get_back_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]]
    )
