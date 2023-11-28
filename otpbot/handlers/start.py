from telegram import Update
from telegram.ext import CallbackContext

from ..helpers.keyboards import default_keyboard


def cbk_home(update: Update, context: CallbackContext) -> None:
    if cbk := update.callback_query:
        context.bot.answer_callback_query(cbk.id)
        if update.message:
            update.message.reply_text(
                "Choose somethind to do!", reply_markup=default_keyboard()
            )
        elif msg := cbk.message:
            context.bot.edit_message_text(
                chat_id=msg.chat.id,
                message_id=msg.message_id,
                text="Choose somethind to do!",
                reply_markup=default_keyboard(),
            )
