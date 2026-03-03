from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from database import add_user
from keyboards import get_timezone_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "Привет!\n\n"
        "Я - Бот \"Ледяной\" Луны🌙\n\n"
        "Вместе с тобой мы будем наблюдать за процессом жизни.\n\n"
        "Выбор часового пояса:"
    )
    await message.answer(text, reply_markup=get_timezone_keyboard())

@router.callback_query(F.data.startswith("tz_"))
async def process_timezone(callback: CallbackQuery):
    try:
        timezone = callback.data.split("_", 1)[1]
        user_id = callback.from_user.id

        await add_user(user_id, timezone)

        await callback.message.edit_text(
            f"Часовой пояс {timezone} установлен."
        )
        await callback.answer()
    except Exception as e:
        # Если что-то пошло не так, хотя бы ответим на callback,
        # чтобы не висела "крутилка" у пользователя.
        await callback.answer("Произошла ошибка, попробуйте ещё раз позже.", show_alert=True)
