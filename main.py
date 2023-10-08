import dotenv
import telebot
import logging
from telebot import types
from src.func_util.cpu import CpuUsageInfo, RamUsageInfo, DiskUsageInfo

# logger = telebot.logger
# telebot.logger.basicConfig(filename='test.log', level=logging.DEBUG,
#                            format=' %(asctime)s - %(levelname)s - %(message)s')


version = 0.03
SYSTEM_INFO_CAPTION = "/menu"
config = dotenv.dotenv_values()
bot = telebot.TeleBot(config['API_KEY'])
print(config['teg'])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the club, goi!")


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
        btn_swap = types.KeyboardButton("SWAP")
        btn_usr = types.KeyboardButton("USERS")
        markup.add(btn_cpu)
        markup.add(btn_disk)
        markup.add(btn_net)
        markup.add(btn_pid)
        markup.add(btn_ram)
        markup.add(btn_swap)
        markup.add(btn_usr)
        bot.send_message(message.chat.id, 'Press the required button', reply_markup=markup)
    elif message.text == "CPU":
        cpu_info = CpuUsageInfo()
        bot.send_message(message.chat.id, text=cpu_info.get_info_time())
    elif message.text == "DISK":
        disk_info = DiskUsageInfo()
        bot.send_message(message.chat.id, text=disk_info.mount_get_info())
    elif message.text == "NET":
        bot.send_message(message.chat.id, text="NET_INFO")
    elif message.text == "PID":
        bot.send_message(message.chat.id, text="PID_INFO")
    elif message.text == "RAM":
        ram_info = RamUsageInfo()
        bot.send_message(message.chat.id, text=ram_info.ram_get_info())
    elif message.text == "SWAP":
        swap_info = RamUsageInfo()
        bot.send_message(message.chat.id, text=swap_info.swap_get_info())
    elif message.text == "USERS":
        bot.send_message(message.chat.id, text="USERS_INFO")


bot.infinity_polling()
