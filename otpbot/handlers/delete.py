import logging

from telegram import Update
from telegram.ext import CallbackContext

from ..constant import USER_DATA_KEY_DEL_NAME
from ..helpers import persistence
from ..helpers.keyboards import default_keyboard, ls_rm_keyboard, rm_keyboard

logger = logging.getLogger(__name__)


async def cbk_rm_ls(update: Update, _: CallbackContext) -> None:
    if cbk := update.callback_query:
        await cbk.answer()
        if msg := cbk.message:
            await cbk.edit_message_text(
                "Select the application to remove 🗑🗑",
                reply_markup=ls_rm_keyboard(str(msg.chat.id)),
            )
        else:
            logger.error("Called cbk_rm_ls with no mesage")


async def cbk_rm(update: Update, context: CallbackContext) -> None:
    if (
        (cbk := update.callback_query)
        and (data := cbk.data)
        and (userdata := context.user_data)
    ):
        name = "__".join(data.split("__")[1:])
        if msg := cbk.message:
            if persistence.exists(str(msg.chat.id), name):
                userdata[USER_DATA_KEY_DEL_NAME] = name
                await cbk.edit_message_text(
                    f"🥺🥺 Are you sure you want to delete {name}?",
                    reply_markup=rm_keyboard(),
                )

            else:
                await cbk.edit_message_text(
                    f"Oooops, seems like '{name}' isn't your OTPs 🤷🏻‍♂️\nWhat now?",
                    reply_markup=default_keyboard(),
                )
    else:
        logger.error(
            "Called cbk_on_otp with no message or no text on message or no user data."
        )


async def cbk_rm_confirm_y(update: Update, context: CallbackContext) -> None:
    if (cbk := update.callback_query) and (userdata := context.user_data):
        await cbk.answer()
        otp_name = userdata[USER_DATA_KEY_DEL_NAME]
        if msg := cbk.message:
            persistence.delete(str(msg.chat.id), otp_name)
            await cbk.edit_message_text(
                text=f"🥳🥳 OTP {otp_name} successfully deleted!\nWhat now?",
                reply_markup=default_keyboard(),
            )
        else:
            logger.error("Called cbk_rm_ls with no mesage")


async def cbk_rm_confirm_n(update: Update, _: CallbackContext) -> None:
    if cbk := update.callback_query:
        await cbk.answer()
        if cbk.message:
            await cbk.edit_message_text(
                text="✌️✌️ Nevermind, let's start again. \nWhat to do?",
                reply_markup=default_keyboard(),
            )
        else:
            logger.error("Called cbk_rm_ls with no mesage")
