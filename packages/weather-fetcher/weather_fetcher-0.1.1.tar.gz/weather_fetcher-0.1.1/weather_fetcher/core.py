import os
import logging
from .api import WeatherAPI
from .utils import validate_location

logging.basicConfig(level=logging.INFO)


class WeatherFetcher:
    def __init__(self):
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            raise ValueError(
                "API key not found. Set the WEATHER_API_KEY environment variable."
            )
        self.api = WeatherAPI(api_key)

    def get_weather(self, location):
        if not validate_location(location):
            logging.error("Invalid location format.")
            raise ValueError("Invalid location format.")

        try:
            data = self.api.fetch_weather(location)
            return data
        except Exception as e:
            logging.error(f"Error fetching weather: {e}")
            raise
