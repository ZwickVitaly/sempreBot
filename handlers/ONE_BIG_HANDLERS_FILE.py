from bot_loader import dispatcher
from messages.standard_messages import help_message, start_message, stop_message
from aiogram.types import Message, ContentTypes
from aiogram.dispatcher import filters
from other_api.open_weather import get_moscow_weather, get_curr_loc_weather
from keyboards.reply_keyboards import sempre_main_kb, sempre_workers_kb, day_set_kb, sempre_dish_menu
from aiogram.types import ReplyKeyboardRemove
from FSM.FSM import SempreFSM
from datetime import datetime, timedelta
from re import IGNORECASE, findall, compile


@dispatcher.message_handler(filters.CommandHelp(), state="*")
async def help_handler(message: Message):
    """
    Function to handle help message

    :param: message (Message): takes in user message

    :arg: msg (str): bot answer message

    :awaited: message.answer (Awaitable): processed bot answer
    """
    msg = help_message
    await message.answer(msg)


@dispatcher.message_handler(filters.CommandStart(), state="*")
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


@dispatcher.message_handler(filters.Command('stop'), state="*")
async def start_handler(message: Message):
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


@dispatcher.message_handler(filters.Text('Погода в Москве'), state=SempreFSM.main_menu)
async def moscow_weather_handler(message: Message):
    """
    Function to handle weather message

    :param: message (Message): takes in user message

    :arg: msg (str): bot answer message (weather data string)

    :awaited: message.answer (Awaitable): processed bot answer
    """
    msg: str = get_moscow_weather()
    await message.answer(msg)


@dispatcher.message_handler(content_types=ContentTypes.LOCATION, state=SempreFSM.main_menu)
async def curr_loc_weather_handler(message: Message):
    """
    Function to handle location message for weather data for this location

    :param: message (Message): takes in user message with location

    :arg: msg (str): bot answer message (weather data string)

    :awaited: message.answer (Awaitable): processed bot answer
    """
    lat = message.location.latitude
    lon = message.location.longitude
    msg = get_curr_loc_weather(lat=lat, lon=lon)
    await message.answer(msg)


@dispatcher.message_handler(filters.Text('Меню'), state=SempreFSM.main_menu)
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


@dispatcher.message_handler(state=SempreFSM.menu_choice)
async def dish_handler(message: Message):
    """
    Function to handle keywords to search through menu Google sheet in a menu_choice state

    :param: message (Message): takes in user message

    :arg: msg (str): bot answer message (dish description, found by keywords)

    :awaited: SempreFSM.main_menu.set (Awaitable): sets bot state to main_menu state
    :awaited: message.answer (Awaitable): processed bot answer and main menu keyboard
    """
    msg: str = dispatcher.bot.menu_sheet.search_main_menu(message.text)
    await SempreFSM.main_menu.set()
    await message.answer(msg, reply_markup=sempre_main_kb())


@dispatcher.message_handler(filters.Text('Смена'), state=SempreFSM.main_menu)
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


@dispatcher.message_handler(filters.Text(['Сегодня', 'Завтра']), state=SempreFSM.day_choice)
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


@dispatcher.message_handler(filters.Text(['Грузчики', 'Хостес', 'Раннеры', 'Клининг', 'Официанты']),
                            state=[SempreFSM.today_shift, SempreFSM.tomorrow_shift])
async def schedule_workers_handler(message: Message):
    """
    Function to handle chosen workers message in today_shift or tomorrow_shift state

    :param: message (Message): takes in user message

    :arg: current_state (str): contains string of current state
    :arg: worker (str): contains worker job title
    :arg: workers (str): contains bot answer message

    :awaited: message.answer (Awaitable): processed bot answer message (string of time shift and workers)
    """
    current_state = await dispatcher.current_state().get_state()
    worker = message.text
    await message.answer(f'Вы выбрали "{worker}". Идёт обработка запроса...')
    if current_state == 'SempreFSM:today_shift':
        workers = dispatcher.bot.schedule_sheet.search_workers(worker, datetime.now().day)
    else:
        workers = dispatcher.bot.schedule_sheet.search_workers(worker, (datetime.now().day + 1))
    await message.answer(workers)


@dispatcher.message_handler(filters.Text('< Главное меню'),
                            state=[SempreFSM.today_shift,
                                   SempreFSM.tomorrow_shift,
                                   SempreFSM.menu_choice,
                                   SempreFSM.day_choice])
async def main_menu_handler(message: Message):
    """
    Function to handle main menu message in any state, except end_state

    :param: message (Message): takes in user message

    :awaited: SempreFSM.main_menu.set: awaits main_menu state
    :awaited: message.answer: processed bot answer and main menu keyboard
    """
    await SempreFSM.main_menu.set()
    await message.answer('Возвращаю главное меню.', reply_markup=sempre_main_kb())


@dispatcher.message_handler(filters.Regexp(regexp=compile(r'^/new_table.*', IGNORECASE)), state=SempreFSM.main_menu)
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
        dispatcher.bot.set_google_table(new_schedule_url)
        await message.answer('Ссылка на таблицу подгружена.')
    else:
        await message.answer('Не найдена ссылка на таблицу.')
