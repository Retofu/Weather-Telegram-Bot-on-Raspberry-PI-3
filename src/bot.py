import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from .weather_client import OpenMeteoClient
from .formatting import format_day
from .geocoding import OpenMeteoGeocoder


async def main() -> None:
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in environment")

    bot = Bot(token=token)
    dp = Dispatcher()
    client = OpenMeteoClient()
    geocoder = OpenMeteoGeocoder()

    @dp.message(Command("start"))
    async def cmd_start(message: types.Message) -> None:
        text = (
            "Привет! Я бот погоды.\n"
            "Команды:\n"
            "/today [город] — прогноз на сегодня\n"
            "/tomorrow [город] — прогноз на завтра\n"
            "/weather [город] — прогноз на сегодня и завтра\n"
            "По умолчанию используется город Челябинск."
        )
        await message.answer(text)

    @dp.message(Command("today"))
    async def cmd_today(message: types.Message) -> None:
        # Support: /today <город>
        args = (message.text or "").split(maxsplit=1)
        place_name = args[1] if len(args) > 1 else "Челябинск"
        place = geocoder.search(place_name)
        if not place:
            await message.answer("Не нашёл такой город. Попробуйте уточнить название.")
            return
        local_client = OpenMeteoClient(latitude=place.latitude, longitude=place.longitude, tz=place.timezone or "auto")
        f = local_client.get_day(0)
        title = f"Сегодня — {place.name}"
        text = format_day(title, f)
        await message.answer(text)

    @dp.message(Command("tomorrow"))
    async def cmd_tomorrow(message: types.Message) -> None:
        # Support: /tomorrow <город>
        args = (message.text or "").split(maxsplit=1)
        place_name = args[1] if len(args) > 1 else "Челябинск"
        place = geocoder.search(place_name)
        if not place:
            await message.answer("Не нашёл такой город. Попробуйте уточнить название.")
            return
        local_client = OpenMeteoClient(latitude=place.latitude, longitude=place.longitude, tz=place.timezone or "auto")
        f = local_client.get_day(1)
        title = f"Завтра — {place.name}"
        text = format_day(title, f)
        await message.answer(text)

    @dp.message(Command("weather"))
    async def cmd_weather(message: types.Message) -> None:
        # /weather <город>
        args = (message.text or "").split(maxsplit=1)
        if len(args) == 1:
            await message.answer("Использование: /weather <город>")
            return
        place_name = args[1]
        place = geocoder.search(place_name)
        if not place:
            await message.answer("Не нашёл такой город. Попробуйте уточнить название.")
            return
        local_client = OpenMeteoClient(latitude=place.latitude, longitude=place.longitude, tz=place.timezone or "auto")
        f0 = local_client.get_day(0)
        f1 = local_client.get_day(1)
        text = format_day(f"Сегодня — {place.name}", f0) + "\n\n" + format_day(f"Завтра — {place.name}", f1)
        await message.answer(text)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

