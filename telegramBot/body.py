import telebot
from telegramBot.config import API

bot = API

@bot.message_handler(commands=['start'])
def startMessage(message):
    start_message = ("Здравствуйте! Для корректной работы с нашим ботом,"
                     " пропишите команду "
                     "/help, она вам поможет :D")
    bot.send_message(message.chat.id,start_message)

@bot.message_handler(commands=['help'])
def helpMessage(message):
    bot.send_message(bot.chat.id, "Ща Хелпану!")