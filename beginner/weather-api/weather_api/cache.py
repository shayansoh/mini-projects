import os
import redis
from typing import Optional, cast
from dotenv import load_dotenv
from weather_api.models import WeatherData

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CACHE_TTL = 12 * 60 * 60  # 12 hours in seconds

def _get_client() -> redis.Redis:
    return redis.from_url(REDIS_URL)

def _cache_key(city: str) -> str:
    return f"weather:{city.lower().strip()}"

def get(city: str) -> Optional[WeatherData]:
    try:
        client = _get_client()
        raw = client.get(_cache_key(city))
        if raw is None:
            return None
        value = cast(bytes, raw)
        return WeatherData.model_validate_json(value)
    except Exception:
        return None
    
def set(city: str, data: WeatherData) -> None:
    try:
        client = _get_client()
        client.setex(
            _cache_key(city), 
            CACHE_TTL, 
            data.model_dump_json()
        )
    except Exception:
        pass