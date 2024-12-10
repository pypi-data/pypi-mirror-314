import unittest
import os
from unittest.mock import patch
from weather_fetcher.core import WeatherFetcher


class TestWeatherFetcher(unittest.TestCase):
    def setUp(self):
        # Set a mock API key in the environment for testing
        os.environ["WEATHER_API_KEY"] = "test_api_key"
        self.fetcher = WeatherFetcher()

    def tearDown(self):
        # Clean up environment variables
        if "WEATHER_API_KEY" in os.environ:
            del os.environ["WEATHER_API_KEY"]

    def test_valid_location(self):
        # Test that invalid location raises ValueError
        with self.assertRaises(ValueError):
            self.fetcher.get_weather("")

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_key(self):
        # Ensure ValueError is raised when API key is not set
        with self.assertRaises(ValueError):
            WeatherFetcher()
