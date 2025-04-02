from aiogram.filters import BaseFilter
from aiogram.types import Message


MINUTES = ["минута", "минуты", "минут"]
HOURS = ["час", "часа", "часов"]
TIMES = MINUTES + HOURS


class BookTimeFilter(BaseFilter):
    async def __call__(self, message: Message, *args, **kwargs):
        if len(message.text.split(" ")) == 2:
            time, min_or_hour = message.text.split(" ")
            if not time.isdigit():
                return False
            if min_or_hour not in TIMES:
                return False
            return True
        if len(message.text.split(" ")) == 4:
            num_hour, hour, num_minute, minute = message.text.split(" ")
            print(num_hour, hour, num_minute, minute)
            if hour not in HOURS or minute not in MINUTES:
                return False
            if not num_minute.isdigit() or not num_hour.isdigit():
                return False
            return True
        return False
