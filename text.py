from aiogram.types import reply_keyboard
#from config import *
#from sqlite import *
#from buttons import *
#from states import *
#from freesteam import parse_link

import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import filters
import asyncio


from config import TOKEN



HELP_COMMAND = """
/start - Начать работу с ботом
/help - Помощь
/description - описание бота
/reg - регистрация заявки
/channel - Наш канал
"""



bot = Bot(token=TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
     await message.answer(md.text(
            md.bold('Info about commands:\n'),
            md.text('🔸', md.bold('/cs'), md.code(' - Create Story')),
            md.text('🔸', md.bold('/cb'), md.code(' - Create Bug')),
            sep='\n',
        ),
        parse_mode=types.ParseMode.MARKDOWN_V2,
    )
    










if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
