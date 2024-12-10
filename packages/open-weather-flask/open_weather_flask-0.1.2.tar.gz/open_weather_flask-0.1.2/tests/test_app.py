import unittest
from unittest.mock import patch, MagicMock
from weather_fetcher.core import WeatherFetcher


class TestWeatherFetcher(unittest.TestCase):
    @patch.dict("os.environ", {"WEATHER_API_KEY": "test_api_key"})
    @patch("weather_fetcher.api.WeatherAPI.fetch_weather")
    def test_get_weather_success(self, mock_fetch_weather):
        # Mock API response
        mock_response = {
            "weather": [{"description": "clear sky"}],
            "main": {"temp": 298.15},
        }
        mock_fetch_weather.return_value = mock_response

        # Instantiate WeatherFetcher and test
        fetcher = WeatherFetcher()
        response = fetcher.get_weather("New York")
        self.assertIn("weather", response)
        self.assertEqual(response["main"]["temp"], 298.15)

    @patch.dict("os.environ", {"WEATHER_API_KEY": "test_api_key"})
    @patch("weather_fetcher.api.WeatherAPI.fetch_weather")
    def test_get_weather_failure(self, mock_fetch_weather):
        # Mock API failure
        mock_fetch_weather.side_effect = Exception("API error")

        fetcher = WeatherFetcher()
        with self.assertRaises(Exception) as context:
            fetcher.get_weather("Invalid City")
        self.assertIn("API error", str(context.exception))

    @patch.dict("os.environ", {}, clear=True)  # Clear environment for this test
    def test_missing_api_key(self):
        # Ensure WEATHER_API_KEY is not set
        with self.assertRaises(ValueError) as context:
            WeatherFetcher()
        self.assertIn("API key not found", str(context.exception))


if __name__ == "__main__":
    unittest.main()
