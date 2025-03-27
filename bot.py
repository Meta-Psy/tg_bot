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
        bot.delete_message(chat_id, message.id)
        text = '📥 Корзина: \n\n'
        count = 0
        cart = get_prod_cart(chat_id)
        tot_price = 0
        for product in cart:
            count += 1
            pr_id = product[0]
            product_info = get_product(pr_id)
            pr_name = product_info[1]
            quantity = product[1]
            price = product_info[3]
            text += (f'{count}. {pr_name}\n'
                     f'{quantity} x {price} = {price * quantity}\n\n')
            tot_price += price * quantity
        text += f'\n\nИтого: {tot_price}'
        bot.send_message(chat_id, text, reply_markup=redact_cart_bt(cart))
    elif message.text == 'Назад':
        bot.delete_message(chat_id, message.id)
        bot.register_next_step_handler(message, start)
    elif message.text == 'Оформить заказ':
        bot.delete_message(chat_id, message.id)
        text = '📥 Поступил новый заказ: \n\n'
        count = 0
        cart = get_prod_cart(chat_id)
        tot_price = 0
        for product in cart:
            count += 1
            pr_id = product[0]
            product_info = get_product(pr_id)
            pr_name = product_info[1]
            quantity = product[1]
            price = product_info[3]
            text += (f'{count}. {pr_name}\n'
                     f'{quantity} x {price} = {price * quantity}\n\n')
            tot_price += price * quantity
        text += f'\n\nИтого: {tot_price}'
        bot.send_message(-4711046085, text)
        bot.send_message(chat_id, 'Заказ успешно оформлен. Ожидайте')
        clear_cart(chat_id)
    elif message.text == 'Очистить корзину':
        clear_cart(chat_id)
        products = get_products()
        bot.send_message(chat_id, 'Ваша корзина очищена.\n'
                                       'Хотели бы что-то заказать?', reply_markup=products_bt(products))




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
        prod_id = users[chat_id]['pr_id']
        product = get_product(prod_id)
        quantity = product[5]
        if quantity > 0:
            users[chat_id]['pr_quantity'] += 1
            count = users[chat_id]['pr_quantity']
            quantity -= 1
            change_product(quantity, prod_id)
            bot.edit_message_reply_markup(chat_id, message_id=call.message.id, reply_markup=cart_bt(count=count))
        else:
            count = users[chat_id]['pr_quantity']
            bot.send_message(chat_id, 'Больше на складе не осталось продуктов', reply_markup=cart_bt(count=count))
    elif call.data == 'minus':
        if users[chat_id]['pr_quantity'] > 1:
            users[chat_id]['pr_quantity'] -= 1
            count = users[chat_id]['pr_quantity']
            bot.edit_message_reply_markup(chat_id, message_id=call.message.id, reply_markup=cart_bt(count=count))
    elif call.data == 'cart':
        bot.delete_message(chat_id, call.message.id)
        text = '📥 Корзина: \n\n'
        count = 0
        cart = get_prod_cart(chat_id)
        tot_price = 0
        for product in cart:
            count += 1
            pr_id = product[0]
            product_info = get_product(pr_id)
            pr_name = product_info[1]
            quantity = product[1]
            price = product_info[3]
            text += (f'{count}. {pr_name}\n'
                     f'{quantity} x {price} = {price*quantity}\n\n')
            tot_price += price * quantity
        text += f'\n\nИтого: {tot_price}'
        bot.send_message(chat_id, text, reply_markup=redact_cart_bt(cart))



@bot.callback_query_handler(lambda call: 'prod_' in call.data)
def prod_calls(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.id)
    product_id = call.data.replace('prod_', '')
    product = get_product(product_id)
    if product:
        quantity = product[5]
        if quantity > 0:
            users[chat_id] = {'pr_id': product[0], 'pr_quantity': 1, 'pr_price': product[3]}
            bot.send_photo(chat_id, photo=product[4], caption=f'{product[1]}\n'
                                                              f'{product[2]}\n'
                                                              f'Цена: {product[3]}\n', reply_markup=cart_bt())

@bot.callback_query_handler(lambda call: 'cartpr_' in call.data)
def cart_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.id
    pr_id = call.data.replace('cartpr_', '')
    del_prod_cart(chat_id, pr_id)
    text = '📥 Корзина: \n\n'
    count = 0
    cart = get_prod_cart(chat_id)
    tot_price = 0
    for product in cart:
        count += 1
        pr_id = product[0]
        product_info = get_product(pr_id)
        pr_name = product_info[1]
        quantity = product[1]
        price = product_info[3]
        text += (f'{count}. {pr_name}\n'
                 f'{quantity} x {price} = {price*quantity}\n\n')
        tot_price += price * quantity
    text += f'\n\nИтого: {tot_price}'
    bot.edit_message_text(text, chat_id, message_id, reply_markup=redact_cart_bt(cart))

@bot.callback_query_handler(lambda call: 'prplus_' in call.data)
def product_plus(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.id
    pr_id = call.data.replace('prplus_', '')
    quantity = get_product_cart(chat_id, pr_id)[0]
    quantity_pr = get_product(prod_id=pr_id)
    if quantity_pr[0] > 0:
        quantity += 1
        update_product_cart(quantity, chat_id, pr_id)
        text = '📥 Корзина: \n\n'
        count = 0
        cart = get_prod_cart(chat_id)
        tot_price = 0
        for product in cart:
            count += 1
            pr_id = product[0]
            product_info = get_product(pr_id)
            pr_name = product_info[1]
            quantity = product[1]
            price = product_info[3]
            total_price = product[2]
            text += (f'{count}. {pr_name}\n'
                     f'{quantity} x {price} = {price*quantity}\n\n')
            tot_price += price * quantity
        text += f'\n\nИтого: {tot_price}'
        bot.edit_message_text(text, chat_id, message_id, reply_markup=redact_cart_bt(cart))


@bot.callback_query_handler(lambda call: 'prminus_' in call.data)
def product_plus(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.id
    pr_id = call.data.replace('prminus_', '')
    quantity = get_product_cart(chat_id, pr_id)[0]
    if quantity > 1:
        quantity -= 1
        update_product_cart(quantity, chat_id, pr_id)
        text = '📥 Корзина: \n\n'
        count = 0
        cart = get_prod_cart(chat_id)
        tot_price = 0
        for product in cart:
            count += 1
            pr_id = product[0]
            product_info = get_product(pr_id)
            pr_name = product_info[1]
            quantity = product[1]
            price = product_info[3]
            text += (f'{count}. {pr_name}\n'
                     f'{quantity} x {price} = {price*quantity}\n\n')
            tot_price += price*quantity
        text += f'\n\nИтого: {tot_price}'
        bot.edit_message_text(text, chat_id, message_id, reply_markup=redact_cart_bt(cart))

bot.infinity_polling()
