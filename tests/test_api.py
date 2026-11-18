from unittest.mock import MagicMock, patch

import pytest

from src.aeroplanes.api import AeroplanesAPI


@patch("src.aeroplanes.api.requests.get")
def test_get_country_boundingbox(mock_get) -> None:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"boundingbox": ["1", "2", "3", "4"]}]
    mock_get.return_value = mock_response

    api = AeroplanesAPI()
    bbox = api.get_country_boundingbox("Spain")
    assert bbox == [1.0, 2.0, 3.0, 4.0]


@patch("src.aeroplanes.api.requests.get")
def test_get_aeroplanes(mock_get) -> None:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "states": [["icao", "CALL", "US", 0, 0, 0, 0, 1000.0, False, 100.0]]
    }
    mock_get.return_value = mock_response

    api = AeroplanesAPI()
    # подменяем boundingbox, чтобы не делать второй запрос
    api.get_country_boundingbox = MagicMock(return_value=[1, 2, 3, 4])
    result = api.get_aeroplanes("Spain")
    assert len(result) == 1