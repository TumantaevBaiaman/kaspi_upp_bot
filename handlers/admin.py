import asyncio

from aiogram import types, Dispatcher
from create_bot import dp, bot
from sheets_settings import read_sheets, new_data_price, update, add_new_data
from aiogram.dispatcher.filters import Text
from key.buttons import menu_info


async def base_commands(message: types.Message):
    await bot.send_message(message.from_user.id, 'Welcome', reply_markup=menu_info)


async def update_google_sheets(message: types.Message):
    await bot.send_message(message.from_user.id, 'Немного подождите')
    name_excel, price_excel = await read_sheets()
    new_price = await new_data_price(name_excel, price_excel)
    await add_new_data(name_excel, price_excel)
    data = await update(new_price)
    if data:
        await bot.send_message(message.from_user.id, 'Новые данные')
        await bot.send_document(chat_id=message.from_user.id, document=open('new_sku_data.xlsx', 'rb'))
    await bot.send_message(message.from_user.id, 'Данные были обновлены')


async def new_data(message: types.Message):
    await bot.send_document(chat_id=message.from_user.id, document=open('new_sku_data.xlsx', 'rb'))


def register_admin(dp : Dispatcher):
    dp.register_message_handler(base_commands, commands=['start'])
    dp.register_message_handler(update_google_sheets, Text(equals='обновить данные', ignore_case=True))
    dp.register_message_handler(new_data, Text(equals='новые данные', ignore_case=True))