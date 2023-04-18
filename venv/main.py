import datetime
import re
import bot_cfg
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType, Message
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor
from google_table import GoogleTable
# from loguru import logger


# logger.add(
#     bot_cfg.settings['Log_File'],
#     format='{time} {level} {message}',
#     level='DEBUG',
#     rotation='1 week',
#     compression='zip',
# )

class MyBot(Bot):
    def __init__(self, token, parse_mode):
        super().__init__(token, parse_mode=parse_mode)
        self.google_table = None
        try:
            with open('actual_table.txt', 'r') as actual_table:
                actual_table = actual_table.read().split('\n')
                if int(actual_table[0]) == datetime.datetime.now().month:
                    self.google_table = GoogleTable(cred_serv_file='credentials.json', google_sheet_url=actual_table[1])
        except FileNotFoundError:
            self.google_table = None

    def set_google_table(self, google_table_url):
        self.google_table = GoogleTable(cred_serv_file='credentials.json', google_sheet_url=google_table_url)


bot = MyBot(token=bot_cfg.settings['TOKEN'],
            parse_mode=types.ParseMode.HTML,
            )
dispatcher = Dispatcher(bot=bot)
users_dict = {}




def get_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
                 KeyboardButton('/loaders'),
                 KeyboardButton('/host'),
                 KeyboardButton('/runners'),
                 KeyboardButton('/cleaning'),
                 KeyboardButton('/waiters'))
    return keyboard


@dispatcher.message_handler(filters.CommandHelp())
async def start_handler(message: types.Message):
    msg = '/start - Начать работу с ботом (начнёт реагировать на сообщения и команды).\n' \
          '/stop - Закончить работу с ботом (перестанет реагировать на сообщения)\n'\
          '/waiters - показать официантов, работающих сегодня.\n' \
          '/host - показать хостес, работающих сегодня.\n' \
          '/runners - показать раннеров, работающих сегодня.\n' \
          '/cleaning - показать уборщиц, работающих сегодня.\n' \
          '/loaders - показать котломойщиков, работающих сегодня.\n'
    await message.answer(msg)


@dispatcher.message_handler(filters.CommandStart())
async def start_handler(message: types.Message):
    if users_dict.get(message.from_user.id):
        msg = 'Бот уже работает!'
        await message.answer(msg)
    else:
        users_dict[message.from_user.id] = True
        msg = 'Начинаем работу!'
        bot_working = True
        await message.answer(msg, reply_markup=get_kb())


@dispatcher.message_handler(commands=['stop'])
async def stop_handler(message: types.Message):
    msg = None
    if users_dict.get(message.from_user.id):
        msg = f'Пока, {message.from_user.first_name}!'
        users_dict[message.from_user.id] = False
        await message.answer(msg)


@dispatcher.message_handler(filters.Regexp(regexp=re.compile(r'^привет.+бот.*', re.IGNORECASE)))
async def hello_handler(message: types.Message):
    msg = None
    if users_dict.get(message.from_user.id):
        msg = f'Привет, {message.from_user.first_name}!'
        await message.answer(msg)


@dispatcher.message_handler(commands=['host', 'waiters', 'runners', 'cleaning', 'loaders'])
async def schedule_workers_handler(message: types.Message):
    if users_dict.get(message.from_user.id) and bot.google_table:
        workers = bot.google_table.search_workers(message.text)
        if workers:
            await message.answer(workers)
        else:
            await message.answer('Нет результатов')
    elif users_dict.get(message.from_user.id) and not bot.google_table:
        await message.answer('Воспользуйтесь командой /new_table [ссылка на таблицу], чтобы актуализировать таблицу графика.\n'
                             'Не забудьте дать доступ к таблице через сервисную почту бота.')


@dispatcher.message_handler(filters.Regexp(regexp=re.compile(r'^/new_table https://docs.google.com/spreadsheets/.*', re.IGNORECASE)))
async def find_worker_handler(message: types.Message):
    if users_dict.get(message.from_user.id):
        result = re.findall(r'^/new_table (https://docs.google.com/spreadsheets/.*)edit*', message.text, re.IGNORECASE)[0]
        with open('actual_table.txt', 'w') as actual_table:
            actual_table.write(f'{datetime.datetime.now().month}\n{result}')
        bot.set_google_table(result)
        await message.answer('Ссылка на таблицу подгружена.')


@dispatcher.message_handler()
async def find_worker_handler(message: types.Message):
    if message.from_user.id not in users_dict:
        await message.answer('Воспользуйтесь командой /start')

if __name__ == '__main__':
    print('Бот работает.')
    executor.start_polling(dispatcher, skip_updates=True)



