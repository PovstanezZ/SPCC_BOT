# import os
# import sqlite3
# import telebot
# from telebot import TeleBot, types
# from threading import Timer
# from telegramBot.config import API
#
# # Путь к базе данных
# dbPath = os.path.join('D:', 'SPCC_BOT', 'DataBase', 'PCBuild.db')
# # Настройка бота
# bot = TeleBot(API)
#
#
# # Словарь для временного хранения сборок
# active_builds = {}
#
# def connect_db():
#     conn = sqlite3.connect(dbPath)
#     return conn
#
# # Удаление несохранённой сборки через 15 минут
# def delete_unsaved_build(user_id):
#     if user_id in active_builds:
#         del active_builds[user_id]
#         bot.send_message(user_id, "Ваша сборка была удалена, так как не была сохранена в течение 15 минут.")
#
# # Распределение бюджета
# def calculate_budget_distribution(budget):
#     """Распределяет бюджет между компонентами."""
#     return {
#         "processor": (int(budget * 0.25), int(budget * 0.35)),
#         "gpu": (int(budget * 0.3), int(budget * 0.4)),
#         "ram": (int(budget * 0.1), int(budget * 0.15)),
#         "power_supply": (int(budget * 0.1), int(budget * 0.2)),
#         "storage": (int(budget * 0.1), int(budget * 0.15)),
#     }
#
# # Регистрация пользователя
# @bot.message_handler(commands=["start"])
# def register_user(message):
#     conn = connect_db()
#     cursor = conn.cursor()
#     user_id = message.from_user.id
#     username = message.from_user.username
#     first_name = message.from_user.first_name
#     last_name = message.from_user.last_name
#
#     cursor.execute("""
#         INSERT OR IGNORE INTO users (telegram_id, username, first_name, last_name)
#         VALUES (?, ?, ?, ?)
#     """, (user_id, username, first_name, last_name))
#     conn.commit()
#     conn.close()
#     bot.send_message(message.chat.id, "Добро пожаловать! Вы зарегистрированы.")
#
# # Создание сборки
# @bot.message_handler(func=lambda message: message.text == "Создать сборку")
# def ask_budget(message):
#     """Спрашивает бюджет сборки."""
#     bot.send_message(message.chat.id, "Введите бюджет для сборки (в рублях):")
#     bot.register_next_step_handler(message, ask_purpose)
#
# def ask_purpose(message):
#     """Спрашивает назначение сборки."""
#     try:
#         budget = int(message.text)
#         if budget <= 0:
#             raise ValueError
#
#         user_id = message.from_user.id
#         active_builds[user_id] = {"budget": budget, "components": {}, "purpose": None, "name": None}
#
#         Timer(900, delete_unsaved_build, args=[user_id]).start()
#
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         keyboard.add("Игровая", "Рабочая", "Для графики", "Бюджетная")
#         bot.send_message(
#             message.chat.id,
#             "Каково назначение сборки?",
#             reply_markup=keyboard
#         )
#         bot.register_next_step_handler(message, select_component)
#     except ValueError:
#         bot.send_message(message.chat.id, "Пожалуйста, введите корректное число для бюджета.")
#         bot.register_next_step_handler(message, ask_budget)
#
# def select_component(message):
#     """Начинает подбор компонентов."""
#     user_id = message.from_user.id
#     if user_id not in active_builds:
#         bot.send_message(message.chat.id, "Что-то пошло не так. Начните сборку заново.")
#         return
#
#     active_builds[user_id]["purpose"] = message.text.lower()
#     bot.send_message(message.chat.id, "Теперь давайте подберем комплектующие!")
#     ask_component(message, "processor")
#
# def ask_component(message, component):
#     """Подбирает комплектующие для выбранной категории."""
#     user_id = message.from_user.id
#     if user_id not in active_builds:
#         bot.send_message(message.chat.id, "Что-то пошло не так. Начните сборку заново.")
#         return
#
#     budget = active_builds[user_id]["budget"]
#     purpose = active_builds[user_id]["purpose"]
#     distribution = calculate_budget_distribution(budget)
#     min_price, max_price = distribution[component]
#
#     conn = connect_db()
#     cursor = conn.cursor()
#     cursor.execute(f"""
#         SELECT id, name, price FROM {component}s
#         WHERE category = ? AND price BETWEEN ? AND ?
#     """, (purpose, min_price, max_price))
#     options = cursor.fetchall()
#     conn.close()
#
#     if not options:
#         bot.send_message(message.chat.id, f"Не найдено компонентов для {component}. Пропускаем.")
#         next_component(message, component)
#         return
#
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     for option in options:
#         keyboard.add(f"{option[1]} ({option[2]} руб)")
#
#     bot.send_message(
#         message.chat.id,
#         f"Выберите {component}:",
#         reply_markup=keyboard
#     )
#     bot.register_next_step_handler(message, lambda msg: save_component(msg, component))
#
# def save_component(message, component):
#     """Сохраняет выбранный компонент."""
#     user_id = message.from_user.id
#     if user_id not in active_builds:
#         bot.send_message(message.chat.id, "Что-то пошло не так. Начните сборку заново.")
#         return
#
#     choice = message.text.split(" (")[0]
#     active_builds[user_id]["components"][component] = choice
#     next_component(message, component)
#
# def next_component(message, current_component):
#     """Переходит к следующему компоненту."""
#     components = ["processor", "gpu", "ram", "power_supply", "storage"]
#     next_index = components.index(current_component) + 1
#     if next_index < len(components):
#         ask_component(message, components[next_index])
#     else:
#         finish_build(message)
#
# def finish_build(message):
#     """Завершает сборку и предлагает сохранить."""
#     user_id = message.from_user.id
#     build = active_builds[user_id]
#
#     summary = "\n".join(
#         [f"{component.capitalize()}: {name}" for component, name in build["components"].items()]
#     )
#     bot.send_message(
#         message.chat.id,
#         f"Сборка завершена!\n\nВаш выбор:\n{summary}\n\nВведите название для сборки:"
#     )
#     bot.register_next_step_handler(message, save_build_name)
#
# def save_build_name(message):
#     """Сохраняет название сборки и предлагает её сохранить."""
#     user_id = message.from_user.id
#     if user_id not in active_builds:
#         bot.send_message(message.chat.id, "Что-то пошло не так. Начните сборку заново.")
#         return
#
#     active_builds[user_id]["name"] = message.text
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add("Сохранить сборку", "Не сохранять")
#     bot.send_message(message.chat.id, "Сохранить эту сборку?", reply_markup=keyboard)
#     bot.register_next_step_handler(message, handle_save_choice)
#
# def handle_save_choice(message):
#     """Обрабатывает выбор пользователя о сохранении сборки."""
#     user_id = message.from_user.id
#     if user_id not in active_builds:
#         bot.send_message(message.chat.id, "Что-то пошло не так. Начните сборку заново.")
#         return
#
#     if message.text == "Сохранить сборку":
#         build = active_builds[user_id]
#         conn = connect_db()
#         cursor = conn.cursor()
#
#         # Запрос для сохранения сборки
#         cursor.execute("""
#             INSERT INTO user_builds (user_id, name, processor_id, gpu_id, ram_id, power_supply_id, storage_id, budget, purpose)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """, (
#             user_id,
#             build["name"],
#             build["components"].get("processor"),
#             build["components"].get("gpu"),
#             build["components"].get("ram"),
#             build["components"].get("power_supply"),
#             build["components"].get("storage"),
#             build["budget"],
#             build["purpose"]
#         ))
#         conn.commit()
#         conn.close()
#
#         bot.send_message(message.chat.id, "Сборка успешно сохранена!")
#     else:
#         bot.send_message(message.chat.id, "Сборка не сохранена.")
#
#     del active_builds[user_id]
#
# # Запуск бота
# bot.infinity_polling()
