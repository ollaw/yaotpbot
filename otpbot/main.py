import logging
import os

from telegram.ext import CallbackQueryHandler, CommandHandler, Updater

from .cmds.help import cmd_help
from .cmds.start import cmd_start
from .constant import (
    CBK_DATA_HOME,
    CBK_DATA_LIST,
    CBK_DATA_REFRESH,
    CBK_DATA_REMOVE,
    CBK_DATA_REMOVE_LIST,
    CBK_DATA_RM_N,
    CBK_DATA_RM_Y,
    CBK_DATA_SHOW,
    CMD_HELP,
    CMD_START,
    TOKEN_ENV_VAR,
)
from .handlers.add import cnvs_hdl_add
from .handlers.delete import cbk_rm, cbk_rm_confirm_n, cbk_rm_confirm_y, cbk_rm_ls
from .handlers.list import cbk_ls
from .handlers.show import cbk_refresh, cbk_show
from .handlers.start import cbk_home
from .helpers.env import check_environments

logger = logging.getLogger(__name__)


def main() -> None:

    check_environments()

    """Start the bot."""
    updater = Updater(os.getenv(TOKEN_ENV_VAR))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # -- Commands
    dispatcher.add_handler(CommandHandler(CMD_START, cmd_start))
    dispatcher.add_handler(CommandHandler(CMD_HELP, cmd_help))

    # -- Conversation handlers
    dispatcher.add_handler(cnvs_hdl_add())  # add

    # -- Callback query

    # Back home callback
    dispatcher.add_handler(CallbackQueryHandler(cbk_home, pattern=CBK_DATA_HOME))
    # List applications callback
    dispatcher.add_handler(CallbackQueryHandler(cbk_ls, pattern=CBK_DATA_LIST))

    # Manage remove
    dispatcher.add_handler(
        CallbackQueryHandler(cbk_rm_ls, pattern=CBK_DATA_REMOVE_LIST)
    )
    dispatcher.add_handler(CallbackQueryHandler(cbk_rm, pattern=CBK_DATA_REMOVE))
    dispatcher.add_handler(
        CallbackQueryHandler(cbk_rm_confirm_y, pattern=CBK_DATA_RM_Y)
    )
    dispatcher.add_handler(
        CallbackQueryHandler(cbk_rm_confirm_n, pattern=CBK_DATA_RM_N)
    )

    # Manage show
    dispatcher.add_handler(
        CallbackQueryHandler(cbk_show, pattern=f"{CBK_DATA_SHOW}__.*")
    )
    dispatcher.add_handler(
        CallbackQueryHandler(cbk_refresh, pattern=f"{CBK_DATA_REFRESH}__.*")
    )

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
