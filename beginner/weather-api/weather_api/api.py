from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.requests import Request

from weather_api import cache
from weather_api.client import get_weather, CityNotFoundError, WeatherServiceError
from weather_api.models import WeatherData

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) # type: ignore[arg-type]


@app.get("/weather", response_model=WeatherData)
@limiter.limit("10/minute")
def weather(request: Request, city: str = Query(..., description="City name")):
    cached = cache.get(city)
    if cached:
        cached.cached = True
        return cached

    try:
        data = get_weather(city)
    except CityNotFoundError as e:
        return JSONResponse(status_code=404, content={"detail": str(e)})
    except WeatherServiceError as e:
        return JSONResponse(status_code=503, content={"detail": str(e)})

    cache.set(city, data)
    return data