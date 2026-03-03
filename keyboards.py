from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_timezone_keyboard():
    buttons = [
        [InlineKeyboardButton(text="+2 Киев, Таллинн", callback_data="tz_+2")],
        [InlineKeyboardButton(text="+3 Москва, Анкара", callback_data="tz_+3")],
        [InlineKeyboardButton(text="+4 Баку, Тбилиси", callback_data="tz_+4")],
        [InlineKeyboardButton(text="+5 Екатеринбург, Ташкент", callback_data="tz_+5")],
        [InlineKeyboardButton(text="+6 Алматы, Бишкек", callback_data="tz_+6")],
        [InlineKeyboardButton(text="+7 Красноярск, Ханой", callback_data="tz_+7")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_admin_keyboard():
    buttons = [
        [InlineKeyboardButton(text="📋 Сообщения рассылки", callback_data="admin_list")],
        [InlineKeyboardButton(text="➕ Добавить сообщение", callback_data="admin_add")],
        [InlineKeyboardButton(text="🧹 Удалить все сообщения", callback_data="admin_delete_all_confirm")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]]
    )
