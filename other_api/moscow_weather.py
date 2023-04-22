import requests
from config import weather_token
from datetime import datetime


def get_moscow_weather(token=weather_token):
    data = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat=55.7504461&lon=37.6174943&units=metric&'
            f'appid={token}'
        ).json()
    result = f'Погода в Москве на {datetime.now().strftime("%H:%M")}\n' \
             f'Температура: {data["main"]["temp"]}°C (ощущается как {data["main"]["feels_like"]}°C)\n' \
             f'Ветер: {data["wind"]["speed"]} м/c \n' \
             f'Давление: {round(data["main"]["pressure"] * 0.75)}мм рт. ст.\n' \
             f'Влажность: {data["main"]["humidity"]}%\n' \
             f'Восход в {datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")}\n' \
             f'Закат в {datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")}\n'
    return result
