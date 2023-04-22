from aiogram.types import ReplyKeyboardMarkup


def sempre_main_kb() -> ReplyKeyboardMarkup:
    """
    Function to markup telegram main menu keyboard

    :return: keyboard
    :rtype: ReplyKeyboardMarkup
    """
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add('Смена', 'Меню', 'Погода в Москве')
    return keyboard


def sempre_workers_kb() -> ReplyKeyboardMarkup:
    """
    Function to markup telegram workers menu keyboard

    :return: keyboard
    :rtype: ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add('< Главное меню', 'Грузчики', 'Хостес', 'Раннеры', 'Клининг', 'Официанты')
    return keyboard


def sempre_dish_menu() -> ReplyKeyboardMarkup:
    """
    Function to markup telegram dish menu keyboard

    :return: keyboard
    :rtype: ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add('< Главное меню')
    return keyboard


def day_set_kb() -> ReplyKeyboardMarkup:
    """
    Function to markup telegram day set menu keyboard

    :return: keyboard
    :rtype: ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add('< Главное меню', 'Сегодня', 'Завтра')
    return keyboard
