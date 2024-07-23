from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import dp


async def webapp_reply(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(KeyboardButton('Anime Go', web_app=types.WebAppInfo(url='https://animego.org')),
                 KeyboardButton('Jut Su', web_app=types.WebAppInfo(url='https://jut.su')),
                 KeyboardButton('Manga lib',
                                web_app=types.WebAppInfo(url='https://mangalib.org/true-education?section=info')),
                 KeyboardButton('Lalafo', web_app=types.WebAppInfo(url='https://lalafo.kg')),
                 KeyboardButton('Youtube', web_app=types.WebAppInfo(url='https://www.youtube.com')))

    await message.answer('Нажми на кнопку ниже для перехода на сайты:', reply_markup=keyboard)


async def webapp_inline(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton('Anime Go', web_app=types.WebAppInfo(url='https://animego.org')),
                 InlineKeyboardButton('Jut Su', web_app=types.WebAppInfo(url='https://jut.su')),
                 InlineKeyboardButton('Lalafo', web_app=types.WebAppInfo(url='https://lalafo.kg')),
                 InlineKeyboardButton('Youtube', web_app=types.WebAppInfo(url='https://www.youtube.com')),
                 InlineKeyboardButton('Manga lib',
                                      web_app=types.WebAppInfo(url='https://mangalib.org/true-education?section=info')))

    await message.answer('Нажми на кнопку ниже для перехода на сайты:', reply_markup=keyboard)


def register_webapp(dp: Dispatcher):
    dp.register_message_handler(webapp_reply, commands=['web_reply'])
    dp.register_message_handler(webapp_inline, commands=['web_inline'])
