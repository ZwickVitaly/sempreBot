from aiogram.types import Message
from other_api.open_weather import get_moscow_weather, get_curr_loc_weather


async def moscow_weather_handler(message: Message):
    """
    Function to handle weather message

    :param: message (Message): takes in user message

    :arg: msg (str): bot answer message (weather data string)

    :awaited: message.answer (Awaitable): processed bot answer
    """
    msg: str = get_moscow_weather()
    await message.answer(msg)


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