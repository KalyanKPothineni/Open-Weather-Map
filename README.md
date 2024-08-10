# Weather Now - OpenWeatherMap API Python Script

## Project Overview

**Weather Now** is a Python-based command-line application that allows users to retrieve current weather data and extended forecasts for a specific location using the OpenWeatherMap API. Users can input a city name, country code, or zip code, and the program will fetch and display weather information in a user-friendly format.

## Features

- **Current Weather Information**: Displays current temperature, weather conditions, humidity, and more for the specified location.
- **Extended Forecast**: A 36-hour forecast with temperature and weather conditions.
- **Temperature Conversion**: Converts temperature from Kelvin to Fahrenheit and Celsius.
- **Error Handling**: Includes robust error handling for invalid inputs, API connection issues, and other potential errors.

## Usage

- Enter a U.S. zip code or a city name followed by a comma and the two-letter country code (e.g., `London, GB`).
- The program will display the current weather and a 36-hour forecast.
- Users can choose to search for another location or exit the program.

## Error Handling

The program includes error handling for:

- **Invalid location input**: Alerts the user if the provided city or zip code is not found.
- **API Connection Issues**: Handles API connectivity errors or timeout errors.
- **Invalid User Input**: Prompts users to re-enter valid input if an invalid selection is made.

## Requirements

- Python 3.x
- `requests` library for making HTTP requests
- OpenWeatherMap API key
