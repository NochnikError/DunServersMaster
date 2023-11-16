import psycopg2
from psycopg2 import Error
# Инициализация бд

# try:
#     connection = psycopg2.connect(user="postgres", password="postgres", host="localhost", port="5432", database="postgres")

    # cursor = connection.cursor()
    # create_table_query = '''CREATE TABLE login_bot
    #                       (ID_USER INT PRIMARY KEY     ,
    #                       FIRST_NAME           TEXT    ,
    #                       LAST_NAME            TEXT    ,
    #                       USERNAME             TEXT    ,
    #                       ACCESS_LEVEL         TEXT    ,
    #                       SALT                 TEXT    ,
    #                       LOGIN_HASH           TEXT    ,
    #                       PASSWORD_HASH        TEXT    ,
    #                       REGISTARED          BOOL);'''
    # cursor.execute(create_table_query)
    # connection.commit()
    # print("BD created.")
    # fsj = (2178717, "test", "tset", "hui")
    # cursor.execute("INSERT INTO login_bot (id_user, first_name,  last_name, username) VALUES (%s, %s, %s, %s)", fsj)
    # connection.commit()
    # print("Данные добавлены")
    # print("Информация о сервере PostgreSQL")
    # print(connection.get_dsn_parameters(), "\n")
    # cursor.execute("SELECT version();")
    # record = cursor.fetchone()
    # print("Вы подключены к - ", record, "\n")
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

salt = 'ndasdiaddsa'
user_id = 415172037
update_q = ("UPDATE login_bot set salt = %s WHERE id_user = %s")
data = (salt, user_id)
cursor.execute(update_q, data)
connection.commit()


finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")