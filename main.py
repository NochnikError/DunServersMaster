import dotenv
import telebot
from telebot import types

SYSTEM_INFO_CAPTION = "/menu"
config = dotenv.dotenv_values()
bot = telebot.TeleBot(config['API_KEY'])
print(config['teg'])

@bot.message_handler(commands=['start'])
def start(message):
    make_menu(message)


def send_welcome(message):
    bot.reply_to(message, "As`Salam Aleikum, brat!")


def make_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True)
    btn_info = types.KeyboardButton(text=SYSTEM_INFO_CAPTION)
    markup.add(btn_info)
    bot.send_message(message.from_user.id, "commands:\nmenu", reply_markup=markup)

# @bot.message_handler(commands=['start'])
# def button_message(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     btn_menu = types.KeyboardButton("/menu")
#     markup.add(btn_menu)
#     bot.send_message(message.chat.id, '/Menu', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text == "/menu":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_cpu = types.KeyboardButton("CPU")
        btn_disk = types.KeyboardButton("DISK")
        btn_net = types.KeyboardButton("NET")
        btn_pid = types.KeyboardButton("PID")
        btn_ram = types.KeyboardButton("RAM")
        btn_usr = types.KeyboardButton("USERS")
        markup.add(btn_cpu)
        markup.add(btn_disk)
        markup.add(btn_net)
        markup.add(btn_pid)
        markup.add(btn_ram)
        markup.add(btn_usr)
        bot.send_message(message.chat.id, 'Press the required button', reply_markup=markup)
    # elif message.text=="":
    #     bot.send_message(message.chat.id,'')

bot.infinity_polling()
