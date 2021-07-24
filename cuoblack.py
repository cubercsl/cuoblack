#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

from telegram import Bot, Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext import (Updater, CommandHandler)

token = os.getenv('TELEGRAM_APITOKEN')
bot = Bot(token=token)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    print(context.error)


def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, '/cuoblack')


def cuoblack(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    reply_to_message_id = update.message.reply_to_message.message_id \
        if update.message.reply_to_message else None
    with open(os.path.join(os.path.dirname(__file__),
                           os.getenv('CUOBLACK', 'cuoblack.webp')), 'rb') as sticker:
        context.bot.send_sticker(chat_id, sticker, reply_to_message_id=reply_to_message_id)

def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # log all errors
    dp.add_error_handler(error)

    # add handler
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("cuoblack", cuoblack))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
