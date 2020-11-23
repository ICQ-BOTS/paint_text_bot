from handlers import *
from mailru_im_async_bot.filter import Filter
from mailru_im_async_bot.bot import Bot
from mailru_im_async_bot.handler import MessageHandler, DefaultHandler, StartCommandHandler, BotButtonCommandHandler
from logging.config import fileConfig
from pid import PidFile
import logging
import asyncio
import sys
import os


configs_path = os.path.realpath(os.path.dirname(sys.argv[0])) + "/"

if not os.path.isfile(os.path.join(configs_path, "logging.ini")):
    raise FileExistsError(f"File logging.ini not found in path {configs_path}")

logging.config.fileConfig(os.path.join(configs_path, "logging.ini"), disable_existing_loggers=False)
log = logging.getLogger(__name__)

NAME = "paint_text"
TOKEN = "***.**********.**********:*********"

loop = asyncio.get_event_loop()

bot = Bot(token=TOKEN, name=NAME)


# Register your handlers here
# ---------------------------------------------------------------------
bot.dispatcher.add_handler(StartCommandHandler(callback=start))
bot.dispatcher.add_handler(MessageHandler(
                            callback=media, 
                            filters=Filter.media
                        )
                    )
bot.dispatcher.add_handler(MessageHandler(
        callback=media,
        filters=Filter.sticker
    )
)
# Нужен фон стола
bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=button_1,
        filters=Filter.callback_data('call_back_id_1')
    )
)
# Не нужен фон стола
bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=button_2,
        filters=Filter.callback_data('call_back_id_2')
    )
)
bot.dispatcher.add_handler(DefaultHandler(
        callback=write_text
    )
)


with PidFile(NAME):
    try:
        loop.create_task(bot.start_polling())
        loop.run_forever()
    finally:
        loop.close()
