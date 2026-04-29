# Weather API Wrapper

Source: [https://roadmap.sh/projects/weather-api-wrapper-service](https://roadmap.sh/projects/weather-api-wrapper-service)

A REST API that wraps the OpenWeatherMap API, adds in-memory caching via Redis, and returns current weather data by city. Covers third-party API integration, environment variable management, caching strategy, and rate limiting.

## Demo

TBD

## Getting Started

Prerequisites: Python 3.10+, Redis

```bash
git clone https://github.com/<your-username>/mini-projects.git
cd mini-projects/beginner/weather-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your API key and Redis connection string
python main.py
```

## Requirements

Build a REST API that fetches weather data from OpenWeatherMap and returns it to the client. The API should cache responses to avoid redundant upstream calls.

The service must:

- Accept a city name as input and return its current weather data
- Fetch data from [OpenWeatherMap](https://openweathermap.org/api)
- Cache responses in Redis using the city name as the key
- Automatically expire cached entries after 12 hours
- Return cached data on repeat requests within the expiry window
- Implement rate limiting to prevent abuse
- Handle errors gracefully -- invalid city, API downtime, missing credentials

Constraints:

- API keys and connection strings stored in environment variables, never hardcoded
- Return appropriate HTTP status codes and error messages

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/weather?city=Toronto` | Returns current weather for the given city |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENWEATHER_API_KEY` | API key from openweathermap.org |
| `REDIS_URL` | Redis connection string |

## Caching Strategy

- Cache key: city name normalized to lowercase
- Cache store: Redis
- TTL: 12 hours
- On cache hit: return stored response directly
- On cache miss: fetch from upstream, store result, return to client