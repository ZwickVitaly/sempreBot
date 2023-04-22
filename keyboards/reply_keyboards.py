from aiogram.types import ReplyKeyboardMarkup


def sempre_main_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add('Смена', 'Меню', 'Погода в Москве')
    return keyboard


def sempre_workers_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add('< Главное меню', 'Грузчики', 'Хостес', 'Раннеры', 'Клининг', 'Официанты')
    return keyboard


def sempre_dish_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add('< Главное меню')
    return keyboard


def day_set_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add('< Главное меню', 'Сегодня', 'Завтра')
    return keyboard
