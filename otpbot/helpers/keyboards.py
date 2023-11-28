from typing import List, Tuple

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from ..constant import (
    BTN_ADD_LABEL,
    BTN_BACK_LABEL,
    BTN_LIST_LABEL,
    BTN_REFRESH_LABEL,
    BTN_REMOVE_LABEL,
    BTN_REMOVE_N_LABEL,
    BTN_REMOVE_Y_LABEL,
    CBK_DATA_ADD,
    CBK_DATA_HOME,
    CBK_DATA_LIST,
    CBK_DATA_REFRESH,
    CBK_DATA_REMOVE,
    CBK_DATA_REMOVE_LIST,
    CBK_DATA_RM_N,
    CBK_DATA_RM_Y,
    CBK_DATA_SHOW,
    LIST_ROW_LENGTH,
)
from . import persistence


def default_keyboard() -> InlineKeyboardMarkup:
    """
    Default keyboard.
    """
    return _keyboard(
        [
            [
                (BTN_ADD_LABEL, CBK_DATA_ADD),
                (BTN_REMOVE_LABEL, CBK_DATA_REMOVE_LIST),
                (BTN_LIST_LABEL, CBK_DATA_LIST),
            ]
        ]
    )


def add_name_keyboard() -> InlineKeyboardMarkup:
    """
    Keyboard used when a new OTP name is excpected in input.
    """
    return _keyboard([[(BTN_BACK_LABEL, CBK_DATA_HOME)]])


def show_keyboard(name: str) -> InlineKeyboardMarkup:
    """
    Keyboard used when a single OTP value is shown.
    """
    return _keyboard(
        [
            [
                (BTN_REFRESH_LABEL, f"{CBK_DATA_REFRESH}__{name}"),
                (BTN_BACK_LABEL, CBK_DATA_LIST),
            ]
        ]
    )


def ls_keyboard(chat_id: str) -> InlineKeyboardMarkup:
    """
    Keyboard used to list OTPs.
    """
    return _ls_keyboard_helper(chat_id, CBK_DATA_SHOW)


def ls_rm_keyboard(chat_id: str) -> InlineKeyboardMarkup:
    """
    Keyboard used to remove OTPs.
    """
    return _ls_keyboard_helper(chat_id, CBK_DATA_REMOVE)


def rm_keyboard() -> InlineKeyboardMarkup:
    """
    Keyboard used to confirm the deletion of an OTP.
    """
    return _keyboard(
        [[(BTN_REMOVE_Y_LABEL, CBK_DATA_RM_Y), (BTN_REMOVE_N_LABEL, CBK_DATA_RM_N)]]
    )


def _keyboard(args: List[List[Tuple[str, str]]]) -> InlineKeyboardMarkup:
    """
    Helper function used to generate a keyboard with multiple buttons.

    Parameters
    ----------
    args : List[List[Tuple[str, str]]]
        A list of list describing the keyboard layout. Each list represent a row of the layout and
        each element is a tuple in form (str,str), where the first element is the label of the button
        and the second one if the prefix for the CallbackQuery associated with button.

    Returns
    -------
    InlineKeyboardMarkup
        _description_
    """
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(k[0], callback_data=k[1]) for k in j] for j in args]
    )


def _ls_keyboard_helper(chat_id: str, cbk_prefix: str) -> InlineKeyboardMarkup:
    """
    Helper function to generate keyboards who list existing seed.

    Parameters
    ----------
    chat_id : str
        Identifier of the chat
    cbk_prefix : str
        Prefix of the CallbackQuery to register on button click.

    Returns
    -------
    InlineKeyboardMarkup
        A keyboard with existing seeds as buttons.
    """
    otp_keys = [k[0] for k in persistence.load(chat_id)]
    keyboard_matrix = []
    keyboard_row: List[Tuple[str, str]] = []
    for i in range(len(otp_keys)):
        if i % (LIST_ROW_LENGTH) == 0 and i != 0:
            keyboard_matrix.append(keyboard_row)
            keyboard_row = []
        keyboard_row.append((otp_keys[i], f"{cbk_prefix}__{otp_keys[i]}"))
    keyboard_matrix.append(keyboard_row)

    keyboard_matrix.append([(BTN_BACK_LABEL, CBK_DATA_HOME)])
    return _keyboard(keyboard_matrix)
