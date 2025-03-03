import telebot
from telebot.types import Message
from buttons import *
from database import *
from geopy import Photon



bot = telebot.TeleBot(token='7460808784:AAH-AVWMVr05NfNx41ASgrB-4KZLR56l7sA')
geolocation = Photon(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36')


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if check_regist(chat_id):
        bot.send_message(chat_id, 'Пожалуйста, нажмите кнопку ниже, чтобы заказать свой продукт',
                         reply_markup=hello_bt())
        bot.register_next_step_handler(message, main_menu)
    else:
        bot.send_message(chat_id, 'Добро пожаловать в бот KFC. Так как вы у нас в первый раз, вам необходимо пройти регистрацию')
        bot.send_message(chat_id, 'Отправьте своё имя')
        bot.register_next_step_handler(message, get_name)


def get_name(message):
    chat_id = message.chat.id
    name = message.text
    bot.send_message(chat_id, 'Отправьте пожалуйста ваш телефон, через кнопку в меню',
                     reply_markup=get_telephone_bt())
    bot.register_next_step_handler(message, get_location, name)


def get_location(message, name):
    user_phone = message.contact.phone_number
    chat_id = message.chat.id
    bot.send_message(chat_id, text='Отправьте пожалуйста вашу локацию, через кнопку в меню',
                     reply_markup=get_location_bt())
    bot.register_next_step_handler(message, finish_registration, name, user_phone)


def finish_registration(message: Message, name, user_phone):
    latitude = message.location.latitude
    longitude = message.location.longitude
    address = geolocation.reverse((latitude, longitude)).address
    user_regist(name, user_phone, address)
    bot.register_next_step_handler(message, start)


def main_menu(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Главное меню: ', main_menu_bt())
    bot.register_next_step_handler(message, user_choose)

def user_choose(message: Message):
    chat_id = message.chat.id
    if message.text == 'Корзина':
        bot.register_next_step_handler(message, cart)
    elif message.text == 'Еда':
        bot.register_next_step_handler(message, food)
    elif message.text == 'Назад':
        bot.register_next_step_handler(message, back)


bot.infinity_polling()
