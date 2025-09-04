from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class Place:
    name: str
    latitude: float
    longitude: float
    country: Optional[str] = None
    admin1: Optional[str] = None
    timezone: Optional[str] = None


class OpenMeteoGeocoder:
    base_url = "https://geocoding-api.open-meteo.com/v1/search"

    def search(self, name: str) -> Optional[Place]:
        params = {
            "name": name,
            "count": 1,
            "language": "ru",
            "format": "json",
        }
        r = requests.get(self.base_url, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
        results = data.get("results") or []
        if not results:
            return None
        item = results[0]
        return Place(
            name=item.get("name") or name,
            latitude=float(item["latitude"]),
            longitude=float(item["longitude"]),
            country=item.get("country"),
            admin1=item.get("admin1"),
            timezone=item.get("timezone"),
        )


