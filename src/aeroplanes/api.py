"""
Модуль для работы с API nominatim.openstreetmap.org и opensky-network.org.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import requests


class BaseAPI(ABC):
    """Абстрактный класс для работы с API."""

    @abstractmethod
    def _get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Выполняет GET-запрос и возвращает JSON."""
        ...


class AeroplanesAPI(BaseAPI):
    """
    Класс для работы с API nominatim и opensky.
    """

    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    OPENSKY_URL = "https://opensky-network.org/api/states/all"

    def _get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Выполняет GET-запрос, проверяет статус, возвращает JSON."""
        response = requests.get(url, params=params, timeout=30)
        if response.status_code != 200:
            raise RuntimeError(
                f"Ошибка запроса: {response.status_code} — {response.text[:200]}"
            )
        return response.json()

    def get_country_boundingbox(self, country: str) -> List[float]:
        """
        Возвращает boundingbox страны: [south, north, west, east].
        """
        params = {"q": country, "format": "json", "limit": 1}
        data = self._get(self.NOMINATIM_URL, params=params)
        if not data:
            raise ValueError(f"Страна не найдена: {country}")
        return [float(x) for x in data[0]["boundingbox"]]

    def get_aeroplanes(self, country: str) -> List[Dict[str, Any]]:
        """
        Возвращает список самолётов в воздушном пространстве страны.
        """
        south, north, west, east = self.get_country_boundingbox(country)
        params = {
            "lamin": south,
            "lamax": north,
            "lomin": west,
            "lomax": east,
        }
        data = self._get(self.OPENSKY_URL, params=params)
        return data.get("states", []) or []