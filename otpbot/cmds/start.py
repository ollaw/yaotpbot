from telegram import Update
from telegram.ext import CallbackContext

from ..helpers.keyboards import default_keyboard


def cmd_start(update: Update, _: CallbackContext) -> None:
    if msg := update.message:
        msg.reply_text("Choose somethind to do!", reply_markup=default_keyboard())
