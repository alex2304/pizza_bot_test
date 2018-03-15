from telebot import types

from src.user_session import UserSession

sessions = {}


def get_user_session(chat_id) -> UserSession:
    if sessions.get(chat_id) is None:
        sessions[chat_id] = UserSession(chat_id)

    return sessions[chat_id]


def make_kb_markup(*buttons):
    if not buttons:
        return None

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    markup.row(*buttons)

    return markup
