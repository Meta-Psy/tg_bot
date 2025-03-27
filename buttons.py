from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_product

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


def cart_bt(count=1):
    kb = InlineKeyboardMarkup()
    minus = InlineKeyboardButton(text='➖', callback_data='minus')
    plus = InlineKeyboardButton(text='➕', callback_data='plus')
    count = InlineKeyboardButton(text=f'{count}', callback_data='count')
    add_to_cart = InlineKeyboardButton(text='Добавить в корзину', callback_data='add_to_cart')
    kb.add(minus, count, plus)
    kb.row(add_to_cart)
    return kb


def end_bt():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    back = KeyboardButton('Назад')
    btn2 = KeyboardButton('Оформить заказ')
    btn3 = KeyboardButton('Очистить')
    kb.add(back, btn2)
    kb.row(btn3)
    return kb


def redact_cart_bt(cart):
    kb = InlineKeyboardMarkup()
    count = 0
    for product in cart:
        count += 1
        pr_id = product[0]
        product_info = get_product(pr_id)
        pr_name = product_info[1]
        quantity = product[1]
        prod_bt = InlineKeyboardButton(text=f'❌ {count}. {pr_name}', callback_data=f'cartpr_{pr_id}')
        prod_plus = InlineKeyboardButton(text='➕', callback_data=f'prplus_{pr_id}')
        prod_minus = InlineKeyboardButton(text='➖', callback_data=f'prminus_{pr_id}')
        prod_quantity = InlineKeyboardButton(text=f'{quantity}', callback_data='prod_quantity')
        kb.add(prod_bt)
        kb.row(prod_minus, prod_quantity, prod_plus)
    return kb
