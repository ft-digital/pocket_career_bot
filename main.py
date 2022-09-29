from pprint import pprint
import pandas as pd
import telebot
from telebot import types
import datetime, time

bot_token = '5541011348:AAEEEA-9K-0AYpudzj5vrf9dU4n4Q2r69t8'

# Start bot
bot = telebot.TeleBot(bot_token, parse_mode=None)

# Выдать задачу для этой даты

# tasks = pd.read_csv('date_task.csv', sep=';')
# tasks['date'] = pd.to_datetime(tasks['date'])
# pprint(tasks['date'].dt.date[2])

# Welcome message
@bot.message_handler(commands=['start'])
def start_button(message):
    # Get today task
    tasks = pd.read_csv('date_task.csv', sep=';')
    tasks['date'] = pd.to_datetime(tasks['date'])
    current_date = datetime.datetime.utcfromtimestamp(message.date).date()
    current_date_mask = tasks['date'].dt.date == current_date
    pprint(current_date)
    pprint(current_date_mask)
    current_task = tasks[current_date_mask]['task']
    pprint(current_task)

    # Buttons
    # button_one = types.InlineKeyboardButton('1', callback_data='1')
    # button_two = types.InlineKeyboardButton('2', callback_data='2')
    # keyboard = types.InlineKeyboardMarkup()
    # keyboard.add(button_one)
    # keyboard.add(button_two)

    # Reply to user
    pprint(current_task)
    bot.send_message(message.chat.id, current_task)
    # msg = bot.send_message(message.chat.id, text='Выбери вариант ответа', reply_markup=keyboard)
    # bot.register_next_step_handler(msg, process_city_step)


# def process_city_step(message):
#     if not message.text.startswith('/'):
#         bot.send_message(message.chat.id, 'You has to click one of the buttons!')
#     start_button(message)


# @bot.callback_query_handler(func=lambda call: True)
# def longname(call):
#     if call.data == "1":
#         bot.send_message(chat_id=call.message.chat.id, text="Нажал 1")


bot.infinity_polling()
