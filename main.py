import os
import time
import hashlib
import logging
import psycopg2
from psycopg2 import Error
import dotenv
import telebot
from telebot import types
import subprocess
from src.func_util.cpu import CpuUsageInfo, RamUsageInfo, DiskUsageInfo, NetUsageInfo, PIDUsageInfo

user_id = 0
try:
    connection = psycopg2.connect(user="postgres", password="postgres", host="localhost", port="5432",
                                  database="postgres")
    cursor = connection.cursor()
    cursor.execute("select id_user from login_bot;")
    res = cursor.fetchall()
    print(res)
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
    cursor.execute("SELECT id_user FROM login_bot")
    user_id = message.chat.id
    user_bd = cursor.fetchall()
    res = [int(''.join(map(str, x))) for x in user_bd]
    body = (message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
    if user_id in res:
        print("Waiting login:", body)
        bot.reply_to(message, "Welcome to the club. Again.\nSend (/login), for authorization")
        bot.register_next_step_handler()
    else:
        cursor.execute("INSERT INTO login_bot (id_user, first_name,  last_name, username) VALUES (%s, %s, %s, %s)",
                       body)
        connection.commit()
        print("New member:", body)
        bot.reply_to(message, "Welcome to the club, goi!\nSend (/register) me for details ")


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, 'send /menu, for menu title,\n send /login for window authorization')


@bot.message_handler(commands=['feedback'])
def feedback_message(message):
    test = bot.reply_to(message, "Describe your problem:")
    bot.register_next_step_handler(test, out_message)


def out_message(message):
    output = bot.send_message(message.chat.id, "Your problem for consideration.")
    bot.send_message(6052726574, message.text)
    bot.send_message(6052726574, message.chat.id)


@bot.message_handler(commands=['login'])
def login(message):
    login_message = bot.send_message(message.chat.id, "Send login")
    bot.register_next_step_handler(login_message, auth)


def auth(login_message):
    select_salt = "SELECT salt FROM login_bot"
    select_login = "SELECT login_hash FROM logtin_bot"

    login = hashlib.pbkdf2_hmac('sha256', login_message, select_salt, 256000)

    if login == select_login:
        bot.delete_message(login_message.chat.id, login_message.id)
        password_message = bot.send_message(login_message.chat.id, "Send password")
        bot.register_next_step_handler(password_message, check_credentials, login_message)
    else:
        bot.send_message(login_message.chat.id, 'Wrong login. Try again')
        bot.delete_message(login_message.chat.id, login_message.id)



def check_credentials(password_message, login_message):
    select_password = "SELECT password_hash FROM login_bot"
    if select_password == password_message:
        bot.send_message(password_message.chat.id, 'Welcome, master!')
        bot.delete_message(password_message.chat.id, password_message.id)
    else:
        bot.send_message(password_message.chat.id, 'Wrong login or password! Try again.')
        bot.delete_message(password_message.chat.id, password_message.id)


@bot.message_handler(commands=['register'])
def get_login(message):
    reg_login_message = bot.send_message(message.chat.id, "Create a username for login in this bot:")
    bot.register_next_step_handler(reg_login_message, register_login)
    bot.delete_message(message.chat.id, message)
def get_password(message):
    reg_pass_message = bot.send_message(message.chat.id, "Create a password for login in this bot:")
    bot.register_next_step_handler(reg_pass_message, register_password)
    bot.delete_message(message.chat.id, message)
def register_login(reg_login_message, message):
    salt = os.urandom(128)
    get_login = reg_login_message.text
    reg_login = get_login.encode('utf-8')
    login = hashlib.pbkdf2_hmac('sha256', reg_login, salt, 256000)
    user_id = message.chat.id
    update_q = ("UPDATE login_bot set salt = %s WHERE id_user = %s")
    data = (salt, user_id)
    cursor.execute(update_q, data)
    connection.commit()
    update_q = ("UPDATE login_bot set login_hash = %s WHERE id_user = %s")
    data = (login, user_id)
    cursor.execute(update_q, data)
    connection.commit()
    bot.register_next_step_handler(salt, get_password)
