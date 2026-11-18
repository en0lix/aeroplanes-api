import os

import pytest

from src.aeroplanes.aeroplane import Aeroplane
from src.aeroplanes.storage import JSONSaver


@pytest.fixture
def temp_file(tmp_path):
    return str(tmp_path / "test.json")


def test_add_and_get(temp_file) -> None:
    saver = JSONSaver(temp_file)
    a = Aeroplane("CALL", "US", 100, 1000)
    saver.add_aeroplane(a)
    result = saver.get_aeroplanes()
    assert len(result) == 1
    assert result[0].callsign == "CALL"


def test_delete(temp_file) -> None:
    saver = JSONSaver(temp_file)
    a = Aeroplane("CALL", "US", 100, 1000)
    saver.add_aeroplane(a)
    saver.delete_aeroplane(a)
    assert saver.get_aeroplanes() == []


def test_get_by_criteria(temp_file) -> None:
    saver = JSONSaver(temp_file)
    saver.add_aeroplane(Aeroplane("A", "US", 100, 1000))
    saver.add_aeroplane(Aeroplane("B", "FR", 200, 2000))
    result = saver.get_aeroplanes(origin_country="US")
    assert len(result) == 1