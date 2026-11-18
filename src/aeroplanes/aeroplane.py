"""
Модуль с классом Aeroplane.
"""

from typing import Any, Dict, List


class Aeroplane:
    """
    Класс самолёта. Инкапсулирует атрибуты и валидирует их.

    Атрибуты:
        callsign (str): Позывной.
        origin_country (str): Страна регистрации.
        velocity (float): Скорость (м/с).
        altitude (float): Высота (м).
    """

    def __init__(
        self,
        callsign: str,
        origin_country: str,
        velocity: float,
        altitude: float,
    ) -> None:
        if not isinstance(callsign, str) or not callsign.strip():
            raise ValueError("Позывной должен быть непустой строкой")
        if not isinstance(origin_country, str) or not origin_country.strip():
            raise ValueError("Страна регистрации должна быть непустой строкой")
        if velocity is not None and (not isinstance(velocity, (int, float)) or velocity < 0):
            raise ValueError("Скорость должна быть неотрицательным числом")
        if altitude is not None and (not isinstance(altitude, (int, float)) or altitude < 0):
            raise ValueError("Высота должна быть неотрицательным числом")

        self._callsign = callsign.strip()
        self._origin_country = origin_country.strip()
        self._velocity = float(velocity) if velocity is not None else 0.0
        self._altitude = float(altitude) if altitude is not None else 0.0

    @property
    def callsign(self) -> str:
        return self._callsign

    @property
    def origin_country(self) -> str:
        return self._origin_country

    @property
    def velocity(self) -> float:
        return self._velocity

    @property
    def altitude(self) -> float:
        return self._altitude

    @classmethod
    def cast_to_object_list(cls, states: List[List[Any]]) -> List["Aeroplane"]:
        """
        Преобразует список состояний из opensky в список Aeroplane.

        Формат состояния opensky:
        [icao24, callsign, origin_country, time_position, last_contact,
         longitude, latitude, baro_altitude, on_ground, velocity, ...]
        """
        result: List[Aeroplane] = []
        for state in states:
            try:
                callsign = (state[1] or "").strip() or "UNKNOWN"
                origin_country = state[2] or "UNKNOWN"
                altitude = state[7] if state[7] is not None else 0.0
                velocity = state[9] if state[9] is not None else 0.0
                result.append(cls(callsign, origin_country, velocity, altitude))
            except (ValueError, IndexError):
                continue
        return result

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (
            self._callsign == other._callsign
            and self._origin_country == other._origin_country
        )

    def __lt__(self, other: "Aeroplane") -> bool:
        """Сравнение по скорости, затем по высоте."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        if self._velocity != other._velocity:
            return self._velocity < other._velocity
        return self._altitude < other._altitude

    def __le__(self, other: "Aeroplane") -> bool:
        return self == other or self < other

    def __gt__(self, other: "Aeroplane") -> bool:
        return not self <= other

    def __ge__(self, other: "Aeroplane") -> bool:
        return not self < other

    def __str__(self) -> str:
        return (
            f"{self._callsign} ({self._origin_country}): "
            f"скорость {self._velocity} м/с, высота {self._altitude} м"
        )

    def __repr__(self) -> str:
        return (
            f"Aeroplane(callsign={self._callsign!r}, "
            f"origin_country={self._origin_country!r}, "
            f"velocity={self._velocity}, altitude={self._altitude})"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Сериализация в словарь для JSON."""
        return {
            "callsign": self._callsign,
            "origin_country": self._origin_country,
            "velocity": self._velocity,
            "altitude": self._altitude,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Aeroplane":
        """Десериализация из словаря."""
        return cls(
            callsign=data["callsign"],
            origin_country=data["origin_country"],
            velocity=data["velocity"],
            altitude=data["altitude"],
        )