# from buttons import create_keyboard
#
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     keyboard = create_keyboard()
#     bot.send_message(message.chat.id, "Выберите кнопку:", reply_markup=keyboard)
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback_handler(call):
#     if call.data == "button1":
#         bot.send_message(call.message.chat.id, "Вы нажали кнопку 1!")
#     elif call.data == "button2":
#         bot.send_message(call.message.chat.id, "Вы нажали кнопку 2!")
#     elif call.data == "button3":
#         bot.send_message(call.message.chat.id, "Вы нажали кнопку 3!")
#
