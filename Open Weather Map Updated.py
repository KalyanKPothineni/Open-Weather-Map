######################################
# DSC 510
# Week 12
# Programming Assignment Week 12
# Description: This program will allows the user to input a location and
# call an API to get lat/long, second api to get the weather by lat/long and
# gathers data from openweathermap.org and prints weather information in a
# readable format for said location
# Author: Kalyan Pothineni
# 05/25/2023
######################################
import requests
import json

# define OpenWeatherMap API key and base URL
API_KEY = "ac4a3c5a4c288da716e237359597874f"
BASE_URL = "http://api.openweathermap.org/data/2.5/"
# special character used to represent degrees of temperature
DEGREE_SYMBOL = "\u00b0"

def kelvin_to_celsius(temp_kelvin):
    """
    Function to convert temperature from Kelvin to Celsius
    """
    return temp_kelvin - 273.15

def kelvin_to_fahrenheit(temp_kelvin):
    """
    Function to convert temperature from Kelvin to Fahrenheit
    """
    return (temp_kelvin - 273.15) * 9/5 + 32

def get_weather_by_zip(zip_code, unit):
    """
    Function to get weather data for a given location by ZIPCODE
    """
    try:
        geo_url = f"{BASE_URL}weather?zip={zip_code},&appid={API_KEY}"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()

        if geo_response.status_code == 200:
            lat = geo_data["coord"]["lat"]
            lon = geo_data["coord"]["lon"]
            weather_url = f"{BASE_URL}weather?lat={lat}&lon={lon}&appid={API_KEY}"
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()

            if weather_response.status_code == 200:
                display_weather_data(weather_data, unit)
            else:
                print("Failed to retrieve weather data.")
        else:
            print("Invalid zip code. Please try again.")
    except requests.exceptions.RequestException as e:
        print("Connection error:", str(e))
        return None

def get_weather_by_city(city, state, unit):
    """
    Function to get weather data for a given location by City and state
    """
    try:
        geo_url = f"{BASE_URL}weather?q={city},{state},US,&appid={API_KEY}"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()

        if geo_response.status_code == 200:
            lat = geo_data["coord"]["lat"]
            lon = geo_data["coord"]["lon"]

            weather_url = f"{BASE_URL}weather?lat={lat}&lon={lon}&appid={API_KEY}&units={unit}"
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()

            if weather_response.status_code == 200:
                display_weather_data(weather_data, unit)
            else:
                print("Failed to retrieve weather data.")
        else:
            print("Invalid city or state. Please check and correct city name or"
                  " state (State name should be in full) .")
    except requests.exceptions.RequestException as e:
        print("Connection error:", str(e))
        return None

def display_weather_data(weather_data, unit):
    """
    Function to display weather data in a readable/printable format
    Parse the json
    Convert the temperatures
    """
    city = str(json.dumps(weather_data['name'])).replace('"', '')
    country = str(json.dumps(weather_data['sys']['country'])).replace('"', '')
    desc = str(json.dumps(weather_data['weather'][0]['description'])).\
        replace('"', '').title()
    temp = float(json.dumps(weather_data['main']['temp']))
    real_feel = float(json.dumps(weather_data['main']['feels_like']))
    pressure = float(json.dumps(weather_data['main']['pressure']))
    humidity = float(json.dumps(weather_data['main']['humidity']))
    speed = float(json.dumps(weather_data['wind']['speed']))

    if unit == "C":
        temperature = kelvin_to_celsius(temp)
        feels_like = kelvin_to_celsius(real_feel)
        temperature_unit = "°C"
    elif unit == "F":
        temperature = kelvin_to_fahrenheit(temp)
        feels_like = kelvin_to_fahrenheit(real_feel)
        temperature_unit = "°F"
    else:
        temperature = temp
        feels_like = real_feel
        temperature_unit = "K"

    print(f"{'':-<40}\n"
          f'Weather Report for {city}, {country}:\n'
          f'\tCurrent Temperature: {round(temperature,2)},'
          f' {temperature_unit}\n'
          f'\tFeels Like: {round(feels_like,2)},{temperature_unit}\n'
          f'\tCurrent Conditions: {desc}\n'
          f'\tAtmospheric Pressure: {pressure} hPa\n'
          f'\tHumidity: {humidity}%\n'
          f'\tWind Speed: {speed}%\n'
          f"{'':-<40}"
          )

def main():
    print("Welcome to the Weather Forecast App!")
    print()

    while True:
        print("Please select an option:")
        print("1. Get weather by ZIP code")
        print("2. Get weather by city and state")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            zip_code = input("Enter ZIP code: ")
            unit = input("Enter temperature unit (C/F/K): ").upper()
            get_weather_by_zip(zip_code, unit)
        elif choice == "2":
            city = input("Enter City Name: ").upper()
            state = input("Enter Full State Name (Example: Texas): ").upper()
            unit = input("Enter temperature unit (C/F/K): ").upper()
            get_weather_by_city(city, state, unit)
        elif choice == "0":
            print('Thank you for using Weather Now! Goodbye')
            break
        else:
            print("Invalid choice. Please try again.")
        print()

if __name__ == "__main__":
    main()
