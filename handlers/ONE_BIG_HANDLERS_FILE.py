from bot_loader import dispatcher
from messages.standard_messages import help_message, start_message, stop_message
from aiogram.types import Message
from aiogram.dispatcher import filters
from other_api.moscow_weather import get_moscow_weather
from keyboards.reply_keyboards import sempre_main_kb, sempre_workers_kb, day_set_kb, sempre_dish_menu
from aiogram.types import ReplyKeyboardRemove
from FSM.FSM import SempreFSM
from datetime import datetime, timedelta
import re

dp = dispatcher


@dispatcher.message_handler(filters.CommandHelp(), state="*")
async def help_handler(message: Message):
    msg = help_message
    await message.answer(msg)


@dispatcher.message_handler(filters.CommandStart(), state="*")
async def start_handler(message: Message):
    msg = start_message
    await SempreFSM.main_menu.set()
    await message.answer(msg, reply_markup=sempre_main_kb())


@dispatcher.message_handler(filters.Command('stop'), state="*")
async def start_handler(message: Message):
    msg = stop_message
    await SempreFSM.end_state.set()
    await message.answer(msg, reply_markup=ReplyKeyboardRemove())


@dispatcher.message_handler(filters.Text('Погода в Москве'), state=SempreFSM.main_menu)
async def weather_handler(message: Message):
    msg = get_moscow_weather()
    await message.answer(msg)


@dispatcher.message_handler(filters.Text('Смена'), state=SempreFSM.main_menu)
async def day_handler(message: Message):
    msg = 'Выберите день'
    await message.answer(msg, reply_markup=day_set_kb())


@dispatcher.message_handler(filters.Text('Меню'), state=SempreFSM.main_menu)
async def dish_menu_handler(message: Message):
    msg = 'Введите название блюда (поиск по ключевым словам)'
    await SempreFSM.menu_choice.set()
    await message.answer(msg, reply_markup=sempre_dish_menu())


@dispatcher.message_handler(state=SempreFSM.menu_choice)
async def dish_handler(message: Message):
    msg = dispatcher.bot.menu_table.search_main_menu(message.text)
    await SempreFSM.main_menu.set()
    await message.answer(msg, reply_markup=sempre_main_kb())


@dispatcher.message_handler(filters.Text(['Сегодня', 'Завтра']), state=SempreFSM.main_menu)
async def worker_handler(message: Message):
    try:
        if message.text == 'Сегодня':
            await SempreFSM.today_shift.set()
        else:
            if datetime.now().day > (datetime.now() + timedelta(days=1)).day:
                raise IndexError
            else:
                await SempreFSM.tomorrow_shift.set()
        msg = 'Выберите должность работников'
        await message.answer(msg, reply_markup=sempre_workers_kb())
    except IndexError:
        await message.answer('Завтра новый месяц. В конце этого дня обновите ссылку на таблицу.\n'
                             'Возвращаю главное меню.',
                             reply_markup=sempre_main_kb())
        await SempreFSM.main_menu.set()


@dispatcher.message_handler(filters.Text(['Грузчики', 'Хостес', 'Раннеры', 'Клининг', 'Официанты']),
                            state=[SempreFSM.today_shift, SempreFSM.tomorrow_shift])
async def schedule_workers_handler(message: Message):
    current_state = await dispatcher.current_state().get_state()
    worker = message.text
    await message.answer(f'Вы выбрали "{worker}". Идёт обработка запроса...')
    if current_state == 'SempreFSM:today_shift':
        workers = dispatcher.bot.schedule_table.search_workers(worker, datetime.now().day)
    else:
        workers = dispatcher.bot.schedule_table.search_workers(worker, (datetime.now() + timedelta(days=1)).day)
    await message.answer(workers)


@dispatcher.message_handler(filters.Text('< Главное меню'),
                            state=[SempreFSM.today_shift,
                                   SempreFSM.tomorrow_shift,
                                   SempreFSM.menu_choice,
                                   SempreFSM.main_menu,
                                   None])
async def main_menu_handler(message: Message):
    await SempreFSM.main_menu.set()
    await message.answer('Возвращаю главное меню.', reply_markup=sempre_main_kb())


@dispatcher.message_handler(filters.Regexp(regexp=re.compile(r'^/new_table.*',
                                                             re.IGNORECASE)), state='*')
async def new_table_handler(message: Message):
    result = re.findall(r'(https://docs.google.com/spreadsheets/.*)', message.text, re.IGNORECASE)
    if result:
        result = result[0]
        with open('config.py', 'r+') as config_file:
            data = config_file.readlines()
            config_file.seek(0)
            data[5] = f"sempre_schedule_url = '{result}'"
            config_file.writelines(data)
        dispatcher.bot.set_google_table(result)
        await message.answer('Ссылка на таблицу подгружена.')
    else:
        await message.answer('Не найдена ссылка на таблицу.')
