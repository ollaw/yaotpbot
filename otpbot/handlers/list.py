import logging

from telegram import Update
from telegram.ext import CallbackContext

from ..helpers.keyboards import ls_keyboard

logger = logging.getLogger(__name__)


async def cbk_ls(update: Update, _: CallbackContext) -> None:
    if cbk := update.callback_query:
        await cbk.answer()
        if msg := cbk.message:
            await cbk.edit_message_text(
                "Select the application to show 👀",
                reply_markup=ls_keyboard(str(msg.chat.id)),
            )
        else:
            logger.error("Called cbk_rm_ls with no mesage")
