import logging

import pyotp
from telegram import Message, Update
from telegram.ext import CallbackContext

from ..helpers import persistence
from ..helpers.keyboards import show_keyboard

logger = logging.getLogger(__name__)


async def cbk_show(update: Update, _: CallbackContext) -> None:
    if (cbk := update.callback_query) and (data := cbk.data):
        await cbk.answer()
        name = "__".join(data.split("__")[1:])
        if msg := cbk.message:
            seed = persistence.get(str(msg.chat.id), name)
            otp = pyotp.TOTP(seed)
            await cbk.edit_message_text(
                f"OTP for {name}: {otp.now()}",
                reply_markup=show_keyboard(name),
            )
        else:
            logger.error("Called cbk_show with no message")


async def cbk_refresh(update: Update, _: CallbackContext) -> None:
    if (cbk := update.callback_query) and (data := cbk.data):
        await cbk.answer()
        name = "__".join(data.split("__")[1:])
        if (msg := cbk.message) and isinstance(msg, Message):
            seed = persistence.get(str(msg.chat.id), name)
            otp = pyotp.TOTP(seed)
            if raw_old_otp := msg.text:
                oldotp = raw_old_otp.split(" ")[-1]
                newotp = otp.now()
                if oldotp != newotp:
                    await cbk.edit_message_text(
                        f"OTP for {name}: {newotp}",
                        reply_markup=show_keyboard(name),
                    )
            else:
                logger.error("Unable to retrieve old OTP on refresh")
        else:
            logger.error("Called cbk_show with no message")
