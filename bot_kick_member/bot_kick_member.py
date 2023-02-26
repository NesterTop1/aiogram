from aiogram.types import reply_keyboard

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
#import aioschedule


from config import TOKEN






@bot.message_handler(content_types=["new_chat_members"])
def new_member(message):
    name = message.new_chat_members[0].first_name 
    bot.send_message(message.chat.id, f"Добро пожаловать, @{name}!")










if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
