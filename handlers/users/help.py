from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp

HELP_COMMAND = """
/start - Начать работу с ботом
/help - Помощь
/description - описание бота
/registration - регистрация заявки
/channel - Наш канал
"""

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply(text=HELP_COMMAND)