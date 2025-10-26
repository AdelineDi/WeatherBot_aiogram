import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

BOT_TOKEN = "8482336373:AAGMhAgif1yO_V5F-yOqNkDtmJGyeu4xGKk"
WEATHER_API = "49015a6d51ee5b278338c8d730a1f313"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Напиши название своего города:")

@dp.message()
async def get_weather(message: types.Message):
    city = message.text.strip().lower()
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as result:
            if result.status == 200:
                data = await result.json()
                temp = data["main"]["temp"]
                await message.reply(f"Погода в данный момент: {temp}°C")

                image = "sun.png" if temp > 5.0 else "cloud.png"
                photo = FSInputFile(image)
                await message.answer_photo(photo)
            else:
                await message.reply("Не нужно вымышленных городов, введите реальный!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())