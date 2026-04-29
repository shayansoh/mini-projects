import os
import httpx
from dotenv import load_dotenv
from weather_api.models import WeatherData

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

class CityNotFoundError(Exception):
    pass

class WeatherServiceError(Exception):
    pass

def get_weather(city: str) -> WeatherData:
    if not OPENWEATHER_API_KEY:
        raise WeatherServiceError("API key is not set. Please set the OPENWEATHER_API_KEY environment variable.")
    
    try:
        response = httpx.get(
            BASE_URL, 
            params={"q": city, 
                    "appid": OPENWEATHER_API_KEY, 
                    "units": "metric"
                    },
                    timeout=10.0
            )
    except httpx.TimeoutException:
        raise WeatherServiceError("The request timed out. Please try again later.")
    
    except httpx.RequestError:
        raise WeatherServiceError("An error occurred while making the request. Please check your network connection and try again.")
    
    if response.status_code == 404:
        raise CityNotFoundError(f"City '{city}' not found. Please check the city name and try again.")
    
    if response.status_code == 401:
        raise WeatherServiceError("Unauthorized access. Please check your API key and try again.")
    
    if response.status_code != 200:
        raise WeatherServiceError(f"An unexpected error occurred: {response.status_code}")
    
    data = response.json()

    return WeatherData(
        city=data["name"],
        country=data["sys"]["country"],
        temperature=data["main"]["temp"],
        feels_like=data["main"]["feels_like"],
        humidity=data["main"]["humidity"],
        description=data["weather"][0]["description"]
    )