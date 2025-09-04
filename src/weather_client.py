import datetime as dt
from dataclasses import dataclass
from typing import Dict, Any, Optional

import requests


CHELYABINSK_LAT = 55.1644
CHELYABINSK_LON = 61.4368


@dataclass
class DayForecast:
    date: dt.date
    temp_min: float
    temp_max: float
    wind_speed_max: float
    precipitation_sum: float
    weathercode: int
    sunrise: Optional[str]
    sunset: Optional[str]


class OpenMeteoClient:
    base_url = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, latitude: float = CHELYABINSK_LAT, longitude: float = CHELYABINSK_LON, tz: str = "auto") -> None:
        self.latitude = latitude
        self.longitude = longitude
        self.tz = tz

    def fetch(self) -> Dict[str, Any]:
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timezone": self.tz,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "sunrise",
                "sunset",
                "precipitation_sum",
                "weathercode",
                "windspeed_10m_max",
            ],
        }
        response = requests.get(self.base_url, params=params, timeout=20)
        response.raise_for_status()
        return response.json()

    def get_day(self, offset_days: int = 0) -> DayForecast:
        data = self.fetch()
        daily = data["daily"]
        idx = offset_days
        date = dt.date.fromisoformat(daily["time"][idx])
        return DayForecast(
            date=date,
            temp_min=float(daily["temperature_2m_min"][idx]),
            temp_max=float(daily["temperature_2m_max"][idx]),
            wind_speed_max=float(daily["windspeed_10m_max"][idx]),
            precipitation_sum=float(daily["precipitation_sum"][idx]),
            weathercode=int(daily["weathercode"][idx]),
            sunrise=daily.get("sunrise", [None])[idx],
            sunset=daily.get("sunset", [None])[idx],
        )


