import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("RADHAUNT_TELEGRAM_API_TOKEN")
if not API_TOKEN:
    raise ValueError("ERROR: RADHAUNT_TELEGRAM_API_TOKEN not found in .env")

raw_admin_id = os.getenv("ADMIN_TELEGRAM_ID")
if not raw_admin_id:
    raise ValueError("ERROR: ADMIN_TELEGRAM_ID not found in .env")

try:
    ADMIN_ID = int(raw_admin_id)
except ValueError:
    raise ValueError("ERROR: ADMIN_TELEGRAM_ID must to be integer!")

BOT_USER_IN_SYSTEM = "radhaunt_agent"