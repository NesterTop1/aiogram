from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db
from keyboards.default.main_menu import main_menu


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привет! Начни работу со мной! Для регистрации нажми /registration")
    if db.select_user(id=message.from_user.id) is None:
        db.add_user(id=message.from_user.id, Name=message.from_user.username)
