from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from database import add_user, get_setting
from keyboards import get_timezone_keyboard

router = Router()


DEFAULT_WELCOME_TEXT = (
    "Привет!\n\n"
    "Я - Бот \"Ледяной\" Луны🌙\n\n"
    "Вместе с тобой мы будем наблюдать за процессом жизни.\n\n"
    "Выбор часового пояса:"
)

DEFAULT_AFTER_TZ_TEXT = "Часовой пояс {tz} установлен."


@router.message(Command("start"))
async def cmd_start(message: Message):
    setting = await get_setting("welcome")
    text = setting["text"] if setting and setting["text"] else DEFAULT_WELCOME_TEXT
    photo_id = setting["photo_file_id"] if setting else None

    if photo_id:
        await message.answer_photo(photo=photo_id, caption=text, reply_markup=get_timezone_keyboard())
    else:
        await message.answer(text, reply_markup=get_timezone_keyboard())


@router.callback_query(F.data.startswith("tz_"))
async def process_timezone(callback: CallbackQuery):
    try:
        timezone = callback.data.split("_", 1)[1]
        user_id = callback.from_user.id

        await add_user(user_id, timezone)

        setting = await get_setting("after_timezone")
        if setting and setting["text"]:
            text = setting["text"].replace("{tz}", timezone)
        else:
            text = DEFAULT_AFTER_TZ_TEXT.format(tz=timezone)
        photo_id = setting["photo_file_id"] if setting else None

        # убираем клавиатуру выбора пояса
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except Exception:
            pass

        if photo_id:
            await callback.message.answer_photo(photo=photo_id, caption=text)
        else:
            await callback.message.answer(text)

        await callback.answer()
    except Exception:
        await callback.answer("Произошла ошибка, попробуйте ещё раз позже.", show_alert=True)
