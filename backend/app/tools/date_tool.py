from datetime import datetime
from zoneinfo import ZoneInfo

_WEEKDAYS_ES = [
    "lunes",
    "martes",
    "miércoles",
    "jueves",
    "viernes",
    "sábado",
    "domingo",
]


def get_colombia_datetime() -> dict:
    now = datetime.now(ZoneInfo("America/Bogota"))
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "weekday": _WEEKDAYS_ES[now.weekday()],
        "week_number": now.isocalendar()[1],
        "iso_datetime": now.isoformat(),
    }
