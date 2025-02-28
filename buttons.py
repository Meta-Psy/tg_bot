from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def hello_bt():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    begin = KeyboardButton('Заказать')
    kb.add(begin)
    return kb

def get_telephone():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    get_telephone_bt = KeyboardButton('Отправить телефон', request_contact=True)
    kb.add(get_telephone_bt)
    return kb

