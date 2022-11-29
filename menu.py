import markups
import logging
import sqlite3
import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.message import ContentTypes
from aiogram.types import Message

import config as cfg
import markups as nav

ADMIN = 2121518774 # ваш user-id. Узнать можно тут @getmyid_bot

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot, storage=storage)

conn = sqlite3.connect('db.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   user_id INTEGER,
   block INTEGER);
""")
conn.commit()

class dialog(StatesGroup):
    spam = State()
    blacklist = State()
    whitelist = State()

@dp.message_handler(commands=['start'])
async def start(message: Message):
    cur = conn.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
    result = cur.fetchone()
    if message.from_user.id == ADMIN:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        await message.answer('Добро пожаловать в Админ-Панель!', reply_markup=keyboard)  #приветственное сообщение если админ
    else:
            await message.answer('Привет!'.format(message.from_user), reply_markup = nav.RegistrationMenu)  #приветственное сообщение если не админ


@dp.message_handler(content_types=['text'], text='Рассылка')
async def spam(message: Message):
    if message.from_user.id == ADMIN:
        await dialog.spam.set()
        await message.answer('Напиши текст рассылки')
    else:
        await message.answer('Вы не являетесь админом')


@dp.message_handler(state=dialog.spam)
async def start_spam(message: Message, state: FSMContext):
    if message.text == 'Назад':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        await message.answer('Главное меню', reply_markup=keyboard)
        await state.finish()
    else:
        cur = conn.cursor()
        cur.execute(f'''SELECT user_id FROM users''')
        spam_base = cur.fetchall()
        print(spam_base)
        for z in range(len(spam_base)):
            print(spam_base[z][0])
        for z in range(len(spam_base)):
            await bot.send_message(spam_base[z][0], message.text)
        await message.answer('Рассылка завершена')
        await state.finish()


@dp.message_handler(state='*', text='Назад')
async def back(message: Message):
    if message.from_user.id == ADMIN:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        await message.answer('Главное меню', reply_markup=keyboard)
    else:
        await message.answer('Вам не доступна эта функция')

@dp.message_handler()
async def start(message: types.Message):
    if message.text=="Прайс лист":
        await bot.send_message(message.from_user.id, ' ')
    elif message.text=="Информация":
        await bot.send_message(message.from_user.id, ' ')
    elif message.text=="Главное меню":
        await bot.send_message(message.from_user.id, 'Главное меню', reply_markup = nav.mainMenu)
    elif message.text=="Другое":
        await bot.send_message(message.from_user.id, 'Другое', reply_markup = nav.otherMenu)
    else:
        await message.reply('Неизвестная команда')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)