# import datetime
import re
from aiogram import Bot, executor, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN  # для работы с ботом необходимо создать файл config.py с содержимым TOKEN = 'токен бота'


bot: Bot = Bot(token=TOKEN)
dispatcher: Dispatcher = Dispatcher(bot=bot)
users_dict: dict = {}  # первичная мера обработки /start /stop команд.


def get_kb() -> ReplyKeyboardMarkup:
    """
    Функция для создания клавиатуры бота.

    :return: keyboard
    :rtype: ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('/start'), KeyboardButton('/stop'), KeyboardButton('Привет, бот!'))
    return keyboard


# def log_requests(user_id, message_text, answer_message):
#
#     with open('requests.log', 'a', encoding='utf-8') as log_file:
#
#         log_file.write(
#                         f'User_ID: {user_id} Message: {message_text}, '
#                         f'{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}\n'
#                         f'Bot_message: {answer_message}\n'
#         )


@dispatcher.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    """
    Хэндлер команды "/start"

    :param: message (types.Message): передаёт команду "/start"

    :arg: msg (str): передаёт ответ бота.

    :await: message.answer(msg) (types.Message): передаёт сообщение с ответом от бота.
    """
    if users_dict.get(message.from_user.id):
        msg = 'Бот уже работает!'
        await message.answer(msg)
    else:
        users_dict[message.from_user.id] = True
        msg = 'Начинаем работу!'
        await message.answer(msg, reply_markup=get_kb())
    # log_requests(user_id=message.from_user.id, message_text=message.text, answer_message=msg)


@dispatcher.message_handler(commands=['stop'])
async def start_handler(message: types.Message):
    """
    Хэндлер команды "/stop"

    :param: message (message): передаёт команду "/stop"

    :arg: msg (str): передаёт ответ бота.

    :await: message.answer(msg) (types.Message): передаёт сообщение с ответом от бота.
    """
    # msg = None
    if users_dict.get(message.from_user.id):
        msg = f'Пока, {message.from_user.first_name}!'
        users_dict[message.from_user.id] = False
        await message.answer(msg)
    # if msg:
    #     log_requests(user_id=message.from_user.id, message_text=message.text, answer_message=msg)


@dispatcher.message_handler(content_types='text')
async def start_handler(message: types.Message):
    """
    Хэндлер для ответа на сообщение "Привет бот"

    :param: message (types.Message): передаёт сообщение боту.

    :arg: result (str): результат проверки на совпадение текста сообщения с обрабатываемым паттерном.
    :arg: msg (str): передаёт ответ бота.

    :await: message.answer(msg) (types.Message): передаёт сообщение с ответом от бота.
    """
    result = re.match('привет.*.*бот', message.text, re.IGNORECASE)
    # msg = None
    if result and users_dict.get(message.from_user.id):
        msg = f'Привет, {message.from_user.first_name}!'
        await message.answer(msg)
    # if msg:
    #     log_requests(user_id=message.from_user.id, message_text=message.text, answer_message=msg)


if __name__ == '__main__':
    print('Бот работает.')
    executor.start_polling(dispatcher, skip_updates=True)
