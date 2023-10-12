import dotenv
import telebot
import logging
from telebot import types
from src.func_util.cpu import CpuUsageInfo, RamUsageInfo, DiskUsageInfo, NetUsageInfo, PIDUsageInfo

logging.basicConfig(level=logging.DEBUG, filename="test.log",filemode="w",
                    format = "%(asctime)s %(levelname)s %(message)s")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")


version = 0.04
SYSTEM_INFO_CAPTION = "/menu"
config = dotenv.dotenv_values()
bot = telebot.TeleBot(config['API_KEY'])
print(config['teg'])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the club, goi!\nSend (/menu) me for details ")

@bot.message_handler(content_types='text')
def button_message(message):
    if message.text == "/menu":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn_cpu = types.KeyboardButton("CPU")
        btn_ram = types.KeyboardButton("RAM")
        btn_disk = types.KeyboardButton("DISK")
        btn_net = types.KeyboardButton("NET")
        btn_pid = types.KeyboardButton("PID")
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
    elif message.text == "RAM":
        ram_info = RamUsageInfo()
        bot.send_message(message.chat.id, text=ram_info.ram_get_info())
    elif message.text == "SWAP":
        swap_info = RamUsageInfo()
        bot.send_message(message.chat.id, text=swap_info.swap_get_info())
    elif message.text == "DISK":
        disk_info = DiskUsageInfo()
        bot.send_message(message.chat.id, text=disk_info.get_stats_message(), parse_mode='Markdown')
    elif message.text == "NET":
        net_info = NetUsageInfo()
        bot.send_message(message.chat.id, text=net_info.net_get_info_all_io())
    elif message.text == "PID":
        pid = PIDUsageInfo
        bot.send_message(message.chat.id, text=pid.print_top_pid())
    elif message.text == "USERS":
        bot.send_message(message.chat.id, text="to soon")


bot.infinity_polling()
pid = PIDUsageInfo()
