import telebot
from telebot import types
import dotenv
from func_util

SYSTEM_INFO_CAPTION = "Status"
config = dotenv.dotenv_values()
bot = telebot.TeleBot(config['API_KEY'])


def make_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True)
    btn_info = types.KeyboardButton(text=SYSTEM_INFO_CAPTION)
    markup.add(btn_info)
    bot.send_message(message.from_user.id, "Выберите действие", reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    make_menu(message)
def send_welcome(message):
    bot.reply_to(message, "As`Salam Aleikum, brat!")


@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    if message.text == SYSTEM_INFO_CAPTION:
        bot.send_message(message.from_user.id, )


bot.infinity_polling()
