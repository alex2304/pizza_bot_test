import os
from typing import Union, Any

import telebot

from platforms.telegram.helpers import get_user_session, make_kb_markup
from src.dialog_engine import DialogEngine

bot = telebot.TeleBot(os.environ.get('TELEGRAM_BOT_TOKEN'),
                      threaded=False)


@bot.message_handler(commands=['start', 'help'])
def handle_commands(message):
    chat_id = str(message.chat.id)

    session = get_user_session(chat_id)

    if session.state == 'initial':
        messages = DialogEngine.process_message(session, 'initial')

        send_messages(chat_id, messages)

    else:
        bot.reply_to(message, "Я - бот для заказа пиццы. Чтобы сделать заказ, следуй моим инструкциям")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    message_text = message.text

    chat_id = str(message.chat.id)

    session = get_user_session(chat_id)

    answer_messages = DialogEngine.process_message(session, message_text)

    send_messages(chat_id, answer_messages)


def send_messages(chat_id, messages: Union[list, Any]):
    if not isinstance(messages, list):
        messages = [messages]

    for msg in messages:
        message_text, kb_markup = msg['message'], make_kb_markup(*msg.get('options', []))

        bot.send_message(chat_id, message_text, reply_markup=kb_markup)
