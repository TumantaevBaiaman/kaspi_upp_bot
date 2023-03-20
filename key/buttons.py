from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton

b1 = KeyboardButton('обновить данные')
b2 = KeyboardButton('новые данные')

menu_info = ReplyKeyboardMarkup(resize_keyboard=True)
menu_info.add(b1)