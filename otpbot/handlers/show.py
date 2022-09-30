import logging

import pyotp
from telegram import Update
from telegram.ext import CallbackContext

from ..helpers import persistence
from ..helpers.keyboards import show_keyboard

logger = logging.getLogger(__name__)


def cbk_show(update: Update, context: CallbackContext) -> None:
    if (cbk := update.callback_query) and (data := cbk.data):
        context.bot.answer_callback_query(cbk.id)
        name = "__".join(data.split("__")[1:])
        if msg := cbk.message:
            seed = persistence.get(str(msg.chat.id), name)
            otp = pyotp.TOTP(seed)
            context.bot.edit_message_text(
                f"OTP for {name}: {otp.now()}",
                chat_id=msg.chat.id,
                message_id=msg.message_id,
                reply_markup=show_keyboard(name),
            )
        else:
            logger.error("Called cbk_show with no message")


def cbk_refresh(update: Update, context: CallbackContext) -> None:
    if (cbk := update.callback_query) and (data := cbk.data):
        context.bot.answer_callback_query(cbk.id)
        name = "__".join(data.split("__")[1:])
        if msg := cbk.message:
            seed = persistence.get(str(msg.chat.id), name)
            otp = pyotp.TOTP(seed)
            if raw_old_otp := msg.text:
                oldotp = raw_old_otp.split(" ")[-1]
                newotp = otp.now()
                if oldotp != newotp:
                    context.bot.edit_message_text(
                        f"OTP for {name}: {newotp}",
                        chat_id=msg.chat.id,
                        message_id=msg.message_id,
                        reply_markup=show_keyboard(name),
                    )
            else:
                logger.error("Unable to retrieve old OTP on refresh")
        else:
            logger.error("Called cbk_show with no message")
