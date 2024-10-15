import telebot
from telegramBot.config import API
from telegramBot.DataBaseCode import *
from datetime import datetime

bot = API

def connect_db():
    conn = sqlite3.connect(dbPath)
    return conn

# Создание таблицы пользователей, если она не существует
def create_users_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Создание таблицы для компонентов, если она не существует
def create_components_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS components (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            component_type TEXT NOT NULL,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            usage TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Проверка, зарегистрирован ли пользователь
def check_user(telegram_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE telegram_id = ?', (telegram_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# Регистрация нового пользователя через Telegram данные
def register_user(telegram_id, username, first_name, last_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (telegram_id, username, first_name, last_name)
        VALUES (?, ?, ?, ?)
    ''', (telegram_id, username, first_name, last_name))
    conn.commit()
    conn.close()

# Стартовый обработчик, проверка авторизации
@bot.message_handler(commands=['start'])
def start(message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    user = check_user(telegram_id)

    if user:
        bot.send_message(message.chat.id, "Вы уже зарегистрированы! Можете начинать искать комплектующие.")
        bot.send_message(message.chat.id, "Введите максимальный бюджет (например, 50000):")
        bot.register_next_step_handler(message, get_budget)
    else:
        # Регистрация пользователя
        register_user(telegram_id, username, first_name, last_name)
        bot.send_message(message.chat.id, f"Спасибо за регистрацию, {first_name}! Теперь можете начать поиск комплектующих.")
        bot.send_message(message.chat.id, "Введите максимальный бюджет (например, 50000):")
        bot.register_next_step_handler(message, get_budget)

# Получение бюджета от пользователя
def get_budget(message):
    try:
        budget = int(message.text)
        bot.send_message(message.chat.id, "Какое назначение компьютера вас интересует? (игры, графика, офис, универсальный)")
        bot.register_next_step_handler(message, get_usage, budget)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число для бюджета.")
        bot.register_next_step_handler(message, get_budget)

# Получение назначения от пользователя
def get_usage(message, budget):
    usage = message.text.lower()
    if usage in ['игры', 'графика', 'офис', 'универсальный']:
        search_components(message, budget, usage)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите одно из назначений: игры, графика, офис, универсальный.")
        bot.register_next_step_handler(message, get_usage, budget)

# Поиск комплектующих в базе данных
def search_components(message, budget, usage):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT component_type, name, price, usage FROM components
        WHERE price <= ? AND usage = ?
        ORDER BY price DESC
    ''', (budget, usage))

    results = cursor.fetchall()
    conn.close()

    if results:
        response = "Вот комплектующие, подходящие под ваш бюджет и назначение:\n\n"
        for row in results:
            component_type, name, price, usage = row
            response += f"{component_type}: {name} - {price} руб.\n"
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "К сожалению, не удалось найти комплектующие по вашим критериям.")

# Создание таблиц пользователей и компонентов при первом запуске
create_users_table()
create_components_table()