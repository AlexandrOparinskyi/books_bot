import math

TIME_DATA = {
    "30m": 30,
    "1h": 60,
    "1h30m": 90,
    "2h": 120,
    "2h30m": 150,
    "3h": 180
}


def calculate_minute_and_hour(hour: int, minute: int) -> int:
    """Считает общее кол-во минут по времени"""
    return hour * 60 + minute


def calculate_point_from_time(message: str) -> tuple[int, int]:
    """Считает количество заработанных очков"""
    if len(message.split(" ")) == 2:
        time, min_or_hour = message.split(' ')
        if min_or_hour.lower().startswith("ча"):
            return math.floor(int(time) * 60 / 10), int(time) * 60
        else:
            return math.floor(int(time) / 10), int(time)
    hour, _, minute, _ = message.split(' ')
    minute = calculate_minute_and_hour(int(hour), int(minute))
    return math.floor(minute / 10), minute
