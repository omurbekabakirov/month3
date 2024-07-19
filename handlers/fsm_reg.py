from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import buttons


class RegisterUSer(StatesGroup):
    full_name = State()
    age = State()
    address = State()
    phone_number = State()
    email = State()
    photo = State()
    submit = State()


async def fsm_start(message: types.Message):
    await RegisterUSer.full_name.set()
    await message.answer(text='enter your full name 👇', reply_markup=buttons.cancel)


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['full_name'] = message.text

    await RegisterUSer.next()
    await message.answer(text='enter your age 👇')


async def load_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text

    await RegisterUSer.next()
    await message.answer(text='enter your phone number 👇')


async def load_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text

    await RegisterUSer.next()
    await message.answer(text='enter your address 👇')


async def load_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text

    await RegisterUSer.next()
    await message.answer(text='send your email 👇')


async def load_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text

    await RegisterUSer.next()
    await message.answer(text='send your photo 👇')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    keyword = InlineKeyboardMarkup(row_width=2)
    yes_button = InlineKeyboardButton(text='yes', callback_data='yes')
    no_button = InlineKeyboardButton(text='no', callback_data='no')
    keyword.add(yes_button, no_button)

    await RegisterUSer.next()
    await message.answer(text='<b>Do you want to submit ?</b>', parse_mode=types.ParseMode.HTML)
    await message.answer_photo(photo=data['photo'],
                               caption=f'full_name - {data["full_name"]}\n'
                                       f'age - {data["age"]}\n'
                                       f'address - {data["address"]}\n'
                                       f'phone_number - {data["phone_number"]}\n'
                                       f'email - {data["email"]}',
                                       reply_markup=keyword)


async def submit(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'yes':
        await callback_query.message.answer(text='good job')
        await state.finish()
    elif callback_query.data == 'no':
        await callback_query.message.answer(text='Canceled', reply_markup=buttons.start_buttons)
        await state.finish()
    else:
        await callback_query.message.answer(text='press on the button')


async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer(text='canceled')


def register_fsm_fpr_user(dp: Dispatcher):
    dp.register_message_handler(cancel, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(fsm_start, commands=['registration'])
    dp.register_message_handler(load_name, state=RegisterUSer.full_name)
    dp.register_message_handler(load_age, state=RegisterUSer.age)
    dp.register_message_handler(load_address, state=RegisterUSer.address)
    dp.register_message_handler(load_phone_number, state=RegisterUSer.phone_number)
    dp.register_message_handler(load_email, state=RegisterUSer.email)
    dp.register_message_handler(load_photo, state=RegisterUSer.photo, content_types=['photo'])
    dp.register_callback_query_handler(submit, state=RegisterUSer.submit)
