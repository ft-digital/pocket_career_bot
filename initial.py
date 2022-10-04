import sqlite3
from pprint import pprint
from sqlite3 import Error


# def create_connection(path):
#     connection = None
#     try:
#         connection = sqlite3.connect(path)
#         print("Connection to SQLite DB successful")
#     except Error as e:
#         print(f"The error '{e}' occurred")
#
#     return connection
#
#
# def execute_query(connection, query):
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query)
#         connection.commit()
#         print("Query executed successfully")
#     except Error as e:
#         print(f"The error '{e}' occurred")
#
#
# def execute_read_query(connection, query):
#     cursor = connection.cursor()
#     result = None
#     try:
#         cursor.execute(query)
#         result = cursor.fetchall()
#         return result
#     except Error as e:
#         print(f"The error '{e}' occurred")


# Вопросы - дата, вопрос, правильный ответ, отбивка при верном ответе, отбивка при неверном ответе
# Ответы пользователей - дата, id пользователя, верно/не верно, нажал на кнопку начать, нажал на кнопку ответа

# Create new database
# connection = create_connection("bot_users_data.sqlite")

# Open connection
#
# connection = sqlite3.connect('bot_users_data.sqlite')

# Create question table

# create_questions_table = """
# CREATE TABLE IF NOT EXISTS questions (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   date TEXT,
#   question TEXT,
#   right_answer TEXT,
#   correct_reply TEXT,
#   incorrect_reply TEXT
# );
# """

# execute_query(connection, create_questions_table)

# Create answers  table
#
# create_answers_table = """
# CREATE TABLE IF NOT EXISTS answers(
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   date TEXT,
#   tg_id TEXT,
#   is_right INT,
#   start_datetime INT,
#   end_datetime INT
# );
# """

# execute_query(connection, create_answers_table)
#
# create_questions = """
# INSERT INTO
#   questions (date, question, right_answer, correct_reply, incorrect_reply)
# VALUES
#   ('2022-10-01', 'question_1', '2', 'good boy', 'bad boy'),
#   ('2022-10-02', 'question_2', '1', 'good boy 2', 'bad boy 2');
# """

# execute_query(connection, create_questions)


# Test table - id, name, answer
# create_test_table = """
# CREATE TABLE IF NOT EXISTS test (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   tg_id TEXT,
#   tg_name TEXT,
#   answer TEXT
# );
# """

# execute_query(connection, create_test_table)


# EXECUTE QUERY
#
# query = """
# SELECT * FROM test
# """
#
# pprint(execute_read_query(connection, query))


# # Подключаемся к ДБ
# conn = sqlite3.connect('users_info.db')
# c = conn.cursor()

# # Создаем таблицу с данными пользователей
# c.execute('CREATE TABLE IF NOT EXISTS users (user_id INT, date TEXT, tg_id TEXT, answer INT, is_correct INT, start_time TEXT, end_time TEXT, duration INT)')