def register_password(salt, reg_pass_message):
    get_pass = reg_pass_message.text
    reg_pass = get_pass.encode('utf-8')
    password_hash = hashlib.pbkdf2_hmac('sha256', reg_pass, salt, 256000)
    update_q = ("UPDATE login_bot set password_hash = %s WHERE id_user = %s")
    data = (password_hash, user_id)
    cursor.execute(update_q, data)
    connection.commit()



@bot.message_handler(commands=['menu'])
def menu_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn_stats = types.KeyboardButton("/stats")
    btn_feedback = types.KeyboardButton("/feedback")
    btn_register = types.KeyboardButton("/register")
    btn_login = types.KeyboardButton("/login")
    markup.add(btn_login)
    markup.add(btn_register)
    markup.add(btn_feedback)
    markup.add(btn_stats)
    bot.send_message(message.chat.id, 'Press the required button', reply_markup=markup)


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
        # markup.add(btn_usr)
        # markup.add(btn_cmd)
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
    # elif message.text == "/users":
    #     bot.send_message(message.chat.id, text="to soon")


@bot.message_handler(commands=['command', 'New command'])
def input_command(message):
    get_command_message = bot.send_message(message.chat.id, "Send me command for execution in server: ")
    bot.register_next_step_handler(get_command_message, return_result)
def return_result(get_command_message):
    completed = subprocess.check_output([get_command_message.text])
    bot.send_message(get_command_message.chat.id, completed)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    repeat_btn = types.KeyboardButton("New command")
    markup.add(repeat_btn)



# @bot.message_handler(content_types='text')
# def button_list_command(message):
#     if message.text == "/command":
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         btn_ls = types.KeyboardButton("ls")
#         btn_ipa = types.KeyboardButton("ip a")
#         btn_ifconfig = types.KeyboardButton("ifconfig")
#         btn_update = types.KeyboardButton("apt update")
#         btn_reboot = types.KeyboardButton("reboot")
#         btn_shutdown = types.KeyboardButton("shutdown")
#         btn_ping = types.KeyboardButton("ping")
#         markup.add(btn_ls)
#         markup.add(btn_ipa)
#         markup.add(btn_ifconfig)
#         markup.add(btn_update)
#         markup.add(btn_reboot)
#         markup.add(btn_shutdown)
#         markup.add(btn_ping)
#         bot.send_message(message.chat.id, 'Press the required button', reply_markup=markup)
#     elif message.text == "ls":
#         result = subprocess.run(["ls"], capture_output=True)
#         bot.send_message(message.chat.id, result.stdout.decode)
#     elif message.text == "ip a":
#         result = subprocess.run(["ip a"], capture_output=True)
#         bot.send_message(message.chat.id, result.stdout.decode)
#     elif message.text == "ifconfig":
#         result = subprocess.run(["ifconfig"], capture_output=True)
#         bot.send_message(message.chat.id, result.stdout.decode)
#     elif message.text == "apt update":
#         result = subprocess.run(["sudo apt update && sudo apt dist-upgrade"], capture_output=True)
#         bot.send_message(message.chat.id, result.stdout.decode)
#     elif message.text == "reboot":
#         result = subprocess.run(["sudo reboot now"], capture_output=True)
#         bot.send_message(message.chat.id, result.stdout.decode)
#     elif message.text == "shutdown":
#         result = subprocess.run(["sudo shutdown now"], capture_output=True)
#         bot.send_message(message.chat.id, result.stdout.decode)
#     elif message.text == "ping":
#         result = subprocess.run(["ping 8.8.8.8"], capture_output=True)
#         bot.send_message(message.chat.id, result.stdout.decode)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            time.sleep(10)
