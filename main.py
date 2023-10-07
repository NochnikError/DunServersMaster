import dotenv
import telebot
from telebot import types

from src.func_util.ram_usage import RamUsageInfo

version = 0.02
SYSTEM_INFO_CAPTION = "/menu"
config = dotenv.dotenv_values()
bot = telebot.TeleBot(config['API_KEY'])
print(config['teg'])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "As`Salam Aleikum, brat!")


def make_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True)
    btn_info = types.KeyboardButton(text=SYSTEM_INFO_CAPTION)
    markup.add(btn_info)
    bot.send_message(message.from_user.id, "commands:\nmenu", reply_markup=markup)


def start(message):
    make_menu(message)


@bot.message_handler(content_types='text')
def button_message(message):
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
    elif message.text == "CPU":
        bot.send_message(message.chat.id, "CPU_INFO")
    elif message.text == "DISK":
        bot.send_message(message.chat.id, text="DISK_INFO")
    elif message.text == "NET":
        bot.send_message(message.chat.id, text="NET_INFO")
    elif message.text == "PID":
        bot.send_message(message.chat.id, text="PID_INFO")
    elif message.text == "RAM":
        ram_info = RamUsageInfo()
        bot.send_message(message.chat.id, text=ram_info.get_info())
    elif message.text == "USERS":
        bot.send_message(message.chat.id, text="USERS_INFO")


bot.infinity_polling()
