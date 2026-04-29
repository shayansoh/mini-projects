import pytest
import httpx
from unittest.mock import MagicMock
from weather_api.client import get_weather, CityNotFoundError, WeatherServiceError


def make_mock_response(status_code: int, json_data: dict) -> MagicMock:
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = json_data
    return mock


VALID_RESPONSE = {
    "name": "Toronto",
    "sys": {"country": "CA"},
    "main": {"temp": 15.2, "feels_like": 13.1, "humidity": 72},
    "weather": [{"description": "clear sky"}],
}


def test_get_weather_returns_weather_data(mocker):
    mocker.patch("weather_api.client.httpx.get", return_value=make_mock_response(200, VALID_RESPONSE))
    result = get_weather("Toronto")
    assert result.city == "Toronto"
    assert result.country == "CA"
    assert result.temperature == 15.2
    assert result.humidity == 72
    assert result.cached is False


def test_get_weather_city_not_found(mocker):
    mocker.patch("weather_api.client.httpx.get", return_value=make_mock_response(404, {}))
    with pytest.raises(CityNotFoundError):
        get_weather("Fakecity")


def test_get_weather_invalid_api_key(mocker):
    mocker.patch("weather_api.client.httpx.get", return_value=make_mock_response(401, {}))
    with pytest.raises(WeatherServiceError, match="Unauthorized"):
        get_weather("Toronto")


def test_get_weather_unexpected_status(mocker):
    mocker.patch("weather_api.client.httpx.get", return_value=make_mock_response(500, {}))
    with pytest.raises(WeatherServiceError, match="unexpected error"):
        get_weather("Toronto")


def test_get_weather_timeout(mocker):
    mocker.patch("weather_api.client.httpx.get", side_effect=httpx.TimeoutException("timeout"))
    with pytest.raises(WeatherServiceError, match="timed out"):
        get_weather("Toronto")


def test_get_weather_connection_error(mocker):
    mocker.patch("weather_api.client.httpx.get", side_effect=httpx.RequestError("error"))
    with pytest.raises(WeatherServiceError, match="network connection"):
        get_weather("Toronto")


def test_get_weather_missing_api_key(mocker):
    mocker.patch("weather_api.client.OPENWEATHER_API_KEY", None)
    mocker.patch("weather_api.client.httpx.get")
    with pytest.raises(WeatherServiceError, match="not set"):
        get_weather("Toronto")