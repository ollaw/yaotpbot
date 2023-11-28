import logging

from telegram import Update
from telegram.ext import CallbackContext

from ..constant import USER_DATA_KEY_DEL_NAME
from ..helpers import persistence
from ..helpers.keyboards import default_keyboard, ls_rm_keyboard, rm_keyboard

logger = logging.getLogger(__name__)


def cbk_rm_ls(update: Update, context: CallbackContext) -> None:
    if cbk := update.callback_query:
        context.bot.answer_callback_query(cbk.id)
        if msg := cbk.message:
            context.bot.edit_message_text(
                "Select the application to remove 🗑🗑",
                chat_id=msg.chat.id,
                message_id=msg.message_id,
                reply_markup=ls_rm_keyboard(str(msg.chat.id)),
            )
        else:
            logger.error("Called cbk_rm_ls with no mesage")


def cbk_rm(update: Update, context: CallbackContext) -> None:
    if (
        (cbk := update.callback_query)
        and (data := cbk.data)
        and (userdata := context.user_data)
    ):
        name = "__".join(data.split("__")[1:])
        if msg := cbk.message:
            if persistence.exists(str(msg.chat_id), name):
                userdata[USER_DATA_KEY_DEL_NAME] = name
                context.bot.edit_message_text(
                    f"🥺🥺 Are you sure you want to delete {name}?",
                    chat_id=msg.chat.id,
                    message_id=msg.message_id,
                    reply_markup=rm_keyboard(),
                )

            else:
                context.bot.edit_message_text(
                    f"Oooops, seems like '{name}' isn't your OTPs 🤷🏻‍♂️\nWhat now?",
                    chat_id=msg.chat.id,
                    message_id=msg.message_id,
                    reply_markup=default_keyboard(),
                )
    else:
        logger.error(
            "Called cbk_on_otp with no message or no text on message or no user data."
        )


def cbk_rm_confirm_y(update: Update, context: CallbackContext) -> None:
    if (cbk := update.callback_query) and (userdata := context.user_data):
        context.bot.answer_callback_query(cbk.id)
        otp_name = userdata[USER_DATA_KEY_DEL_NAME]
        if msg := cbk.message:
            persistence.delete(str(msg.chat.id), otp_name)
            context.bot.edit_message_text(
                chat_id=msg.chat.id,
                message_id=msg.message_id,
                text=f"🥳🥳 OTP {otp_name} successfully deleted!\nWhat now?",
                reply_markup=default_keyboard(),
            )
        else:
            logger.error("Called cbk_rm_ls with no mesage")


def cbk_rm_confirm_n(update: Update, context: CallbackContext) -> None:
    if cbk := update.callback_query:
        context.bot.answer_callback_query(cbk.id)
        if msg := cbk.message:
            context.bot.edit_message_text(
                chat_id=msg.chat.id,
                message_id=msg.message_id,
                text="✌️✌️ Nevermind, let's start again. \nWhat to do?",
                reply_markup=default_keyboard(),
            )
        else:
            logger.error("Called cbk_rm_ls with no mesage")
