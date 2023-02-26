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

class Person(StatesGroup): 
    contact = State()
    connect = State()  
    calldata = State()
    cancel = State()


@dp.message_handler(commands='start')
async def get_age(msg: types.Message):
     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
     keyboard.add(types.KeyboardButton(text="Отправить номер телефона 📱", request_contact=True))
     await msg.answer("Отправь свой контакт:", reply_markup=keyboard)
     await Person.contact.set()
     return


@dp.message_handler(content_types=types.ContentType.CONTACT, state=Person.contact)
async def contacts(msg: types.Message, state: FSMContext):
    await msg.answer(f"Твой номер успешно получен: @{msg.from_user.username}", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
