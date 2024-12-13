from datetime import datetime
from typing import Dict, Tuple
import requests
import logging
from .types import WeatherType

from cachetools import cached, TTLCache
import python_weather

logger = logging.getLogger(__name__)

# Cache weather results for 5 minutes (300 seconds)
weather_cache = TTLCache(maxsize=100, ttl=300)

class WeatherService:
    def __init__(self):
        pass

    @cached(weather_cache)
    async def get_weather(self, location: Tuple[float, float]) -> WeatherType:
        """
        Get weather forecast for given location coordinates
        Args:
            location: Tuple of (latitude, longitude)
        Returns:
            WeatherType enum indicating current weather
        """
        try:
            lat, lon = location
            async with python_weather.Client(format="celsius") as client:
                weather = await client.get(f"{lat},{lon}")
                return self._categorize_weather(weather.current)
        except python_weather.InvalidCredentials:
            logger.error("Weather API credentials are invalid or not configured")
            return WeatherType.MODERATE
        except (python_weather.ClientError, python_weather.NetworkError) as e:
            logger.error(f"Weather API network error: {str(e)}")
            return WeatherType.MODERATE
        except Exception as e:
            logger.error(f"Unexpected weather API error: {str(e)}", exc_info=True)
            return WeatherType.MODERATE

    def _categorize_weather(self, current_weather) -> WeatherType:
        """Categorize weather conditions based on temperature and precipitation"""
        temp = current_weather.temperature
        
        if current_weather.kind in [python_weather.RAIN, python_weather.SNOW]:
            return WeatherType.RAINY
        elif temp > 28:
            return WeatherType.HOT
        elif temp < 15:
            return WeatherType.COLD
        else:
            return WeatherType.MODERATE 