from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def hello_bt():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    begin = KeyboardButton('Заказать')
    kb.add(begin)
    return kb


def get_telephone_bt():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    get_telephone_bt = KeyboardButton('Отправить телефон', request_contact=True)
    kb.add(get_telephone_bt)
    return kb


def get_location_bt():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    get_location_bt = KeyboardButton('Отправить локацию', request_location=True)
    kb.add(get_location_bt)
    return kb

def main_menu_bt():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    cart_bt = KeyboardButton('Корзина')
    products_bt = KeyboardButton('Еда')
    back_bt = KeyboardButton('Назад')
    kb.add(cart_bt, products_bt)
    kb.row(back_bt)
    return kb
