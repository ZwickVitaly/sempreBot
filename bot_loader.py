from re import IGNORECASE, compile

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import filters
from aiogram.types import ContentTypes

from FSM.FSM import SempreFSM
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers.sempre_specific_handlers import schedule_workers_handler_today, schedule_workers_handler_tomorrow,\
    dish_handler, dish_menu_handler, worker_handler, new_table_handler, day_handler

from handlers.standard_handlers import start_handler, stop_handler, help_handler, main_menu_handler

from handlers.weather_handlers import moscow_weather_handler, curr_loc_weather_handler


storage = MemoryStorage()
bot = Bot(TOKEN, parse_mode='HTML')
dispatcher = Dispatcher(bot, storage=storage)

dispatcher.register_message_handler(
    help_handler,
    filters.CommandHelp(),
    state="*",
)
dispatcher.register_message_handler(
    start_handler,
    filters.CommandStart(),
    state="*",
)
dispatcher.register_message_handler(
    stop_handler,
    filters.Command('stop'),
    state="*",
)
dispatcher.register_message_handler(
    main_menu_handler,
    filters.Text('< Главное меню'),
    state=[SempreFSM.today_shift,
           SempreFSM.tomorrow_shift,
           SempreFSM.menu_choice,
           SempreFSM.day_choice]
)

dispatcher.register_message_handler(
    moscow_weather_handler,
    filters.Text('Погода в Москве'),
    state=SempreFSM.main_menu,
)
dispatcher.register_message_handler(
    curr_loc_weather_handler,
    content_types=ContentTypes.LOCATION,
    state=SempreFSM.main_menu,
)

dispatcher.register_message_handler(
    dish_menu_handler,
    filters.Text('Меню'),
    state=SempreFSM.main_menu,
)
dispatcher.register_message_handler(
    dish_handler,
    lambda message: message.text != '< Главное меню',
    state=SempreFSM.menu_choice,
)
dispatcher.register_message_handler(
    day_handler,
    filters.Text('Смена'),
    state=SempreFSM.main_menu,
)
dispatcher.register_message_handler(
    worker_handler,
    filters.Text(['Сегодня', 'Завтра']),
    state=SempreFSM.day_choice
)
dispatcher.register_message_handler(
    schedule_workers_handler_today,
    filters.Text(['Грузчики', 'Хостес', 'Раннеры', 'Клининг', 'Официанты']),
    state=SempreFSM.today_shift
)
dispatcher.register_message_handler(
    schedule_workers_handler_tomorrow,
    filters.Text(['Грузчики', 'Хостес', 'Раннеры', 'Клининг', 'Официанты']),
    state=SempreFSM.tomorrow_shift
)
dispatcher.register_message_handler(
    new_table_handler,
    filters.Regexp(regexp=compile(r'^/new_table.*', IGNORECASE)),
    state=SempreFSM.main_menu
)
