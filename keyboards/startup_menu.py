from aiogram.types import BotCommand


async def standard_startup_menu(dispatcher):
    async def set_default_commands(wrapped_dispatcher):
        await wrapped_dispatcher.bot.set_my_commands([
                BotCommand('start', 'Запустить бота.'),
                BotCommand('help', 'Список команд.'),
                BotCommand('stop', 'Остановить обработку сообщений.')
                                                      ])
    await set_default_commands(dispatcher)
