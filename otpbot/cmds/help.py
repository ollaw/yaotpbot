from telegram import Update
from telegram.ext import CallbackContext


def cmd_help(update: Update, _: CallbackContext) -> None:
    if msg := update.message:
        msg.reply_text("You can start the bot typing /start.")
