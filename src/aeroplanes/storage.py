"""
Модуль с абстрактным хранилищем и JSONSaver.
"""

import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from .aeroplane import Aeroplane


class BaseStorage(ABC):
    """Абстрактный класс хранилища."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет самолёт в хранилище."""
        ...

    @abstractmethod
    def get_aeroplanes(self, **criteria: Any) -> List[Aeroplane]:
        """Возвращает самолёты по критериям."""
        ...

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет самолёт из хранилища."""
        ...


class JSONSaver(BaseStorage):
    """Хранилище в JSON-файле."""

    def __init__(self, filename: str = "aeroplanes.json") -> None:
        self._filename = filename

    def _load(self) -> List[Dict[str, Any]]:
        try:
            with open(self._filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save(self, data: List[Dict[str, Any]]) -> None:
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._load()
        data.append(aeroplane.to_dict())
        self._save(data)

    def get_aeroplanes(self, **criteria: Any) -> List[Aeroplane]:
        data = self._load()
        result: List[Aeroplane] = []
        for item in data:
            aeroplane = Aeroplane.from_dict(item)
            if all(getattr(aeroplane, key) == value for key, value in criteria.items()):
                result.append(aeroplane)
        return result

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._load()
        data = [
            item for item in data
            if not (
                item["callsign"] == aeroplane.callsign
                and item["origin_country"] == aeroplane.origin_country
            )
        ]
        self._save(data)