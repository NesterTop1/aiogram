from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db
from keyboards.default.main_menu import main_menu



@dp.message_handler(commands=['description'])
async def send_description(message: types.Message):
    await message.answer("Я бот для создания постов в канале @")