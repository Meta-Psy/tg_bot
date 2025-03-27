import telebot
from telebot.types import Message, CallbackQuery
from buttons import *
from database import *
from geopy import Photon

geolocation = Photon(timeout=5, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36')
bot = telebot.TeleBot(token='7460808784:AAH-AVWMVr05NfNx41ASgrB-4KZLR56l7sA')
users = {}


@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    if check_db(tg_id=chat_id):
        bot.send_message(chat_id, 'Добро пожаловать в KFC. Вот ваше главное меню: ',
                         reply_markup=main_menu_bt())
    else:
        bot.send_message(chat_id, 'Добро пожаловать в KFC!')
        bot.send_message(chat_id, 'Вы у нас впервые. Не могли бы вы пройти быструю регистрацию?. \n'
                                  'Отправьте свое имя')
        bot.register_next_step_handler(message, get_name)


def get_name(message: Message):
    chat_id = message.chat.id
    name = message.text
    bot.send_message(chat_id, 'Отправьте пожалуйста свой номер', reply_markup=get_number_bt())
    bot.register_next_step_handler(message, get_number, name)


def get_number(message: Message, name):
    chat_id = message.chat.id
    number = message.contact.phone_number
    bot.send_message(chat_id, 'Отправьте свою локацию', reply_markup=get_location_bt())
    bot.register_next_step_handler(message, get_location, name, number)


def get_location(message: Message, name, number):
    chat_id = message.chat.id
    longitude = message.location.longitude
    latitude = message.location.latitude
    address = geolocation.reverse((latitude, longitude)).address
    if registration_db(tg_id=chat_id, name=name, number=number, location=address):
        bot.send_message(chat_id, 'Поздравляем с успешной регистрацией!')
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(chat_id, 'Во время регистрации произошла ошибка')


@bot.message_handler(content_types=['text'])
def main_menu(message: Message):
    chat_id = message.chat.id
    if message.text == 'Заказать':
        products = get_products()
        bot.send_message(chat_id, 'С чего начнем?', reply_markup=products_bt(products))
    elif message.text == 'Корзина':
        pass
    elif message.text == 'Назад':
        pass


@bot.callback_query_handler(lambda call: call.data in ['back', 'cart', 'plus', 'minus', 'add_to_cart'])
def calls(call: CallbackQuery):
    chat_id = call.message.chat.id
    if call.data == 'back':
        bot.register_next_step_handler(call.message, main_menu)
        bot.delete_message(chat_id, call.message.id)
    elif call.data == 'add_to_cart':
        bot.delete_message(chat_id, call.message.id)
        pr_id = users[chat_id]['pr_id']
        quantity = users[chat_id]['pr_quantity']
        product = get_product(pr_id)
        price = product[3]
        name = product[1]
        products = get_products()
        add_to_cart_db(user_id=chat_id, pr_id=pr_id, quantity=quantity, total_price=quantity*price)
        bot.send_message(chat_id, f'Продукт {name} успешно добавлен в корзину ✅', reply_markup=end_bt())
        bot.send_message(chat_id, f'Продолжим или вы готовы оформить заказ?', reply_markup=products_bt(products))
    elif call.data == 'plus':
        users[chat_id]['pr_quantity'] += 1
        count = users[chat_id]['pr_quantity']
        bot.edit_message_reply_markup(chat_id, message_id=call.message.id, reply_markup=cart_bt(count=count))
    elif call.data == 'minus':
        users[chat_id]['pr_quantity'] -= 1
        count = users[chat_id]['pr_quantity']
        bot.edit_message_reply_markup(chat_id, message_id=call.message.id, reply_markup=cart_bt(count=count))
    elif call.data == 'cart':
        bot.delete_message(chat_id, call.message.id)
        text = '📥 Корзина:'
        count = 0
        cart = get_prod_cart(chat_id)
        for product in cart:
            count += 1
            pr_id = product[0]
            product_info = get_product(pr_id)
            pr_name = product_info[1]
            quantity = product[1]
            price = product_info[3]
            total_price = product[2]
            text += (f'{count}. {pr_name}\n'
                     f'{quantity} x {price} = {total_price}\n\n')
        bot.send_message(chat_id, text, reply_markup=redact_cart_bt(cart))



@bot.callback_query_handler(lambda call: 'prod_' in call.data)
def prod_calls(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.id)
    product_id = call.data.replace('prod_', '')
    product = get_product(product_id)
    users[chat_id] = {'pr_id': product[0], 'pr_quantity': 1, 'pr_price': product[3]}
    bot.send_photo(chat_id, photo=product[4], caption=f'{product[1]}\n'
                                                      f'{product[2]}\n'
                                                      f'Цена: {product[3]}\n', reply_markup=cart_bt())


@bot.callback_query_handler(lambda call: 'cartpr_' in call.data)
def cart_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.id
    pr_id = call.data.replace('cartpr_', '')
    cart = get_prod_cart(chat_id)
    del_prod_cart(chat_id, pr_id)
    bot.edit_message_reply_markup(chat_id, message_id, reply_markup=redact_cart_bt(cart))

bot.infinity_polling()
