import config
from check import check_user
from monitoring import get_server_status
from actions import power_off_server
from utils.py import flog
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from datetime import datetime
import logging

logging.basicConfig(level=logging.ERROR, filename="logs/agent.log", filemode="a")

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):    
    if not await check_user(message, config.ADMIN_ID):
        return

    await message.answer("<b>⚡ Radhaunt EDR agent succesfuly activated, Admin.</b>\nEnter '/help' to get a list of commands.", parse_mode=ParseMode.HTML)

@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    if not await check_user(message, config.ADMIN_ID):
        return
    
    help_text = (
        "<b>🐲 RADHAUNT EDR HELP PAGE 🐲</b>\n\n"
        "<b>Monitoring:</b>\n"
        "'/status' - Server status monitoring.\n\n"
        "<b>Actions</b>:\n"
        "'/shutdown' - Power off server.\n\n"
        "<b>Bot features</b>:\n"
        "'/start' - Activation and check.\n"
        "'/help' - This menu."
    )

    await message.answer(help_text, parse_mode=ParseMode.HTML)

@dp.message(Command('status'))
async def cmd_status(message: types.Message):
    if not await check_user(message, config.ADMIN_ID):
        return
    
    status_prompt = await message.answer("🔄 Collecting data...")
    server_status = get_server_status()

    await status_prompt.edit_text(server_status, parse_mode=ParseMode.HTML)

@dp.message(Command('shutdown'))
async def cmd_shutdown(message: types.Message):
    if not await check_user(message, config.ADMIN_ID):
        return
    
    await message.answer("Power off...")
    power_off_server()

async def on_startup(bot: Bot):
    try:
        current_time = datetime.now()
        await bot.send_message(chat_id=config.ADMIN_ID, text=f"-----------------------------------------------------\n|🐲<b>[HOST IS UP!]</b>🐲                         |\n|Date: <u>{current_time}</u>|\n-----------------------------------------------------", parse_mode=ParseMode.HTML,)
    except Exception as e:
        print(f"Error: {e}")


async def main():
    print("Starting bot...")
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.critical(flog(e), exc_info=True)
        raise e