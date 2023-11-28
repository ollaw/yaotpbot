import logging
from binascii import Error

import pyotp
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    filters,
    MessageHandler,
)

from ..constant import (
    CBK_DATA_ADD,
    CMD_CANCEL,
    ST_ADD_NAME,
    ST_ADD_OPT,
    USER_DATA_KEY_ADD_MSG_ID,
    USER_DATA_KEY_ADD_NAME,
)
from ..handlers.cancel import cbk_cancel
from ..helpers import keyboards, persistence

logger = logging.getLogger(__name__)


def cbk_add(update: Update, context: CallbackContext) -> int:
    if cbk := update.callback_query:
        context.bot.answer_callback_query(cbk.id)
        if msg := update.callback_query.message:
            context.bot.send_message(
                chat_id=msg.chat.id,
                text="Let's insert a new one. How should we call it? 💬\n"
                "Run /cancel command to abort.",
            )
            return ST_ADD_NAME
        else:
            logger.error("Called cbk_add with no message")
    return -1


def cbk_on_name(update: Update, context: CallbackContext) -> int:
    if (oldmsg := update.message) and ((userdata := context.user_data) is not None):
        userdata[USER_DATA_KEY_ADD_NAME] = update.message.text
        msg = oldmsg.reply_text(f"Great! Now insert the OTP seed for {oldmsg.text} 🎲🎲")
        userdata[USER_DATA_KEY_ADD_MSG_ID] = msg.message_id
        return ST_ADD_OPT
    logger.error("Called cbk_on_name with no message")
    return -1


def cbk_on_otp(update: Update, context: CallbackContext) -> int:

    if (
        (msg := update.message)
        and (txt := msg.text)
        and ((userdata := context.user_data) is not None)
    ):
        try:
            otp = pyotp.TOTP(txt)
            otp.now()
        except Error:
            name = userdata[USER_DATA_KEY_ADD_NAME]
            msg = msg.reply_text(
                f"😨😨 Oooops! Seems like this seed is invalid.\nInsert again the seed for {name} 🎲🎲"
            )
            userdata[USER_DATA_KEY_ADD_MSG_ID] = msg.message_id
            return ST_ADD_OPT

        persistence.put(
            str(msg.chat.id),
            userdata[USER_DATA_KEY_ADD_NAME],
            str(txt),
        )
        context.bot.delete_message(
            chat_id=msg.chat.id,
            message_id=userdata[USER_DATA_KEY_ADD_MSG_ID],
        )
        msg.delete()
        msg.reply_text(
            "🥳🥳 OTP successfully added.. I hid the seed for you 🤐\n" "What now?",
            reply_markup=keyboards.default_keyboard(),
        )
        return ConversationHandler.END

    logger.error(
        "Called cbk_on_otp with no message or no text on message or no user data."
    )
    return -1


def cnvs_hdl_add() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CallbackQueryHandler(cbk_add, pattern=CBK_DATA_ADD)],
        states={
            ST_ADD_NAME: [MessageHandler(filters.text & ~filters.command, cbk_on_name)],
            ST_ADD_OPT: [MessageHandler(filters.text & ~filters.command, cbk_on_otp)],
        },
        fallbacks=[CommandHandler(CMD_CANCEL, cbk_cancel)],
    )
