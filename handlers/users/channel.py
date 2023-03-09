from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db
from keyboards.default.main_menu import main_menu







@dp.message_handler(commands=['channel'])
async def send_channel(message: types.Message):
    await message.answer("Наш канал - @zeroem0tion")