import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot,types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
     await message.reply("Բարև Ձեզ, եղանակը պարզելու համար գրեք ձեր քաղաքը \U0000263A \n"
                         "/help եթե խնդիրներ կան ")

@dp.message_handler(commands=["help"])
async def start_command(message: types.Message):
     await message.reply("Դժվարությունների դեպքում մենք կօգնենք ձեզ, գրեք բոտը ստեղծողին անձնական հաղորդագրությամբ - Нор Гаспарян")

@dp.message_handler(commands=["creator"])
async def start_command(message: types.Message):
     await message.reply("------Русский \n Этот бот создал Армянин 🇦🇲 Его зовут: Норо.\n ------"
                         "հայերեն \nԱյս բոտը ստեղծել է հայ 🇦🇲 Նրա անունը Նորո: է\n ------"
                         "English \nThis bot was created by an Armenian 🇦🇲 His name is: Noro.")

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Պարզ \U00002600",
        "Clouds": "Ամպամած \U00002601",
        "Rain": "Անձրև \U00002614",
        "Drizzle": "Անձրև \U00002614",
        "Thunderstorm": "Փոթորիկ \U000026A1",
        "Snow": "Ձյուն \U0001F328",
        "Mist": "Մառախուղ \U0001F32B"

    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Նայիր պատուհանից դուրս, ես չեմ հասկանում, թե ինչպիսի եղանակ է այնտեղ!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Եղանակը քաղաքում: {city}\nՋերմաստիճանը: {cur_weather}C° {wd}\n"
              f"Խոնավություն: {humidity}%\nՃնշում: {pressure} Միլիմետր սնդիկ\nՔամի: {wind} մ/վրկ\n"
              f"Արեւածագ: {sunrise_timestamp}\nՄայրամուտ: {sunset_timestamp}\nՕրվա տեւողությունը: {length_of_the_day}\n"
              f"***Լավ օր եմ մաղթում!*** \U0001F603"
              )

    except :
        await message.reply("\U00002620 Ստուգեք քաղաքի անունը \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)