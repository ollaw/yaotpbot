import logging

from telegram import Update
from telegram.ext import CallbackContext

from ..helpers.keyboards import ls_keyboard

logger = logging.getLogger(__name__)


def cbk_ls(update: Update, context: CallbackContext) -> None:
    if cbk := update.callback_query:
        context.bot.answer_callback_query(cbk.id)
        if msg := cbk.message:
            context.bot.edit_message_text(
                "Select the application to show 👀",
                chat_id=msg.chat.id,
                message_id=msg.message_id,
                reply_markup=ls_keyboard(str(msg.chat.id)),
            )
        else:
            logger.error("Called cbk_rm_ls with no mesage")
