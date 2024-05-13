import requests
from config import weather_token
from datetime import datetime
from typing import Dict


def get_moscow_weather(token=weather_token) -> str:
    """
    Function to get weather data from https://openweathermap.org/ api in requested format

    :param: token (str): takes in openweather api token

    :arg: data (Dict): contains request result

    :return: result: result string
    :rtype: str
    """
    data: Dict = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat=55.7504461&lon=37.6174943&units=metric&'
            f'appid={token}'
        ).json()
    result: str = f'Погода в Москве на {datetime.now().strftime("%H:%M")}\n' \
                  f'Температура: {data["main"]["temp"]}°C (ощущается как {data["main"]["feels_like"]}°C)\n' \
                  f'Ветер: {data["wind"]["speed"]} м/c \n' \
                  f'Давление: {round(data["main"]["pressure"] * 0.75)}мм рт. ст.\n' \
                  f'Влажность: {data["main"]["humidity"]}%\n' \
                  f'Восход в {datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")}\n' \
                  f'Закат в {datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")}\n'
    return result


def get_curr_loc_weather(lat: float, lon: float, token=weather_token) -> str:
    """
    Function to get weather data from https://openweathermap.org/ api in requested format

    :param: lat (float): takes in latitude of location
    :param: lon (float): takes in longitude of location
    :param: token (str): takes in openweather api token

    :arg: data (Dict): contains request result

    :return: result: result string
    :rtype: str
    """
    data: Dict = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&'
            f'appid={token}'
        ).json()
    result: str = f'Погода в указанной точке на {datetime.now().strftime("%H:%M")}\n' \
                  f'Температура: {data["main"]["temp"]}°C (ощущается как {data["main"]["feels_like"]}°C)\n' \
                  f'Ветер: {data["wind"]["speed"]} м/c \n' \
                  f'Давление: {round(data["main"]["pressure"] * 0.75)}мм рт. ст.\n' \
                  f'Влажность: {data["main"]["humidity"]}%\n' \
                  f'Восход в {datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")}\n' \
                  f'Закат в {datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")}\n'
    return result
