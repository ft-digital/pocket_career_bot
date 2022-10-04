from pprint import pprint
import pandas as pd
import numpy as np
import telebot
from telebot import types
import datetime, time
import os
import sqlite3

class User:
    def __int__(self):
        self.start_time = 0

# Start bot
bot_token = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(bot_token, parse_mode=None)

# Функция чтения файла с задачами и фильтрации строки с нужной датой
def current_date_task_data(current_date):
    tasks = pd.read_csv('date_task.csv', sep=';')
    tasks['date'] = pd.to_datetime(tasks['date'])
    current_date_mask = tasks['date'].dt.date == current_date
    current_task_row = tasks[current_date_mask]

    return current_task_row

#About nessage
@bot.message_handler(commands=['start'])
def start_button(message):
    ab = pd.read_csv('about.csv', sep=';')
    text = ab['about'][0]
    # Reply to user
    bot.send_message(message.chat.id, text=text)

@bot.message_handler(commands=['help'])
def help_button(message):
    ab = pd.read_csv('about.csv', sep=';')
    text = ab['help'][0]
    # Reply to user
    bot.send_message(message.chat.id, text=text)

# Welcome message
@bot.message_handler(commands=['task'])
def task_button(message):
    start_time = int(time.time())

    # Get today task
    current_date = datetime.datetime.utcfromtimestamp(message.date).date()
    current_task = current_date_task_data(current_date)['task']
    #Проверяем, есть ли на сегодня задача
    if current_task.empty:
        bot.send_message(message.chat.id, text = "На сегодня нет задач.")
    else:
        bot.send_message(message.chat.id, current_task)

        callback_data_list = [str(i) + '|' + str(start_time) for i in range(1, 5)]

        # Buttons
        keyboard = types.InlineKeyboardMarkup()
        button_one = types.InlineKeyboardButton('1', callback_data=callback_data_list[0])
        button_two = types.InlineKeyboardButton('2', callback_data=callback_data_list[1])
        button_three = types.InlineKeyboardButton('3', callback_data=callback_data_list[2])
        button_four = types.InlineKeyboardButton('4', callback_data=callback_data_list[3])
        keyboard.add(button_one)
        keyboard.add(button_two)
        keyboard.add(button_three)
        keyboard.add(button_four)

        # Reply to user
        bot.send_message(message.chat.id, text='Выбери вариант ответа', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def longname(call):

    # Берем время начала и ответ юзера переданные в callback с предыдущего шага
    start_time = int(call.data.split("|")[1])
    answer = call.data.split("|")[0]
    # Берем ID чата и время нажатия на кнопку
    cid = call.message.chat.id
    end_time = int(time.time())

    # Берем инфу из таблицы с задачами про сегодняшнюю дату: правильный ответ, отбивку для верного, отбивку для неверного
    current_date = datetime.datetime.utcfromtimestamp(call.message.date).date()
    current_correct = str(list(current_date_task_data(current_date)['correct'])[0])
    current_is_correct = list(current_date_task_data(current_date)['is_correct'])[0]
    current_is_incorrect = list(current_date_task_data(current_date)['is_incorrect'])[0]

    # Проверяем и отправляем соответствующее сообщение

    if answer == current_correct:
        bot.send_message(cid, current_is_correct)
        is_correct = 1
    else:
        bot.send_message(cid, current_is_incorrect)
        is_correct = 0

    # Считаем сколько времени ушло на решение задачи и сообщаем пользователю
    duration = end_time - start_time
    message_duration = "Время решения задачи составило: {time} секунд".format(time=str(duration))
    bot.send_message(cid, message_duration)

    #Записываем данные в таблицу в БД на сервере

    conn = sqlite3.connect('users_info.db')
    c = conn.cursor()
    c.execute(
        'INSERT INTO users_info (tg_id, date, us_answer, is_correct, start_time, end_time, duration) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (cid, current_date, answer, is_correct, start_time, end_time, duration))
    conn.commit()
    c.close()
    conn.close()


#Statistics message
@bot.message_handler(commands=['stats'])
def stats_button(message):
    tg_id = message.chat.id
    # Подключаемся к ДБ
    conn = sqlite3.connect('users_info.db')
    c = conn.cursor()

    # Задачи
    def get_right_answers(us_id):

        sum_query = """
                SELECT SUM(is_correct) FROM users_info
                WHERE tg_id LIKE '%{tg_id}%'
        """.format(tg_id=tg_id)
        sum_right = c.execute(sum_query).fetchall()[0][0]
        print(sum_right)

        len_query = """
                SELECT COUNT(is_correct) FROM users_info
                WHERE tg_id LIKE '%{tg_id}%'
        """.format(tg_id=tg_id)
        len_tasks = c.execute(len_query).fetchall()[0][0]

        return sum_right, len_tasks

    task_message = "Правильно решенных задач: " + str(get_right_answers(tg_id)[0]) + "\n\n" + "Всего задач: " + str(get_right_answers(tg_id)[1])

    # Время
    def get_av_time(us_id):
        query = """
        SELECT AVG(duration) FROM users_info
        WHERE tg_id LIKE '%{tg_id}%'
        """.format(tg_id=tg_id)
        avg_dur = c.execute(query).fetchall()[0][0]

        return avg_dur

    av_time_message = "\n\n" + "Среднее время на решение одной задачи: " + str(get_av_time(tg_id))
    stats_message = task_message + av_time_message

    bot.send_message(tg_id, stats_message)

    c.close()
    conn.close()


bot.infinity_polling()
