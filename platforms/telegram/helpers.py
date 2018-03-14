from telebot import types

from src.sessions import UserSession

sessions = {}


def get_session(chat_id):
    if sessions.get(chat_id) is None:
        sessions[chat_id] = UserSession(chat_id)

    return sessions[chat_id]


def make_kb_markup(*buttons):
    if not buttons:
        return None

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    markup.row(*buttons)

    return markup
