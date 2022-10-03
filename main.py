from pprint import pprint
import pandas as pd
import telebot
from telebot import types
import datetime, time
import os


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


# Welcome message
@bot.message_handler(commands=['start'])
def start_button(message):
    start_time = int(time.time())

    # Get today task

    current_date = datetime.datetime.utcfromtimestamp(message.date).date()
    current_task = current_date_task_data(current_date)['task']
    bot.send_message(message.chat.id, current_task)

    callback_data_list = [str(i) + '|' + str(start_time) for i in range(1, 5)]
    pprint(callback_data_list)

    # Buttons
    keyboard = types.InlineKeyboardMarkup()
    button_one = types.InlineKeyboardButton('1', callback_data=callback_data_list[0])
    button_two = types.InlineKeyboardButton('2', callback_data='2')
    button_three = types.InlineKeyboardButton('3', callback_data='3')
    button_four = types.InlineKeyboardButton('4', callback_data='4')
    keyboard.add(button_one)
    keyboard.add(button_two)
    keyboard.add(button_three)
    keyboard.add(button_four)

    # Reply to user
    pprint(current_task)

    bot.send_message(message.chat.id, text='Выбери вариант ответа', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def longname(call):
    start_time = int(call.data.split("|")[1])
    answer = call.data.split("|")[0]
    cid = call.message.chat.id
    end_time = int(time.time())
    current_date = datetime.datetime.utcfromtimestamp(call.message.date).date()
    current_correct = str(list(current_date_task_data(current_date)['correct'])[0])
    current_is_correct = list(current_date_task_data(current_date)['is_correct'])[0]
    current_is_incorrect = list(current_date_task_data(current_date)['is_incorrect'])[0]

    bot.send_message(cid, call.data)
    bot.send_message(cid, end_time)
    duration = end_time - start_time
    message_duration = "Время решения задачи составило: {time} секунд".format(time=str(duration))
    bot.send_message(cid, message_duration)

    print(call.data)
    print(current_correct)
    print(call.data == current_correct)

    if answer == current_correct:
        bot.send_message(cid, current_is_correct)
    else:
        bot.send_message(cid, current_is_incorrect)


bot.infinity_polling()
