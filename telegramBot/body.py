import telebot
from telegramBot.config import API
from telegramBot.DataBaseCode import *

bot = API

@bot.message_handler(commands=['start'])
def startMessage(message):
    start_message = ("Здравствуйте!"
                     "\nЭтот бот предназначен "
                     "для подбора оптимальных комплектующих"
                     " для вашего компьютера под ваши задичи,"
                     " а так же ваш бюджет!\n"
                     "Для того чтобы пользоваться ботом правильно пройдите авторизацию "
                     "- это даст вам возможность собирать,"
                     " сохранять и просмативать свои последние сборки."
                     "\nЕсли у вас есть вопросы по командам "
                     "- пропишите команду /help")
    bot.send_message(message.chat.id,start_message)

@bot.message_handler(commands=['help'])
def helpMessage(message):
    bot.send_message(bot.chat.id, "Ща Хелпану!")

@bot.message_handler(commands=['startBuild'])
def helpMessage(message):
    bot.send_message(bot.chat.id, "<после этого можно будет собирать свою печку>")

@bot.message_handler(commands=['myLastBuild'])
def helpMessage(message):
    bot.send_message(bot.chat.id, "<тут будут твои билды>")