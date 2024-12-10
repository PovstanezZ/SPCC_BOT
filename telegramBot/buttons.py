import telebot
import subprocess
from telebot import types

from telegramBot.config import API
from telegramBot.data_base_code import *
from telegramBot.registration import *

bot = API
@bot.message_handler(commands=["test"])
def hui(message):
    keyboard_register = types.InlineKeyboardMarkup()

    # Кнопки
    add_build_button = types.InlineKeyboardButton(text="Создать сборку", callback_data='btn1')
    saved_build_button = types.InlineKeyboardButton(text="Посмотреть сохранённые", callback_data="saved_builds")

    # Inline клавиатура
    keyboard_register.add(add_build_button)
    keyboard_register.add(saved_build_button)
    bot.send_message(message.chat.id, "Предлогаю вам выбрать действия из перечисленных ниже:",
                         reply_markup=keyboard_register)

@bot.callback_query_handler(func=lambda callback: True)
def response(callback):
    if callback.message:
      if callback.data == "btn1":
        try:
            bot.send_message(callback.message.chat.id, "Вы нажали кнопку 'Создать сборку'!")
        except:
          return

# @bot.callback_query_handler(func=lambda callback: True)
# def callback_handler(callback):
#     print(f"Received callback: {callback.data}")
#     if callback.data == "add_new_build":
#         print("1")
#         bot.send_message(callback.message.chat.id, "Вы нажали кнопку 'Создать сборку'!")
#         print("11")
#     elif callback.data == "saved_builds":
#         print("2")
#         bot.send_message(callback.message.chat.id, "Вы нажали кнопку 'Посмотреть сохранённые'!")
#         print("22")
#     else:
#         print(f"Unexpected callback_data: {callback.data}")
bot.infinity_polling()