from aiogram.types import Message, ReplyKeyboardRemove
from FSM.FSM import SempreFSM
from keyboards.reply_keyboards import sempre_main_kb
from messages.standard_messages import stop_message, start_message, help_message


async def help_handler(message: Message):
    """
    Function to handle help message

    :param: message (Message): takes in user message

    :arg: msg (str): bot answer message

    :awaited: message.answer (Awaitable): processed bot answer
    """
    msg = help_message
    await message.answer(msg)


async def start_handler(message: Message):
    """
    Function to handle start message

    :param: message (Message): takes in user message

    :arg: msg (str): bot answer message

    :awaited: SempreFSM.main_menu.set (Awaitable): sets bot state to main menu
    :awaited: message.answer (Awaitable): processed bot answer and main menu keyboard
    """
    msg: str = start_message
    await SempreFSM.main_menu.set()
    await message.answer(msg, reply_markup=sempre_main_kb())


async def stop_handler(message: Message):
    """
    Function to handle stop message

    :param: message (Message): takes in user message

    :arg: msg (str): bot answer message

    :awaited: SempreFSM.end_state.set (Awaitable): sets bot state to end state
    :awaited: message.answer (Awaitable): processed bot answer and removes any keyboard, except command menu
    """
    msg: str = stop_message
    await SempreFSM.end_state.set()
    await message.answer(msg, reply_markup=ReplyKeyboardRemove())


async def main_menu_handler(message: Message):
    """
    Function to handle main menu message in any state, except end_state

    :param: message (Message): takes in user message

    :awaited: SempreFSM.main_menu.set: awaits main_menu state
    :awaited: message.answer: processed bot answer and main menu keyboard
    """
    await SempreFSM.main_menu.set()
    await message.answer('Возвращаю главное меню.', reply_markup=sempre_main_kb())
