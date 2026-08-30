import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command

async def check_user(message: types.Message, admin_id: int) -> bool:
    if message.from_user.id != admin_id:
        await message.answer("❌ Access denied.")
        return False
    return True