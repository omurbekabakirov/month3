from aiogram import types, Dispatcher
from config import bot
import glob, random, os
from aiogram.types import InputFile


async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=f"Hi {message.from_user.first_name}")


async def mem(message: types.Message):
    path = 'media/'
    files = glob.glob(os.path.join(path, '*'))
    random_photo = random.choice(files)
    await bot.send_photo(chat_id=message.from_user.id, photo=InputFile(random_photo))


async def files(message: types.Message):
    path = 'files/'
    file = glob.glob(os.path.join(path, '*'))
    random_file = random.choice(file)
    await bot.send_audio(chat_id=message.from_user.id, audio=InputFile(random_file))


def register_commands(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'начало'])
    dp.register_message_handler(mem, commands=['mem', 'мем'])
    dp.register_message_handler(files, commands=['file'])
