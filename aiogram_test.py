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




class Form(StatesGroup):
    name = State()  
    projected = State()
    connect = State()  
    calldata = State()
    cancel = State()







@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привет! Начни работу со мной! Для регистрации нажми /reg")



@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply(text=HELP_COMMAND)


@dp.message_handler(commands=['description'])
async def send_description(message: types.Message):
    await message.answer("Я бот для создания постов в канале @zeroem0tion")


@dp.message_handler(commands=['channel'])
async def send_channel(message: types.Message):
    await message.answer("Наш канал - @zeroem0tion")



@dp.message_handler(commands='reg')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.name.set()

    await message.reply("Как тебя зовут?")



@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['name'] = message.text

    await Form.next()
    await message.reply("Опишите ваш проект")


@dp.message_handler(state=Form.projected)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['projected'] = message.text

    await Form.next()
    await message.reply("Выберите способ связи")



@dp.message_handler(state=Form.connect)
async def process_connect(message: types.Message, state: FSMContext):
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Да"))
    poll_keyboard.add(types.KeyboardButton(text="Отмена"))
    async with state.proxy() as data:
        data['connect'] = message.text
        #x = md.text(('Данные введены верно?'),md.bold('Заказчик:'), md.text(data['name']),sep='')
        q = (md.text('Данные введены верно?'), sep='\n')
        w = (md.text(md.bold('Заказчик:'), md.text(data['name']), md.text('Проект:', md.text(data['projected'])),
                            md.text('Способ связи:', data['connect']), sep='\n')
        #e = md.bold('Проект:'), md.text(data['projected']), sep='\n'
        #r = md.bold('Способ связи:'), md.text(data['connect']), sep='\n'
        #question = md.text(
        #    md.text('Данные введены верно?'),md.bold('Заказчик:'), md.text(data['name']),
        #    md.bold('Проект:'), md.text(data['projected']),
        #    md.bold('Способ связи:'), md.text(data['connect']),
        #    sep='\n')
        #question = (md.text(md.bold('Заказчик:'), md.text(data['name']), md.text('Проект:', md.text(data['projected'])),
        #                    md.text('Способ связи:', data['connect']), sep='\n'))
        await message.answer(f"{q}{w}", reply_markup=poll_keyboard, parse_mode=types.ParseMode.MARKDOWN_V2)

    await Form.next()
#f"Данные введены верно? {question}"

#@dp.message_handler(state=Form.calldata)
@dp.message_handler(lambda message: message.text == "Да",state=Form.calldata)
async def action_yes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['calldata'] = message.text
        question = md.text(md.bold('Заказчик:'), md.text(data['name']), md.bold('Проект:'), md.text(data['projected']), md.bold('Способ связи:'), md.text(data['connect']),sep='\n')
        remove_keyboard = types.ReplyKeyboardRemove()
        await bot.send_message(-1001830422328, f"{question}", parse_mode=types.ParseMode.MARKDOWN_V2)
        await state.finish()
    
    await message.reply("Отправляю в канал!")
        

#@dp.message_handler(state=Form.calldata)
@dp.message_handler(lambda message: message.text == "Отмена",state=Form.calldata)
async def action_cancel(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['calldata'] = message.text
        remove_keyboard = types.ReplyKeyboardRemove()
        await message.answer(f"Упс, что-то пошло не так. Нажмите /reg")
    await state.finish()









if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
