import aiosqlite
import datetime

DB_NAME = "bot.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                timezone TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_text TEXT,
                send_time TIMESTAMP,
                is_sent BOOLEAN DEFAULT 0
            )
        """
        )
        # Пер-юзерное состояние доставки сообщений
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS user_message_status (
                user_id INTEGER,
                schedule_id INTEGER,
                is_sent BOOLEAN DEFAULT 0,
                PRIMARY KEY (user_id, schedule_id)
            )
        """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                text TEXT,
                photo_file_id TEXT
            )
        """
        )
        await db.commit()


async def add_user(user_id: int, timezone: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR REPLACE INTO users (user_id, timezone) VALUES (?, ?)",
            (user_id, timezone),
        )
        await db.commit()


async def get_users():
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT user_id, timezone FROM users") as cursor:
            return await cursor.fetchall()


async def add_message(text: str, send_time: datetime.datetime):
    # В БД храним одно базовое время по МСК
    send_time_str = send_time.strftime("%Y-%m-%d %H:%M:%S")
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO schedule (message_text, send_time) VALUES (?, ?)",
            (text, send_time_str),
        )
        await db.commit()


async def get_all_messages():
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM schedule ORDER BY send_time") as cursor:
            return await cursor.fetchall()


async def get_message(message_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM schedule WHERE id = ?", (message_id,)
        ) as cursor:
            return await cursor.fetchone()


async def update_message(message_id: int, text: str, send_time: datetime.datetime):
    send_time_str = send_time.strftime("%Y-%m-%d %H:%M:%S")
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE schedule SET message_text = ?, send_time = ? WHERE id = ?",
            (text, send_time_str, message_id),
        )
        await db.commit()


async def delete_message(message_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM schedule WHERE id = ?", (message_id,))
        await db.execute(
            "DELETE FROM user_message_status WHERE schedule_id = ?", (message_id,)
        )
        await db.commit()


async def delete_all_messages():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM schedule")
        await db.execute("DELETE FROM user_message_status")
        await db.commit()


async def is_message_sent_for_user(user_id: int, schedule_id: int) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT is_sent FROM user_message_status WHERE user_id = ? AND schedule_id = ?",
            (user_id, schedule_id),
        ) as cursor:
            row = await cursor.fetchone()
            if not row:
                return False
            return bool(row["is_sent"])


async def mark_message_sent_for_user(user_id: int, schedule_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT INTO user_message_status (user_id, schedule_id, is_sent)
            VALUES (?, ?, 1)
            ON CONFLICT(user_id, schedule_id) DO UPDATE SET is_sent = 1
        """,
            (user_id, schedule_id),
        )
        await db.commit()


async def seed_march_if_needed():
    """
    Заполнить расписание на март, если таблица schedule пока пустая.
    Даты/время интерпретируются как МСК.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT 1 FROM schedule LIMIT 1") as cursor:
            row = await cursor.fetchone()
            if row:
                return

    current_year = datetime.datetime.now().year

    schedule = [
        ("29.6", "02.03", "14:07"),
        ("14.6", "09.03", "16:58"),
        ("10.2", "12.03", "05:29"),
        ("3.4", "21.03", "08:13"),
        ("2.2", "22.03", "09:06"),
        ("29.6", "29.03", "21:04"),
    ]

    for text, date_str, time_str in schedule:
        dt_str = f"{current_year}.{date_str} {time_str}"
        dt = datetime.datetime.strptime(dt_str, "%Y.%d.%m %H:%M")
        await add_message(text, dt)


async def get_setting(key: str):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT key, text, photo_file_id FROM settings WHERE key = ?", (key,)
        ) as cursor:
            return await cursor.fetchone()


async def set_setting(key: str, text: str | None, photo_file_id: str | None):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT INTO settings (key, text, photo_file_id)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                text = excluded.text,
                photo_file_id = excluded.photo_file_id
        """,
            (key, text, photo_file_id),
        )
        await db.commit()
