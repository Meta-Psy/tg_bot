import telebot
from buttons import *

bot = telebot.TeleBot(token='7460808784:AAH-AVWMVr05NfNx41ASgrB-4KZLR56l7sA')


@bot.message_handler(commands=['start'])
def start(cmd):
    chat_id = cmd.chat.id
    bot.send_message(chat_id, 'Пожалуйста, нажмите кнопку ниже, чтобы заказать свой продукт',
                     reply_markup=hello_bt())
    print(cmd)
@bot.message_handler(content_types=['text'])
def telephone(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Отправьте пожалуйста ваш телефон, через кнопку в меню',
                     reply_markup=get_telephone())
    bot.register_next_step_handler(message, get_location)

def get_location(message):
    user_phone = message.contact.phone_number
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Отправьте пожалуйста вашу локацию, через кнопку в меню',
                     reply_markup=get_location())

bot.infinity_polling()