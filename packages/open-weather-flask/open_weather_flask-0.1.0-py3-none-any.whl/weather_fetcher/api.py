import requests


class WeatherAPI:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_weather(self, location):
        params = {"q": location, "appid": self.api_key}
        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()  # Raise an error for HTTP codes >= 400
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error fetching weather data: {e}")
