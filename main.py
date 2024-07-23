from config import dp, bot, Admin
from aiogram.utils import executor
import logging
from handlers import comands, echo, quiz, fsm_reg, send_products, notification, fsm_online_store, webapp, admin_group
from database import db


async def on_startup(_):
    for i in Admin:
        await bot.send_message(chat_id=i, text='bot started')
        await db.create_table()


async def on_shutdown(_):
    for i in Admin:
        await bot.send_message(chat_id=i, text='bot stopped')


comands.register_commands(dp=dp)
quiz.register_quiz(dp=dp)
fsm_reg.register_fsm_fpr_user(dp=dp)
fsm_online_store.register_fsm_store(dp=dp)
send_products.register_send_products(dp=dp)
notification.register_notification(dp=dp)
webapp.register_webapp(dp=dp)
admin_group.register_admin_group(dp=dp)
# this is echo function you must call it only at the end
echo.register_echo(dp=dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
