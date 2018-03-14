import os

import telebot

from platforms.telegram.helpers import get_session, make_kb_markup

bot = telebot.TeleBot(os.environ.get('TELEGRAM_BOT_TOKEN', '455155698:AAE7ZfKhl8gn78Sc1lU30k8_ymaTHXT08rU'),
                      threaded=False)


@bot.message_handler(commands=['start', 'help'])
def handle_commands(message):
    bot.reply_to(message, "Я - бот для заказа пиццы. Чтобы сделать заказ, следуй моим инструкциям")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    message_text = message.text

    chat_id = str(message.chat.id)

    session = get_session(chat_id)

    screens = session.get_messages(message_text)

    if not isinstance(screens, list):
        screens = [screens]

    for screen in screens:
        message_text, kb_markup = screen['message'], make_kb_markup(*screen.get('options', []))

        bot.send_message(chat_id, message_text, reply_markup=kb_markup)
