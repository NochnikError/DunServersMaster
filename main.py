import logging
import dotenv
import telebot
from telebot import types
from src.func_util.cpu import CpuUsageInfo, RamUsageInfo, DiskUsageInfo, NetUsageInfo, PIDUsageInfo
import smtplib as smtp


logging.basicConfig(level=logging.DEBUG, filename="test.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")

version = 0.05
config = dotenv.dotenv_values()
bot = telebot.TeleBot(config['API_KEY'])
print(config['teg'])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the club, goi!\nSend (/help) me for details ")


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, 'send /menu, for menu title,\n send /login for window authorization')


@bot.message_handler(commands=['feedback'])
def feedback_message(message):
    test = bot.reply_to(message, "Describe your problem")
    bot.register_next_step_handler(test, out_message)


def out_message(message):
    output = bot.send_message(message.chat.id, "Your problem for consideration.")
    bot.send_message(6052726574, message.text)
    bot.send_message(6052726574, message.chat.id)


@bot.message_handler(commands=['login'])
def test(message):
    login_message = bot.send_message(message.chat.id, "Send login")
    bot.register_next_step_handler(login_message, auth)


def auth(login_message):
    if login_message.text == "login":
        bot.delete_message(login_message.chat.id, login_message.id)
        password_message = bot.send_message(login_message.chat.id, "Send password")
        bot.register_next_step_handler(password_message, check_credentials, login_message)
    else:
        bot.send_message(login_message.chat.id, 'Wrong login. Try again')


#
def check_credentials(password_message, login_message):
    credentials = {
        'login': login_message.text,
        'password': password_message.text,
    }

    if credentials['login'] == 'login' and credentials['password'] == 'password':
        bot.send_message(password_message.chat.id, 'Welcome, master!')
        bot.delete_message(password_message.chat.id, password_message.id)
    else:
        bot.send_message(password_message.chat.id, 'Wrong login or password! Try again.')
        bot.delete_message(password_message.chat.id, password_message.id)


@bot.message_handler(commands=['register'])
@bot.message_handler(commands=['menu'])
def menu_message(message):
    trank = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn_stats = types.KeyboardButton("/stats")
    btn_feedback = types.KeyboardButton("/feedback")
    btn_register = types.KeyboardButton("/register")
    btn_login = types.KeyboardButton("/login")
    trank.add(btn_login)
    trank.add(btn_register)
    trank.add(btn_feedback)
    trank.add(btn_stats)
    bot.send_message(message.chat.id, 'Press the required button', reply_markup=trank)


@bot.message_handler(content_types='text')
def button_message(message):
    if message.text == "/stats":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn_cpu = types.KeyboardButton("/cpu")
        btn_ram = types.KeyboardButton("/ram")
        btn_disk = types.KeyboardButton("/disk")
        btn_net = types.KeyboardButton("/net")
        btn_pid = types.KeyboardButton("/pid")
        btn_swap = types.KeyboardButton("/swap")
        btn_usr = types.KeyboardButton("/users")
        markup.add(btn_cpu)
        markup.add(btn_disk)
        markup.add(btn_net)
        markup.add(btn_pid)
        markup.add(btn_ram)
        markup.add(btn_swap)
        markup.add(btn_usr)
        bot.send_message(message.chat.id, 'Press the required button', reply_markup=markup)
    elif message.text == "/cpu":
        cpu_info = CpuUsageInfo()
        bot.send_message(message.chat.id, text=cpu_info.get_info_time())
    elif message.text == "/ram":
        ram_info = RamUsageInfo()
        bot.send_message(message.chat.id, text=ram_info.ram_get_info())
    elif message.text == "/swap":
        swap_info = RamUsageInfo()
        bot.send_message(message.chat.id, text=swap_info.swap_get_info())
    elif message.text == "/disk":
        disk_info = DiskUsageInfo()
        bot.send_message(message.chat.id, text=disk_info.get_stats_message())
    elif message.text == "/net":
        net_info = NetUsageInfo()
        bot.send_message(message.chat.id, text=net_info.net_get_info_all_io())
    elif message.text == "/pid":
        pid = PIDUsageInfo
        bot.send_message(message.chat.id, text=pid.print_top_pid())
    elif message.text == "/users":
        bot.send_message(message.chat.id, text="to soon")


bot.infinity_polling()
