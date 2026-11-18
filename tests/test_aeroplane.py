import pytest

from src.aeroplanes.aeroplane import Aeroplane


def test_creation() -> None:
    a = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
    assert a.callsign == "UAL1621"
    assert a.origin_country == "United States"
    assert a.velocity == 268.79
    assert a.altitude == 10203.18


def test_invalid_callsign() -> None:
    with pytest.raises(ValueError):
        Aeroplane("", "US", 100, 1000)


def test_invalid_velocity() -> None:
    with pytest.raises(ValueError):
        Aeroplane("A", "US", -1, 1000)


def test_comparison() -> None:
    a = Aeroplane("A", "US", 100, 5000)
    b = Aeroplane("B", "US", 200, 6000)
    assert a < b
    assert b > a


def test_cast_to_object_list() -> None:
    states = [
        ["icao", "CALL1", "US", 0, 0, 0, 0, 10000.0, False, 250.0],
    ]
    result = Aeroplane.cast_to_object_list(states)
    assert len(result) == 1
    assert result[0].callsign == "CALL1"