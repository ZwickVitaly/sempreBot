from datetime import datetime, timedelta
from re import findall, IGNORECASE

from aiogram.types import Message

from config import sempre_menu_url, sempre_schedule_url
from other_api.sempre_google_sheets import SempreMenu, SempreSchedule
from FSM.FSM import SempreFSM
from keyboards.reply_keyboards import sempre_dish_menu, sempre_main_kb, day_set_kb, sempre_workers_kb


sempre_menu = SempreMenu(sempre_menu_url)
sempre_schedule = SempreSchedule(sempre_schedule_url)


async def dish_menu_handler(message: Message):
    """
    Function to handle dish menu message

    :param: message (Message): takes in user message

    :arg: msg (str): bot answer message

    :awaited: SempreFSM.menu_choice.set (Awaitable): sets bot state to menu_choice state
    :awaited: message.answer (Awaitable): processed bot answer and Sempre dish menu keyboard
    """
    msg: str = 'Введите название блюда (поиск по ключевым словам)'
    await SempreFSM.menu_choice.set()
    await message.answer(msg, reply_markup=sempre_dish_menu())


async def dish_handler(message: Message):
    """
    Function to handle keywords to search through menu Google sheet in a menu_choice state

    :param: message (Message): takes in user message

    :arg: msg (str): bot answer message (dish description, found by keywords)

    :awaited: SempreFSM.main_menu.set (Awaitable): sets bot state to main_menu state
    :awaited: message.answer (Awaitable): processed bot answer and main menu keyboard
    """
    msg: str = sempre_menu.search_main_menu(message.text)
    await SempreFSM.main_menu.set()
    await message.answer(msg, reply_markup=sempre_main_kb())


async def day_handler(message: Message):
    """
    Function to handle shift day choice message

    :param: message (Message): takes in user message

    :arg: msg (str): bot answer message

    :awaited: SempreFSM.day_choice.set (Awaitable): sets bot state to day_choice
    :awaited: message.answer (Awaitable): processed bot answer and day set keyboard
    """
    msg: str = 'Выберите день'
    await SempreFSM.day_choice.set()
    await message.answer(msg, reply_markup=day_set_kb())


async def worker_handler(message: Message):
    """
    Function to handle chosen day message in a day_choice state

    :param: message (Message): takes in user message

    :arg: msg (str): bot answer message

    :awaited: SempreFSM.today_shift.set (Awaitable): sets bot state to today_shift state
    :awaited: SempreFSM.tomorrow_shift.set (Awaitable): sets bot state to tomorrow_shift state
    :awaited: SempreFSM.main_menu.set (Awaitable): sets bot state to main_menu state
    :awaited: message.answer (Awaitable): processed bot answer and sets workers keyboard or main keyboard

    :raise: IndexError: if it is last day of month
    """
    try:
        if message.text == 'Сегодня':
            await SempreFSM.today_shift.set()
        else:
            if datetime.now().day > (datetime.now() + timedelta(days=1)).day:
                raise IndexError
            else:
                await SempreFSM.tomorrow_shift.set()
        msg: str = 'Выберите должность работников'
        await message.answer(msg, reply_markup=sempre_workers_kb())
    except IndexError:
        await message.answer('Завтра новый месяц. В конце этого дня обновите ссылку на таблицу.\n'
                             'Возвращаю главное меню.',
                             reply_markup=sempre_main_kb())
        await SempreFSM.main_menu.set()


async def schedule_workers_handler_today(message: Message):
    """
    Function to handle chosen workers message in today_shift or tomorrow_shift state

    :param: message (Message): takes in user message

    :arg: current_state (str): contains string of current state
    :arg: worker (str): contains worker job title
    :arg: workers (str): contains bot answer message

    :awaited: message.answer (Awaitable): processed bot answer message (string of time shift and workers)
    """
    worker = message.text
    await message.answer(f'Вы выбрали "{worker}". Идёт обработка запроса...')
    workers = sempre_schedule.search_workers(worker, datetime.now().day)
    await message.answer(workers)


async def schedule_workers_handler_tomorrow(message: Message):
    """
    Function to handle chosen workers message in today_shift or tomorrow_shift state

    :param: message (Message): takes in user message

    :arg: current_state (str): contains string of current state
    :arg: worker (str): contains worker job title
    :arg: workers (str): contains bot answer message

    :awaited: message.answer (Awaitable): processed bot answer message (string of time shift and workers)
    """
    worker = message.text
    await message.answer(f'Вы выбрали "{worker}". Идёт обработка запроса...')
    workers = sempre_schedule.search_workers(worker, (datetime.now().day + 1))
    await message.answer(workers)


async def new_table_handler(message: Message):
    """
    Function to handle new sheet url message in main menu state
    There is no keyboard button for this command.

    :param: message (Message): takes in user message

    :arg: new_schedule_url (list, string): contains new schedule google sheet url
    :arg: data (list): contains config file data list

    :awaited: message.answer: processed bot answer
    """
    new_schedule_url = findall(r'(https://docs.google.com/spreadsheets/.*)', message.text, IGNORECASE)
    if new_schedule_url:
        new_schedule_url = new_schedule_url[0]
        with open('config.py', 'r+') as config_file:
            data = config_file.readlines()
            config_file.seek(0)
            data[5] = f"sempre_schedule_url = '{new_schedule_url}'"
            config_file.writelines(data)
        sempre_schedule.set_google_table(new_schedule_url)
        await message.answer('Ссылка на таблицу подгружена.')
    else:
        await message.answer('Не найдена ссылка на таблицу.')
