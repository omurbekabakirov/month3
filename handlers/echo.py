from aiogram import types, Dispatcher


async def echo(message: types.Message):
    try:
        text = int(message.text) ** 2
        await message.answer(text=text)
    except Exception:
        await message.answer(text='no such a command')


def register_commands(dp: Dispatcher):
    dp.register_message_handler(echo)