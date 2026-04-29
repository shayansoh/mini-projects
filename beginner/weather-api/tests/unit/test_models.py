from weather_api.models import WeatherData

def test_weather_data_defaults():
    data = WeatherData(
        city="Toronto",
        country="CA",
        temperature=15.0,
        feels_like=13.0,
        humidity=72,
        description="clear sky"
    )
    assert data.city == "Toronto"
    assert data.country == "CA"
    assert data.cached is False

def test_weather_data_cached_flag():
    data = WeatherData(
        city="Toronto",
        country="CA",
        temperature=15.0,
        feels_like=13.0,
        humidity=72,
        description="clear sky",
        cached=True
    )
    assert data.cached is True

def test_weather_data_serializes():
    data = WeatherData(
        city="Toronto",
        country="CA",
        temperature=15.0,
        feels_like=13.0,
        humidity=72,
        description="clear sky"
    )
    d = data.model_dump()
    assert d["city"] == "Toronto"
    assert d["cached"] is False
    assert "temperature" in d
    assert "humidity" in d