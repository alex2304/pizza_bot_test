import traceback

from platforms.telegram.bot_src import bot
# some python change for testing pep8speaks bot
def start():
    try:
        bot.polling(none_stop=True)
    except:
        traceback.print_exc()


if __name__ == '__main__':
    start()
