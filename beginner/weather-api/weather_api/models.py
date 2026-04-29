from pydantic import BaseModel

class WeatherData(BaseModel):
    city: str
    country: str
    temperature: float
    feels_like: float
    humidity: int
    description: str
    cached: bool = False