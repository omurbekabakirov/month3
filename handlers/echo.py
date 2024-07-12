from aiogram import types, Dispatcher
from random import choice
from config import bot


async def echo(message: types.Message):
    text = message.text
    try:
        text_1=int(text)**2
        await message.answer(text=text_1)
    except Exception as e:
        ...
    if text == 'game':
        bot_1 = await bot.send_dice(chat_id=message.from_user.id, emoji='🎲')
        user = await bot.send_dice(chat_id=message.from_user.id, emoji='🎲')

        bot_choose = bot_1.dice.value
        user_choose = user.dice.value

        print(bot_choose, user_choose)

        if bot_choose > user_choose:
            await message.reply("Бот победил! 🤖")
        elif bot_choose < user_choose:
            await message.reply("Ты победил! 🎉")
        else:
            await message.reply("Ничья! 😐")
    else:
        await message.answer(text='no such a command')


def register_echo(dp: Dispatcher):
    dp.register_message_handler(echo, commands=['game'])
