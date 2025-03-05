from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_number_bt():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('Отправить номер', request_contact=True)
    kb.add(btn1)
    return kb


def get_location_bt():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('Отправить локацию', request_location=True)
    kb.add(btn1)
    return kb


def main_menu_bt():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('Заказать')
    btn2 = KeyboardButton('Корзина')
    btn3 = KeyboardButton('Назад')
    kb.row(btn1, btn2)
    kb.row(btn3)
    return kb


def products_bt(products):
    kb = InlineKeyboardMarkup(row_width=2)
    back = InlineKeyboardButton(text='Назад', callback_data='back')
    cart = InlineKeyboardButton(text='Корзина', callback_data='cart')
    products = [InlineKeyboardButton(text=f'{product[1]}', callback_data=f'prod_{product[0]}')
                for product in products]
    kb.add(*products)
    kb.row(cart)
    kb.row(back)
    return kb

