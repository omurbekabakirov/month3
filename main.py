from config import dp, bot, Admin
from aiogram.utils import executor
import logging
from handlers import comands, echo, quiz

async def on_startup(_):
    for i in Admin:
        await bot.send_message(chat_id=i, text='bot started')


async def on_shutdown(_):
    for i in Admin:
        await bot.send_message(chat_id=i, text='bot stoped')

comands.register_commands(dp)
quiz.register_quiz(dp)

#this is echo function you must call it only at the end
echo.register_commands(dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
