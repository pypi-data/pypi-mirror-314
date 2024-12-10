
# Weather Fetcher

`Weather Fetcher` is a Python package that allows users to fetch current weather data for a specified location using the OpenWeatherMap API. It is designed with best practices in mind and can be easily configured for use in different environments.

## Features

- Fetch current weather data for any location.

---

## Installation with Pipenv

### Install Production Dependencies
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/your-repo/weather-fetcher.git
   cd weather-fetcher
   ```

2. Install production dependencies:
   ```bash
   pipenv install
   ```

### Install Development Dependencies
If you are contributing to the project or need development tools, install the development dependencies:
```bash
pipenv install --dev
```

---

## Installation with Pip

### Install Production Dependencies
If you are not using `pipenv`, you can install production dependencies directly with `pip`:
```bash
pip install -r requirements.txt
```

### Install Development Dependencies
To include development tools like linters and testing frameworks, install `requirements-dev.txt`:
```bash
pip install -r requirements-dev.txt
```

---

## Setting Up the API Key

To use the OpenWeatherMap API, you need an API key. Sign up for free at [OpenWeatherMap](https://openweathermap.org/api) to get your key.

### Option 1: Using Environment Variables (Recommended)

Set the API key as an environment variable:
- **Linux/Mac**:
  ```bash
  export WEATHER_API_KEY="your_api_key"
  ```
- **Windows (Command Prompt)**:
  ```cmd
  set WEATHER_API_KEY=your_api_key
  ```
- **Windows (PowerShell)**:
  ```powershell
  $env:WEATHER_API_KEY="your_api_key"
  ```

---

## Running the Program

1. Create a script to fetch weather data. Here’s an example (`example.py`):
   ```python
   from weather_fetcher.core import WeatherFetcher

   # Initialize the Weather Fetcher
   fetcher = WeatherFetcher()

   # Fetch weather for a specific location
   try:
       data = fetcher.get_weather("New York")
       print("Weather Data:", data)
   except Exception as e:
       print("Error:", e)
   ```

2. Run the script inside the `pipenv` shell:
   ```bash
   python example.py
   ```

   Or run it directly with `pipenv`:
   ```bash
   pipenv run python example.py
   ```

   If using `pip`:
   ```bash
   python example.py
   ```

---

## Expected Output

If everything is set up correctly, the program will print the weather data for the specified location. Example:
```json
{
    "weather": [
        {
            "description": "clear sky",
            "icon": "01d"
        }
    ],
    "main": {
        "temp": 293.15,
        "humidity": 53
    },
    "name": "New York"
}
```

---

## Debugging Tips

- **API Key Not Found**: Ensure the API key is correctly set in the environment variable or `config.json`.
- **Invalid Location Format**: Check that the location string is not empty or malformed.
- **City Not Found**: Verify the location exists and is correctly spelled.
- **API Errors**: Check the API response for error messages and ensure your API key is valid and active.

---

## Development Workflow

### Linting and Formatting
Run `flake8` for linting:
```bash
pipenv run flake8
```

Run `black` for code formatting:
```bash
pipenv run black .
```

### Running Tests
Run unit tests using `pytest`:
```bash
pipenv run pytest
```

If using `pip`:
```bash
pytest
```

---

## Requirements

- Python 3.6+
- Production dependencies listed in `requirements.txt`
- Development dependencies listed in `requirements-dev.txt`

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgments

This project uses the OpenWeatherMap API. You can find more information at [OpenWeatherMap](https://openweathermap.org/).

---
