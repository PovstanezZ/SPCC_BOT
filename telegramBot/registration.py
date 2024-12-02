import telebot
from telegramBot.config import API
from telegramBot.data_base_code import *
from datetime import datetime

bot = API

def connect_db():
    conn = sqlite3.connect(dbPath)
    return conn
def create_users_table():
    """Создает таблицу users, если её еще нет."""
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT
        )
    """)
    conn.commit()
    conn.close()

create_users_table()  # Убедимся, что таблица существует

def register_user(telegram_id, username, first_name, last_name):
    """Добавляет пользователя в базу данных, если он еще не зарегистрирован."""
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    # Проверка на существование пользователя
    cursor.execute("SELECT 1 FROM users WHERE telegram_id = ?", (telegram_id,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO users (telegram_id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
            (telegram_id, username, first_name, last_name)
        )
        conn.commit()
        return True  # Пользователь успешно зарегистрирован
    else:
        return False  # Пользователь уже зарегистрирован
    conn.close()

@bot.message_handler(commands=["start", "register"])
def start_registration(message):
    """Обработчик команды /start или /register."""
    user_id = message.from_user.id
    username = message.from_user.username or "No username"
    first_name = message.from_user.first_name or "No first name"
    last_name = message.from_user.last_name or "No last name"

    if register_user(user_id, username, first_name, last_name):
        bot.send_message(message.chat.id, "Вы успешно зарегистрированы!")
    else:
        bot.send_message(message.chat.id, "Вы уже зарегистрированы в системе.")

# Запуск бота
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
