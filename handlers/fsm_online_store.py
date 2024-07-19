from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import buttons
from database import db


class Store(StatesGroup):
    name_product = State()
    size = State()
    price = State()
    productid = State()
    category = State()
    info_product = State()
    collection = State()
    photo = State()
    submit = State()


async def fsm_start(message: types.Message):
    await Store.name_product.set()
    await message.answer(text="Введите название товара:", reply_markup=buttons.cancel)


async def load_name_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_product'] = message.text

    await Store.next()
    await message.answer(text='Введите размер одежды')


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await Store.next()
    await message.answer(text='Введите цену товара: ')


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await Store.next()
    await message.answer(text='Введите артикул: ')


async def load_productid(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['productid'] = message.text

    await Store.next()
    await message.answer(text='Write a category for product:')


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await Store.next()
    await message.answer(text='Write info for product:')


async def load_info_for_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['info_product'] = message.text

    await Store.next()
    await message.answer(text='send a collection for product:', reply_markup=kb)


async def load_collection(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['collection'] = message.text

    await Store.next()
    kb = types.ReplyKeyboardRemove()
    await message.answer(text='send a photo for product:', reply_markup=kb)


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    keyboard = ReplyKeyboardMarkup(row_width=2)
    keyboard.add(KeyboardButton('Да'), KeyboardButton('Нет'))

    await Store.next()
    await message.answer_photo(photo=data['photo'],
                               caption=f"Название - {data['name_product']}\n"
                                       f"Размер - {data['size']}\n"
                                       f"Цена - {data['price']}\n"
                                       f"Артикул - {data['productid']}\n"
                                       f"Category - {data['category']}\n"
                                       f"Info - {data['info_product']}\n"
                                       f"<b>Верные ли данные ?</b>",
                               reply_markup=keyboard, parse_mode=types.ParseMode.HTML)


async def submit(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        async with state.proxy() as data:
            await db.sql_insert(
                name_product=data['name_product'],
                size=data['size'],
                price=data['price'],
                product_id=data['product_id'],
                photo=data['photo']
            )

            await db.sql_insert_details(
                product_id=data['product_id'],
                category=data['category'],
                infoproduct=data['info_product']
            )

            await db.sql_insert_collection(
                product_id=data['product_id'],
                collection=data['collection']
            )
            await message.answer('Отлично! Регистрация пройдена.', reply_markup=buttons.start_buttons)
            await state.finish()
    elif message.text == 'Нет':
        await message.answer('Отменено!', reply_markup=buttons.start_buttons)
        await state.finish()

    else:
        await message.answer(text='Нажмите на кнопку!')


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer(text='Отменено')


# Finite State Machine
def register_fsm_store(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена',
                                                 ignore_case=True), state='*')
    dp.register_message_handler(fsm_start, commands=['store'])
    dp.register_message_handler(load_name_product, state=Store.name_product)
    dp.register_message_handler(load_size, state=Store.size)
    dp.register_message_handler(load_price, state=Store.price)
    dp.register_message_handler(load_productid, state=Store.productid)
    dp.register_message_handler(load_category, state=Store.category)
    dp.register_message_handler(load_info_for_product, state=Store.info_product)
    dp.register_message_handler(load_collection, state=Store.collection)
    dp.register_message_handler(load_photo, state=Store.photo, content_types=['photo'])
    dp.register_message_handler(submit, state=Store.submit)
