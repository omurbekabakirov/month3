from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import buttons
from database.db import Database


class RegisterUSer(StatesGroup):
    model_name = State()
    size = State()
    category = State()
    price = State()
    photo = State()
    submit = State()


async def fsm_start(message: types.Message):
    await RegisterUSer.model_name.set()
    await message.answer(text='enter name of the model 👇', reply_markup=buttons.cancel)


async def load_model_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['model_name'] = message.text

    await RegisterUSer.next()
    await message.answer(text='enter size of the model 👇')


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await RegisterUSer.next()
    await message.answer(text='enter category of the model👇')


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await RegisterUSer.next()
    await message.answer(text='enter price of the model 👇')


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await RegisterUSer.next()
    await message.answer(text='send photo of the model 👇')


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
                               caption=f'model_name - {data["model_name"]}\n'
                                       f'size - {data["size"]}\n'
                                       f'category - {data["category"]}\n'
                                       f'price - {data["price"]}\n',
                                       reply_markup=keyword)

    datab = Database()
    path = await message.photo[-1].download(destination_dir='media_destination/')
    async with state.proxy() as data:
        datab.insert_model(
            tg_id=message.from_user.id,
            model_name=data['model_name'],
            category=data['category'],
            price=data['price'],
            photo=path.name
        )


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
    dp.register_message_handler(load_model_name, state=RegisterUSer.model_name)
    dp.register_message_handler(load_size, state=RegisterUSer.size)
    dp.register_message_handler(load_category, state=RegisterUSer.category)
    dp.register_message_handler(load_price, state=RegisterUSer.price)
    dp.register_message_handler(load_photo, state=RegisterUSer.photo, content_types=['photo'])
    dp.register_callback_query_handler(submit, state=RegisterUSer.submit)
