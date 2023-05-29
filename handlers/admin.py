import asyncio

from aiogram import types, Dispatcher
from create_bot import dp, bot
from sheets_settings import read_sheets, new_data_price, update, add_new_data, new_data_sku
from aiogram.dispatcher.filters import Text
from key.buttons import menu_info
from config import AUTHORIZED_USER_ID


async def base_commands(message: types.Message):
    if str(message.from_user.id) in AUTHORIZED_USER_ID:
        await bot.send_message(message.from_user.id, 'Welcome', reply_markup=menu_info)
    else:
        await bot.send_message(chat_id=message.from_user.id, text="Sorry, you are not authorized to use this bot.")


async def update_google_sheets(message: types.Message):
    if str(message.from_user.id) in AUTHORIZED_USER_ID:
        await bot.send_message(message.from_user.id, 'Немного подождите')
        name_excel, price_excel = await read_sheets()
        await add_new_data(name_excel, price_excel)
        name_excel, price_excel = await read_sheets()
        new_sku = await new_data_sku(name_excel, price_excel)
        await update(new_sku)
        await bot.send_message(message.from_user.id, 'Данные были обновлены')
    else:
        await bot.send_message(chat_id=message.from_user.id, text="Sorry, you are not authorized to use this bot.")


async def new_data(message: types.Message):
    await bot.send_document(chat_id=message.from_user.id, document=open('new_sku_data.xlsx', 'rb'))


def register_admin(dp : Dispatcher):
    dp.register_message_handler(base_commands, commands=['start'])
    dp.register_message_handler(update_google_sheets, Text(equals='обновить данные', ignore_case=True))
    dp.register_message_handler(new_data, Text(equals='новые данные', ignore_case=True))