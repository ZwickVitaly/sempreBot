from aiogram.types import BotCommand
from aiogram import Dispatcher


async def standard_startup_menu(dispatcher: Dispatcher):
    """
    Function to wrap up dispatcher.

    :param: dispatcher (Dispatcher): takes in dispatcher instance

    :awaited: set_default_commands (Awaitable): result of wrapped function
    """
    async def set_default_commands(wrapped_dispatcher: Dispatcher):
        """
        Function to set bot command menu

        :param: wrapped_dispatcher (Dispatcher):

        :awaited: wrapped_dispatcher.bot.set_my_commands (Awaitable): settled bot commands
        """
        await wrapped_dispatcher.bot.set_my_commands([
                BotCommand('start', 'Запустить бота.'),
                BotCommand('help', 'Список команд.'),
                BotCommand('stop', 'Остановить обработку сообщений.')
                                                      ])
    await set_default_commands(dispatcher)
