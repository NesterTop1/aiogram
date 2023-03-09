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

from keyboards.default.main_menu import main_menu

from loader import dp, db, bot

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardRemove
from data.config import TOKEN, ADMINS, CHANNEL_ID
#from keyboards.default.main_menu import main_menu


def convert_markdown(find, job, req, contact, converted_data={}):
    converted_data['bak'] = md.text(md.bold('ВАКАНСИЯ:'))
    converted_data['position'] = md.text(md.bold('Позиция: '), md.text(find))
    converted_data['requirements'] = md.text(md.bold('Требования: '), md.text(job))
    converted_data['conditions'] = md.text(md.bold('Условия: '), md.text(req))
    converted_data['contacts'] = md.text(md.bold('Контакты: '), md.text(contact))

    return f"{converted_data['bak']}\n\n" \
           f"{converted_data['position']}\n\n" \
           f"{converted_data['requirements']}\n\n" \
           f"{converted_data['conditions']}\n\n" \
           f"{converted_data['contacts']}" \


logging.basicConfig(level=logging.INFO)



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


# Handler to start the conversation
@dp.message_handler(commands='registration')
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
            reply_markup=urlkb, parse_mode=types.ParseMode.MARKDOWN
        )
        await Form.next()


# Handler to handle the contact state and send the message to the admin
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('yes'), state=Form.check)
async def process_check(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await callback.message.answer(f"Заявка отправлена на модерацию")
        # Sending message to the admin
        message = convert_markdown(data['find'],
                                   data['job'],
                                   data['req'],
                                   data['contact'])
        for admin in ADMINS:
            await bot.send_message(chat_id=int(admin),
                                   text=message,
                                   parse_mode=types.ParseMode.MARKDOWN,
                                   reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                       [
                                           types.InlineKeyboardButton(text="Approve", callback_data='approve'),
                                           types.InlineKeyboardButton(text="Reject", callback_data="reject"),
                                    ]
                                ]))
            await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                                message_id=callback.message.message_id,
                                                reply_markup=None)
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'no', state=Form.check)
async def process_no(callback: types.CallbackQuery):
    await callback.message.answer(f"Введите данные заново:\n"
                                  f"Кого вы ищете?")
    await Form.first()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('approve'))
async def process_callback_approve(callback_query: types.CallbackQuery, state: FSMContext):
    # Get data from callback
    data = []
    for i in callback_query.message.text.split('\n\n'):
        if len(i.split('  ')) == 1:
            pass
        else:
            data.append(i.split('  ')[1])

    message = convert_markdown(data[0], data[1], data[2], data[3])

    await bot.send_message(chat_id=CHANNEL_ID,
                           text=message,
                           parse_mode=types.ParseMode.MARKDOWN)

    # Edit original message to indicate success
    await bot.edit_message_text(text=f"{message}\n\nСообщение отправлено в канал",
                                chat_id=callback_query.message.chat.id, parse_mode=types.ParseMode.MARKDOWN,
                                message_id=callback_query.message.message_id)
    # await bot.send_message(chat_id=chtid,text=callback_query.message.text)
    await state.finish()
    # await Form.first()


# Handler to handle the not approve button press
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('reject'))
async def process_callback_not_approve(callback_query: types.CallbackQuery, state: FSMContext):
    # data = callback_query.data
    message_id = callback_query.data
    await bot.send_message(chat_id=callback_query.message.chat.id,
                           text=f"{callback_query.message.text}\n\nСообщение отменено!",
                           reply_to_message_id=callback_query.message.message_id)
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id, reply_markup=None)
    await state.finish()
    # await Form.first()

