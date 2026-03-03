import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

_raw_admins = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = {
    int(part.strip())
    for part in _raw_admins.split(",")
    if part.strip().isdigit()
}
