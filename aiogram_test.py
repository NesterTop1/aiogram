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


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['name'] = message.text

    await Form.next()
    await message.reply("Опишите ваш проект")


# Check age. Age gotta be digit
#@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.connect)
#async def process_age_invalid(message: types.Message):
#    """
#    If age is invalid
#    """
#    return await message.reply("Age gotta be a number.\nHow old are you? (digits only)")


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
        question = md.bold('Заказчик:'), md.text(data['name']), sep='\n', md.text('Проект:'), md.text(data['projected']),md.bold('Способ связи:'), md.text(data['connect'])
        await message.answer(f"Данные введены верно? {question}" , reply_markup=poll_keyboard)

    await Form.next()

#@dp.message_handler(state=Form.calldata)
@dp.message_handler(lambda message: message.text == "Да",state=Form.calldata)
async def action_yes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['calldata'] = message.text
        question = (md.text(md.text('Заказчик:', md.text(data['name'])), md.text('Проект:', md.text(data['projected'])),
                            md.text('Способ связи:', data['connect']), sep='\n'))
        remove_keyboard = types.ReplyKeyboardRemove()
        await bot.send_message(-1001830422328, f"{question}")
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


#@dp.message_handler(state=Form.connect)


#dp.message_handler(state=Form.connect)
#@dp.message_handler(filters.Text("Да", ignore_case=True), state=Form.connect)
#async def with_puree(message: types.Message, state: FSMContext, callback: types.CallbackQuery):
#    async with state.proxy() as data:
#        data['connect'] = message.text
#    await message.reply("Отправляю в канал")
#    await bot.send_message(
#             -1001830422328,
#             md.text(
#                 md.text('Заказчик', md.bold(data['name'])),
#                 md.text('Проект', md.bold(data['projected'])),
#                 md.text('Способ связи:', data['connect']),
#                 sep='\n',
#                 )
#                 )






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
