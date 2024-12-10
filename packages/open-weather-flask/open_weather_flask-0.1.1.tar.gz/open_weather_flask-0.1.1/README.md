
# Open Weather Flask

Open Weather Flask is a Python-based application that retrieves and displays real-time weather information for specified locations. It provides an API that fetches current weather data using the OpenWeatherMap API.

## Features

- Fetches real-time weather data for any specified location.
- Provides a RESTful API for programmatic access to weather information.

## Requirements

- Python 3.6 or higher
- OpenWeatherMap API key

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/testinapps/open-weather-flask.git
   cd open-weather-flask
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   # Activate the virtual environment:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install .
   ```

4. **Configure the API Key**:
   - Obtain a free API key from [OpenWeatherMap](https://openweathermap.org/).
   - Set the `OPENWEATHER_API_KEY` environment variable with your API key:
     ```bash
     export OPENWEATHER_API_KEY=your_api_key_here
     ```

## Usage

1. **Run the Application**:
   ```bash
   python -m weather_fetcher
   ```

2. **Access the API**:
   - Use tools like `curl` or Postman to interact with the API.
   - Example:
     ```bash
     curl "http://127.0.0.1:5000/weather?location=New York"
     ```
   - The API will return JSON with current weather data for the specified location.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
