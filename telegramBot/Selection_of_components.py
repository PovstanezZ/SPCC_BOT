import sqlite3
import time
from telebot import TeleBot, types
from threading import Timer
from telegramBot.config import API
from telegramBot.data_base_code import *
from telegramBot.registration import *
from datetime import datetime

bot = API

def connect_db():
    conn = sqlite3.connect(dbPath)
    return conn

# Словарь для временного хранения сборок
active_builds = {}

def create_builds_table():
    """Создает таблицу user_builds, если её еще нет."""
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_builds (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        processor_id INTEGER,
        ram_id INTEGER,
        gpu_id INTEGER,
        power_supply_id INTEGER,
        storage_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(user_id),
        FOREIGN KEY(processor_id) REFERENCES processors(id),
        FOREIGN KEY(ram_id) REFERENCES ram(id),
        FOREIGN KEY(gpu_id) REFERENCES gpus(id),
        FOREIGN KEY(power_supply_id) REFERENCES power_supplies(id),
        FOREIGN KEY(storage_id) REFERENCES storage(id)
    );
    """)
    conn.commit()
    conn.close()

create_builds_table()

def create_components_tables():
    """Создает таблицы для компонентов, если их нет."""
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()

    # Таблицы для комплектующих
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS processors (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL CHECK(category IN ('gaming', 'work', 'graphics', 'budget')),
        price INTEGER NOT NULL,
        cores INTEGER NOT NULL,
        threads INTEGER NOT NULL,
        frequency REAL NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ram (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL CHECK(category IN ('gaming', 'work', 'graphics', 'budget')),
        price INTEGER NOT NULL,
        capacity INTEGER NOT NULL,
        speed INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gpus (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL CHECK(category IN ('gaming', 'work', 'graphics', 'budget')),
        price INTEGER NOT NULL,
        vram INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS power_supplies (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL CHECK(category IN ('gaming', 'work', 'graphics', 'budget')),
        price INTEGER NOT NULL,
        wattage INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS storage (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL CHECK(category IN ('gaming', 'work', 'graphics', 'budget')),
        price INTEGER NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('SSD', 'HDD')),
        capacity INTEGER NOT NULL
    );
    """)

    conn.commit()
    conn.close()

create_components_tables()

def delete_unsaved_build(user_id):
    """Удаляет несохраненную сборку через 15 минут."""
    if user_id in active_builds:
        del active_builds[user_id]
        bot.send_message(
            user_id,
            "Ваша сборка была удалена, так как не была сохранена в течение 15 минут."
        )

# Распределение бюджета
def calculate_budget_distribution(budget):
    """Распределяет бюджет между компонентами."""
    return {
        "processor": (int(budget * 0.25), int(budget * 0.35)),
        "gpu": (int(budget * 0.3), int(budget * 0.4)),
        "ram": (int(budget * 0.1), int(budget * 0.15)),
        "power_supply": (int(budget * 0.1), int(budget * 0.2)),
        "storage": (int(budget * 0.1), int(budget * 0.15)),
    }

# Обработчик команды /start
# @bot.message_handler(commands=["start"])
# def start(message):
#     """Приветствие и показ главного меню."""
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add("Создать сборку", "Сохранённые сборки")
#     bot.send_message(
#         message.chat.id,
#         "Привет! Я помогу подобрать комплектующие. Выберите действие:",
#         reply_markup=keyboard
#     )

# Создание сборки
@bot.message_handler(func=lambda message: message.text == "Создать сборку")
def ask_budget(message):
    """Спрашивает бюджет сборки."""
    bot.send_message(message.chat.id, "Введите бюджет для сборки (в рублях):")
    bot.register_next_step_handler(message, ask_purpose)

def ask_purpose(message):
    """Спрашивает назначение сборки."""
    try:
        budget = int(message.text)
        if budget <= 0:
            raise ValueError

        user_id = message.from_user.id
        active_builds[user_id] = {"budget": budget, "components": {}, "purpose": None, "name": None}

        Timer(900, delete_unsaved_build, args=[user_id]).start()  # Удаление через 15 минут

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Игровая", "Рабочая", "Для графики", "Бюджетная")
        bot.send_message(
            message.chat.id,
            "Каково назначение сборки?",
            reply_markup=keyboard
        )
        bot.register_next_step_handler(message, select_component)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число для бюджета.")
        bot.register_next_step_handler(message, ask_budget)

