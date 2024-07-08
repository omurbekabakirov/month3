from aiogram import types, Dispatcher
from random import choice
from config import bot


async def echo(message: types.Message):
    try:
        if type(int(message.text)) is int:
            await message.answer(text=int(message.text) ** 2)
    except Exception:
        pass
    if message.text == 'game':
        games = ['⚽', '🎰', '🏀', '🎯', '🎳', '🎲']
        await bot.send_dice(chat_id=message.from_user.id, emoji=choice(games))
        #dop-dz
        # bot_1 = await bot.send_dice(chat_id=message.from_user.id, emoji='🎲')
        # user = await bot.send_dice(chat_id=message.from_user.id, emoji='🎲')
        # if bot_1 > user:
        #     await message.answer(text='bot won'):
        # elif bot_1 < user:
        #     await message.answer(text='user won')
        # else:
        #     await message.answer(text='draw')
    else:
        await message.answer(text='no such a command')


def register_commands(dp: Dispatcher):
    dp.register_message_handler(echo)
