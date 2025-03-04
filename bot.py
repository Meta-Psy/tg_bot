import telebot
from telebot.types import Message
from buttons import *
from database import *
from geopy import Photon

geolocation = Photon(timeout=5, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36')
bot = telebot.TeleBot(token='7460808784:AAH-AVWMVr05NfNx41ASgrB-4KZLR56l7sA')


@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    if check_db(tg_id=chat_id):
        bot.send_message(chat_id, 'Добро пожаловать в KFC. Вот ваше главное меню: ', reply_markup=main_menu_bt())
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


bot.infinity_polling()
