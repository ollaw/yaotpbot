from telegram import Update
from telegram.ext import CallbackContext


async def cmd_help(update: Update, _: CallbackContext) -> None:
    if msg := update.message:
        await msg.reply_text("You can start the bot typing /start.")
