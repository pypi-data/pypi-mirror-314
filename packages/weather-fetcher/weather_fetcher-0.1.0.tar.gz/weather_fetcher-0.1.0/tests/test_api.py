import unittest
from weather_fetcher.api import WeatherAPI


class TestWeatherAPI(unittest.TestCase):
    def test_fetch_weather(self):
        api = WeatherAPI(api_key="test_key")
        with self.assertRaises(Exception):
            api.fetch_weather("InvalidCity")