def select_component(message):
    """Начинает подбор компонентов."""
    user_id = message.from_user.id
    if user_id not in active_builds:
        bot.send_message(message.chat.id, "Что-то пошло не так. Начните сборку заново.")
        return

    active_builds[user_id]["purpose"] = message.text
    bot.send_message(message.chat.id, "Теперь давайте подберем комплектующие!")
    ask_component(message, "processor")

def ask_component(message, component):
    """Подбирает комплектующие для выбранной категории."""
    user_id = message.from_user.id
    if user_id not in active_builds:
        bot.send_message(message.chat.id, "Что-то пошло не так. Начните сборку заново.")
        return

    budget = active_builds[user_id]["budget"]
    purpose = active_builds[user_id]["purpose"]
    distribution = calculate_budget_distribution(budget)
    min_price, max_price = distribution[component]

    # Обновленный запрос на получение комплектующих
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT name, price FROM {component}s
        WHERE category = ? AND price BETWEEN ? AND ?
    """, (purpose, min_price, max_price))
    options = cursor.fetchall()
    conn.close()

    if not options:
        bot.send_message(message.chat.id, f"Не найдено компонентов для {component}. Пропускаем.")
        next_component(message, component)
        return

    # Создаем кнопки для выбора
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for option in options:
        keyboard.add(f"{option[0]} ({option[1]} руб)")

    bot.send_message(
        message.chat.id,
        f"Выберите {component}:",
        reply_markup=keyboard
    )
    bot.register_next_step_handler(message, lambda msg: save_component(msg, component))

def save_component(message, component):
    """Сохраняет выбранный компонент."""
    user_id = message.from_user.id
    if user_id not in active_builds:
        bot.send_message(message.chat.id, "Что-то пошло не так. Начните сборку заново.")
        return

    choice = message.text.split(" (")[0]
    active_builds[user_id]["components"][component] = choice
    next_component(message, component)

def next_component(message, current_component):
    """Переходит к следующему компоненту."""
    components = ["processor", "gpu", "ram", "power_supply", "storage"]
    next_index = components.index(current_component) + 1
    if next_index < len(components):
        ask_component(message, components[next_index])
    else:
        finish_build(message)

def finish_build(message):
    """Завершает сборку и предлагает сохранить."""
    user_id = message.from_user.id
    build = active_builds[user_id]

    summary = "\n".join(
        [f"{component.capitalize()}: {name}" for component, name in build["components"].items()]
    )
    bot.send_message(
        message.chat.id,
        f"Сборка завершена!\n\nВаш выбор:\n{summary}\n\nВведите название для сборки:"
    )
    bot.register_next_step_handler(message, save_build_name)

def save_build_name(message):
    """Сохраняет название сборки и предлагает её сохранить."""
    user_id = message.from_user.id
    if user_id not in active_builds:
        bot.send_message(message.chat.id, "Что-то пошло не так. Начните сборку заново.")
        return

    active_builds[user_id]["name"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Сохранить сборку", "Не сохранять")
    bot.send_message(message.chat.id, "Сохранить эту сборку?", reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_save_choice)

def handle_save_choice(message):
    """Обрабатывает выбор пользователя о сохранении сборки."""
    user_id = message.from_user.id
    if user_id not in active_builds:
        bot.send_message(message.chat.id, "Что-то пошло не так. Начните сборку заново.")
        return

    if message.text == "Сохранить сборку":
        build = active_builds[user_id]
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_builds (user_id, name, processor_id, gpu_id, ram_id, power_supply_id, storage_id, budget, purpose)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            build["name"],
            build["components"].get("processor"),
            build["components"].get("gpu"),
            build["components"].get("ram"),
            build["components"].get("power_supply"),
            build["components"].get("storage"),
            build["budget"],
            build["purpose"]
        ))
        conn.commit()
        conn.close()

        bot.send_message(message.chat.id, "Сборка успешно сохранена!")
    else:
        bot.send_message(message.chat.id, "Сборка не сохранена.")

    del active_builds[user_id]

bot.polling()
