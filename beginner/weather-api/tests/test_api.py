import pytest
from fastapi.testclient import TestClient
from weather_api.api import app
from weather_api.models import WeatherData
from weather_api.client import CityNotFoundError, WeatherServiceError


SAMPLE_DATA = WeatherData(
    city="Toronto",
    country="CA",
    temperature=15.2,
    feels_like=13.1,
    humidity=72,
    description="clear sky",
)

@pytest.fixture
def client():
    return TestClient(app)


def test_weather_returns_200_on_cache_miss(client, mocker):
    mocker.patch("weather_api.api.cache.get", return_value=None)
    mocker.patch("weather_api.api.get_weather", return_value=SAMPLE_DATA)
    mocker.patch("weather_api.api.cache.set")
    response = client.get("/weather?city=Toronto")
    assert response.status_code == 200
    assert response.json()["city"] == "Toronto"
    assert response.json()["cached"] is False


def test_weather_returns_cached_data(client, mocker):
    cached = SAMPLE_DATA.model_copy()
    mocker.patch("weather_api.api.cache.get", return_value=cached)
    response = client.get("/weather?city=Toronto")
    assert response.status_code == 200
    assert response.json()["cached"] is True


def test_weather_stores_result_in_cache(client, mocker):
    mocker.patch("weather_api.api.cache.get", return_value=None)
    mocker.patch("weather_api.api.get_weather", return_value=SAMPLE_DATA)
    mock_set = mocker.patch("weather_api.api.cache.set")
    client.get("/weather?city=Toronto")
    mock_set.assert_called_once()


def test_weather_returns_404_on_city_not_found(client, mocker):
    mocker.patch("weather_api.api.cache.get", return_value=None)
    mocker.patch("weather_api.api.get_weather", side_effect=CityNotFoundError("City 'Fakecity' not found"))
    response = client.get("/weather?city=Fakecity")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_weather_returns_503_on_service_error(client, mocker):
    mocker.patch("weather_api.api.cache.get", return_value=None)
    mocker.patch("weather_api.api.get_weather", side_effect=WeatherServiceError("Service unavailable"))
    response = client.get("/weather?city=Toronto")
    assert response.status_code == 503
    assert "detail" in response.json()


def test_weather_missing_city_param(client):
    response = client.get("/weather")
    assert response.status_code == 422