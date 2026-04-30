from unittest.mock import MagicMock, patch
from weather_api.cache import get, set
from weather_api.models import WeatherData

SAMPLE_DATA = WeatherData(
    city="Toronto",
    country="CA",
    temperature=15.2,
    feels_like=13.1,
    humidity=72,
    description="clear sky"
)

def test_get_returns_none_on_cache_miss(mocker):
    mock_client = MagicMock()
    mock_client.get.return_value = None
    mocker.patch("weather_api.cache._get_client", return_value=mock_client)
    result = get("Toronto")
    assert result is None

def test_get_returns_weather_data_on_cache_hit(mocker):
    mock_client = MagicMock()
    mock_client.get.return_value = SAMPLE_DATA.model_dump_json()
    mocker.patch("weather_api.cache._get_client", return_value=mock_client)
    result = get("Toronto")
    assert result is not None
    assert result.city == "Toronto"
    assert result.cached == False

def test_get_normalizes_city_key(mocker):
    mock_client = MagicMock()
    mock_client.get.side_effect = Exception("Redis down")
    mocker.patch("weather_api.cache._get_client", return_value=mock_client)
    result = get("  ToRoNtO  ")
    mock_client.get.assert_called_once_with("weather:toronto")

def test_get_returns_none_on_redis_error(mocker):
    mock_client = MagicMock()
    mock_client.get.side_effect = Exception("Redis down")
    mocker.patch("weather_api.cache._get_client", return_value=mock_client)
    result = get("Toronto")
    assert result is None

def test_set_stores_data(mocker):
    mock_client = MagicMock()
    mocker.patch("weather_api.cache._get_client", return_value=mock_client)
    set("Toronto", SAMPLE_DATA)
    mock_client.setex.assert_called_once()
    
def test_set_normalizes_city_key(mocker):
    mock_client = MagicMock()
    mocker.patch("weather_api.cache._get_client", return_value=mock_client)
    set("  TORONTO  ", SAMPLE_DATA)
    call_args = mock_client.setex.call_args[0]
    assert call_args[0] == "weather:toronto"

def test_set_silently_fails_on_redis_error(mocker):
    mock_client = MagicMock()
    mock_client.setex.side_effect = Exception("Redis down")
    mocker.patch("weather_api.cache._get_client", return_value=mock_client)
    set("Toronto", SAMPLE_DATA)