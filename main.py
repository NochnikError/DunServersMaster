import telebot
from telebot import types

bot = telebot.TeleBot('6531368501:AAHMU3_QepnHk2q7OFQmQXwbx4Xdt2pYvoQ')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "As`Salam Aleikum, brat!")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()


@bot.message_handler(commands=['start'])
def start(message):
