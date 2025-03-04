from telebot.types import ReplyKeyboardMarkup, KeyboardButton


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
