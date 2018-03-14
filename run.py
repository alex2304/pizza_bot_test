import traceback

from platforms.telegram.bot_src import bot


def start():
    try:
        bot.polling(none_stop=True)

    except:
        traceback.print_exc()


if __name__ == '__main__':
    start()
