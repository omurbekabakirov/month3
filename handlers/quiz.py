from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot

async def quiz(message: types.Message):
    button_quiz = InlineKeyboardMarkup()
    button_quiz_1 = InlineKeyboardButton("Next", callback_data="button_1")
    button_quiz.add(button_quiz_1)

    question = ' apple or banana ?'
    answers = ['apple', 'banana']

    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=True,
        type='quiz',
        correct_option_id=1,
        explanation='good choice',
        open_period=60,
        reply_markup=button_quiz
                        )


async def quiz2(call: types.CallbackQuery):
    button_quiz = InlineKeyboardMarkup()
    button_quiz_1 = InlineKeyboardButton("Next", callback_data="button_2")
    button_quiz.add(button_quiz_1)

    question = 'college or university'
    answers = ['college', 'university']

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answers,
        is_anonymous=True,
        type='quiz',
        correct_option_id=1,
        explanation='good choice',
        open_period=60,
        reply_markup=button_quiz
                        )


async def quiz3(call: types.CallbackQuery):
    button_quiz = InlineKeyboardMarkup()
    button_quiz_1 = InlineKeyboardButton("Next", callback_data="button_3")
    button_quiz.add(button_quiz_1)

    question = 'fuel car or electric car '
    answers = ['fuel car', 'electric car']

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answers,
        is_anonymous=True,
        type='quiz',
        correct_option_id=0,
        explanation='you are not gay',
        open_period=60,
        reply_markup=button_quiz
                        )


def register_quiz(dp: Dispatcher):
    dp.register_message_handler(quiz, commands=['quiz'])
    dp.register_callback_query_handler(quiz2, lambda call: call.data == 'button_1')
    dp.register_callback_query_handler(quiz3, lambda call: call.data == 'button_2')
