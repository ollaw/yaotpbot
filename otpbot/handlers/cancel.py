import logging

from telegram import Update
from telegram.ext import CallbackContext

from ..helpers.keyboards import default_keyboard

logger = logging.getLogger(__name__)


async def cbk_cancel(update: Update, context: CallbackContext) -> None:
    from .add import cnvs_hdl_add

    context.application.add_handler(cnvs_hdl_add())
    if msg := update.message:
        await msg.reply_text(
            "Okay, let's start again..\nChoose somethind to do!",
            reply_markup=default_keyboard(),
        )
    else:
        logger.error("Called cbk_rm_ls with no mesage")
