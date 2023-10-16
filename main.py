import os
import hashlib
import logging
import psycopg2
from psycopg2 import Error
import dotenv
import telebot
from telebot import types
from subprocess import check_output
from src.func_util.cpu import CpuUsageInfo, RamUsageInfo, DiskUsageInfo, NetUsageInfo, PIDUsageInfo
user_id = 0
try:
    connection = psycopg2.connect(user="postgres", password="postgres", host="localhost", port="5432", database="postgres")
    cursor = connection.cursor()
    print("Информация о сервере PostgreSQL")
    print(connection.get_dsn_parameters(), "\n")
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("Вы подключены к - ", record, "\n")

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)



logging.basicConfig(level=logging.DEBUG, filename="test.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")

version = 0.06
config = dotenv.dotenv_values()
bot = telebot.TeleBot(config['API_KEY'])
print(config['teg'])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    body = (message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
    print(type(body))
    if user_id == cursor.execute("SELECT id_user FROM login_bot"):
        print("Waiting login:", body)
        bot.reply_to(message, "Welcome to the club. Again.\nSend (login), for authorization")
    else:
        cursor.execute("INSERT INTO login_bot (id_user, first_name,  last_name, username) VALUES (%s, %s, %s, %s)", body)
        connection.commit()
        print("New member:", body)
        bot.reply_to(message, "Welcome to the club, goi!\nSend (/register) me for details ")


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


# Здесь необходимо вытащить из всего вывода именно сообщения, конвертировать его в байты по utf-8 и после этого хэшировать данные.
@bot.message_handler(commands=['register'])
def get_login(message):
    reg_login = bot.send_message(message.chat.id, "Create a username for login in this bot:")
    bot.delete_message(message.chat.id, message)
    bot.register_next_step_handler(get_login, treatment_login)


def treatment_login(get_login):
    salt = os.urandom(128)
    get_login = get_login.text
    reg_login = get_login.encode('utf-8')
    login = hashlib.pbkdf2_hmac('sha256', reg_login, salt, 256000)
    storage = salt + login
    bot.register_next_step_handler(get_login, get_password)


def get_password(message):
    reg_pass = bot.send_message(message.chat.id, "Cool, create a password:")
    salt_for_pass = os.urandom(256)
    password = hashlib.pbkdf2_hmac('sha256', reg_pass.text, salt_for_pass, 512000)
    storage = salt_for_pass + password
    bot.delete_message(message.chat.id, reg_pass.chat.id)


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
        btn_cmd = types.KeyboardButton("/command")
        markup.add(btn_cpu)
        markup.add(btn_disk)
        markup.add(btn_net)
        markup.add(btn_pid)
        markup.add(btn_ram)
        markup.add(btn_swap)
        markup.add(btn_usr)
        markup.add(btn_cmd)
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
    elif message.text == "/command":
        bot.send_message(message.chat.id, text="Write a command to execute:")
        bot.register_next_step_handler(message, command)


def command(message):
    if user_id == (354939115, 415172037):
        cmd = message.text
        try:
            bot.send_message(message.chat.id, check_output(cmd, shell=True))
        except:
            bot.send_message(message.chat.id, "Invalid input")


bot.infinity_polling()
