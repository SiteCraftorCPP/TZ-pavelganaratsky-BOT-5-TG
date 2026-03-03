import asyncio
from datetime import datetime, timedelta
from aiogram import Bot

from database import (
    get_all_messages,
    get_users,
    is_message_sent_for_user,
    mark_message_sent_for_user,
)


MSK_OFFSET = 3  # Москва = UTC+3


def _parse_send_time(send_time_str: str) -> datetime:
    return datetime.strptime(send_time_str, "%Y-%m-%d %H:%M:%S")


async def check_and_send_messages(bot: Bot):
    """
    Логика:
    - админ вносит дату/время в МСК;
    - в БД в schedule.send_time хранится это МСК-время;
    - у пользователя в users.timezone лежит строка вида '+2', '+3', '+4' и т.д.;
    - пользователю шлём тогда, когда в его локальной зоне наступает то же самое "часы:минуты, дата".

    Для этого считаем, что локальное время сервера тоже МСК.
    Тогда момент отправки для конкретного пользователя по серверному времени:
        send_time_for_user_msk = base_msk_time + (MSK_OFFSET - user_offset) часов.
    """

    messages = await get_all_messages()
    if not messages:
        return

    users = await get_users()
    if not users:
        return

    now_msk = datetime.now()

    for msg in messages:
        text = msg["message_text"]
        schedule_id = msg["id"]
        base_msk_time = _parse_send_time(msg["send_time"])

        for user in users:
            user_id = user["user_id"]
            tz_str = user["timezone"] or "+3"

            try:
                user_offset = int(tz_str.replace("+", "").replace(" ", ""))
            except ValueError:
                user_offset = MSK_OFFSET

            # когда по МСК нужно отослать этому конкретному пользователю,
            # чтобы он получил в то же "локальное время", что и МСК-время админа
            send_time_for_user_msk = base_msk_time + timedelta(
                hours=(MSK_OFFSET - user_offset)
            )

            if now_msk < send_time_for_user_msk:
                continue

            # уже отправляли этому пользователю это сообщение?
            if await is_message_sent_for_user(user_id, schedule_id):
                continue

            try:
                await bot.send_message(chat_id=user_id, text=text)
                await mark_message_sent_for_user(user_id, schedule_id)
            except Exception as e:
                print(f"Failed to send to {user_id}: {e}")
