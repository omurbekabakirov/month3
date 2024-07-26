from google_sheets.config_sheets import service, google_sheet_id_users
from aiogram import types, Dispatcher


def update_google_sheet_products(name_product, size, price, productid, category, infoproduct, collection):
    try:
        range_name = 'Лист2!A:G'
        row = [name_product, size, price, productid, category, infoproduct, collection]
        service.spreadsheets().values().append(
            spreadsheetId=google_sheet_id_users,
            range=range_name,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': [row]}
        ).execute()
        print(f'Data - {row}')
    except Exception as e:
        print(f'Error - {e}')


def get_data():
    try:
        range_name = 'Лист2!A:G'
        result = service.spreadsheets().values().get(
            spreadsheetId=google_sheet_id_users,
            range=range_name,
        ).execute()
        rows = result.get('values', [])
        return rows
    except Exception as e:
        print(f'Error - {e}')
        return []


async def send_data(message: types.Message):
    data = get_data()

    if not data:
        await message.reply('Таблица пуста!')

    else:
        headers = data[0]
        response = 'Данные из Google Таблиц:\n\n'
        for row in data[1:]:
            for header, value in zip(headers, row):
                response += f"{header}: {value}\n"
            response += "\n"
        await message.reply(response)


def register_g_sheets(dp: Dispatcher):
    dp.register_message_handler(send_data, commands=['send_data'])
