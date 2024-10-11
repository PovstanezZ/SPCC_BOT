import telegramBot
from telegramBot.config import API

bot = API
@bot.message_handler(commands=['start'])
def startMessage():
    bot.send_message("Hello")