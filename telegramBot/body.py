import telebot
from telegramBot.config import API
from telegramBot.data_base_code import *
from datetime import datetime

bot = API

def connect_db():
    conn = sqlite3.connect(dbPath)
    return conn

