from flask import Flask, request, jsonify
from weather_fetcher.core import WeatherFetcher

# Create Flask app
app = Flask(__name__)

# Initialize WeatherFetcher instance
fetcher = WeatherFetcher()


@app.route("/weather", methods=["GET"])
def get_weather():
    location = request.args.get("location", "")
    if not location:
        return jsonify({"error": "Location is required"}), 400

    # Fetch and return weather data
    try:
        weather_data = fetcher.get_weather(location)
        return jsonify(weather_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/status", methods=["GET"])
def status():
    """Return the server status."""
    return jsonify({"status": "running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
