from aiogram.types import reply_keyboard

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, CallbackQuery
from aiogram.utils import executor
import aiogram.utils.markdown as md
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardRemove



logging.basicConfig(level=logging.INFO)

from config import TOKEN, chtid
#from config import chtid


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

HELP_COMMAND = """
/start - Начать работу с ботом
/help - Помощь
/description - описание бота
/reg - регистрация заявки
/channel - Наш канал
"""

class Form(StatesGroup):

    find = State()
    job = State()
    req = State()
    contact = State()
    check = State()
    approve = State()

    @staticmethod
    async def finish():
        pass

    async def reset_state(data=None):
        await Form.finish()
        return await Form.first()

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


# Handler to start the conversation
@dp.message_handler(commands='reg')
async def cmd_start(message: types.Message):
    await message.answer("Кого вы ищете?")
    await Form.find.set()


# Handler to handle the name state
@dp.message_handler(state=Form.find)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['find'] = message.text
    await message.answer("Опишите требования к вакансии")
    await Form.next()


# Handler to handle the job state
@dp.message_handler(state=Form.job)
async def process_job(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['job'] = message.text
    await message.answer("Опишите условия работы")
    await Form.next()

@dp.message_handler(state=Form.req)
async def process_req(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['req'] = message.text
    await message.answer("Как с вами связаться? Укажите почту или telegram_id")
    await Form.next()

@dp.message_handler(state=Form.contact)
async def process_contact(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['contact'] = message.text
        position = md.text(md.bold('Позиция: '), md.text(data['find']))
        requirements = md.text(md.bold('Требования: '), md.text(data['job']))
        conditions = md.text(md.bold('Условия: '), md.text(data['req']))
        contacts = md.text(md.bold('Контакты: '), md.text(data['contact']))
        urlkb = InlineKeyboardMarkup(row_width=2)
        yes_button = InlineKeyboardButton(text='Да', callback_data="yes")
        no_button = InlineKeyboardButton(text='Нет', callback_data="no")
        urlkb.add(yes_button, no_button)
        await message.answer(
            f"Данные введены верно?\n{position}\n{requirements}\n{conditions}\n{contacts}",
            reply_markup=urlkb, parse_mode=types.ParseMode.MARKDOWN_V2
        )
        await Form.next()


# Handler to handle the contact state and send the message to the admin
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('yes'),state=Form.check)
async def process_check(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        #data['check'] = message.text
        await callback.message.answer(f"Заявка отправлена на модерацию")
        # Sending message to the admin
        bak = md.text(md.bold('ВАКАНСИЯ:'))
        position = md.text(md.bold('Позиция: '), md.text(data['find']))
        requirements = md.text(md.bold('Требования: '), md.text(data['job']))
        conditions = md.text(md.bold('Условия: '), md.text(data['req']))
        contacts = md.text(md.bold('Контакты: '), md.text(data['contact']))

        #text = md.text(bak, '\n\n', position, '\n\n', requirements, '\n\n', conditions, '\n\n', contacts)



        await bot.send_message(chat_id=chtid, text=f"{bak}\n\n{position}\n\n{requirements}\n\n{conditions}\n\n{contacts}",
                               parse_mode=types.ParseMode.MARKDOWN_V2,
                               reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                   [
                                       types.InlineKeyboardButton(text="Aprove", callback_data="approve"),
                                       types.InlineKeyboardButton(text="Not", callback_data="not_approve"),

                                   ]
                               ]))
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                            reply_markup=None)
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'no',state=Form.check)
async def process_no(callback: types.CallbackQuery):
    await callback.message.answer(f"Введите данные заново:\n"
                                                       f"Кого вы ищете?")
    await Form.first()




@dp.callback_query_handler(lambda c: c.data and c.data.startswith('approve'))
async def process_callback_approve(callback_query: types.CallbackQuery, state: FSMContext):
    # Get data from callback

    data = callback_query.data
    message_id = callback_query.message.message_id



    # Get message from the admin chat
    message = await bot.send_message(chat_id='-1001830422328',
                                        text=callback_query.message.text,
                                        parse_mode=types.ParseMode.MARKDOWN_V2
                                                  )

    # Edit original message to indicate success
    await bot.edit_message_text(text=f"{callback_query.message.text}\n\nСообщение отправлено в канал",chat_id=callback_query.message.chat.id,parse_mode=types.ParseMode.MARKDOWN_V2,
                                message_id=message_id)
    #await bot.send_message(chat_id=chtid,text=callback_query.message.text)
    await state.finish()
    #await Form.first()




# Handler to handle the not approve button press
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('not_approve'))
async def process_callback_not_approve(callback_query: types.CallbackQuery,state: FSMContext):
    #data = callback_query.data
    message_id = callback_query.data
    await bot.send_message(chat_id=callback_query.message.chat.id,
                           text=f"{callback_query.message.text}\n\nСообщение отменено!",
                           reply_to_message_id=callback_query.message.message_id)
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id, reply_markup=None)
    await state.finish()
    #await Form.first()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)