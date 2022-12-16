from aiogram.types import reply_keyboard

#from aiogram.dispatcher.webhook import GetChatMember

import logging

#from aiogram.methods import GetChatMember
#from aiogram.methods.get_chat_member import GetChatMember
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
#import aioschedule


from config import TOKEN

bot = Bot(token=TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())

all_users  = []

all_haters = []



@dp.message_handler(content_types=['new_chat_members'])
async def handler_new_member(message: types.Message):
    if message.new_chat_members[0].username == None:
        await bot.send_message(message.chat.id,f"Нихао, {message.new_chat_members[0].first_name}! Добро пожаловать к нам! Конфа собирает народ на футбол, преимущественно по воскресеньям. Еженедельно необходимо голосовать в опросе, в противном случае я тебя репрессирую.")
    else:
        await bot.send_message(message.chat.id,f"Нихао, @{message.new_chat_members[0].username}! Добро пожаловать к нам! Конфа собирает народ на футбол, преимущественно по воскресеньям. Еженедельно необходимо голосовать в опросе, в противном случае я тебя репрессирую.")
        chat_id = message.chat.id
        await bot.get_chat_members_count(chat_id=chat_id)






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
