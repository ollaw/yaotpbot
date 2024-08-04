from telegram import Update
from telegram.ext import CallbackContext

from ..helpers.keyboards import default_keyboard


async def cbk_home(update: Update, _: CallbackContext) -> None:
    if cbk := update.callback_query:
        await cbk.answer()
        if update.message:
            await update.message.reply_text(
                "Choose somethind to do!", reply_markup=default_keyboard()
            )
        elif cbk.message:
            await cbk.edit_message_text(
                text="Choose somethind to do!",
                reply_markup=default_keyboard(),
            )
