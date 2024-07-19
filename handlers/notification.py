from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
from config import bot
from apscheduler.triggers.cron import CronTrigger
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
users = [995712956, ]
notifications = []


class NotificationStates(StatesGroup):
    waiting_for_message = State()
    waiting_for_time = State()


async def send_notification(user_id, message):
    user = await bot.get_chat(user_id)
    firstname = user.first_name if user.first_name else "Пользователь"
    await bot.send_message(
        chat_id=user_id,
        text=f"🔔 Напоминание 🔔 \nДобрый день {firstname}! \nНе забудьте про - {message}"
    )


async def set_scheduler():
    scheduler = AsyncIOScheduler(timezone="Asia/Bishkek")
    scheduler.start()


async def handle_notification_command(message: types.Message):
    await message.reply("Введите сообщение для уведомления:")
    await NotificationStates.waiting_for_message.set()


async def handle_notification_text(message: types.Message, state: FSMContext):
    await state.update_data(notification_message=message.text)
    await message.reply("Введите время для уведомления в формате HH:MM (например, 22:36):")
    await NotificationStates.waiting_for_time.set()


async def handle_notification_time(message: types.Message, state: FSMContext):
    try:
        notification_time = datetime.datetime.strptime(message.text, "%H:%M").time()
        user_data = await state.get_data()
        notification_message = user_data['notification_message']
        notifications.append(
            {'message': notification_message, 'time': notification_time, 'user_id': message.from_user.id})

        scheduler = AsyncIOScheduler(timezone="Asia/Bishkek")
        scheduler.add_job(
            send_notification,
            CronTrigger(hour=notification_time.hour, minute=notification_time.minute),
            args=[message.from_user.id, notification_message]
        )
        scheduler.start()

        await message.reply(
            f"Сообщение '{notification_message}' добавлено в список уведомлений на {notification_time}.")
    except ValueError:
        await message.reply("Неверный формат времени. Пожалуйста, введите время в формате HH:MM (например, 22:36):")
        return

    await state.finish()


def register_notification(dp: Dispatcher):
    dp.register_message_handler(handle_notification_command, commands=['notification'], state='*')
    dp.register_message_handler(handle_notification_text, state=NotificationStates.waiting_for_message)
    dp.register_message_handler(handle_notification_time, state=NotificationStates.waiting_for_time)


scheduler = AsyncIOScheduler(timezone="Asia/Bishkek")
scheduler.start()