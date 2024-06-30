######################################
# DSC 510
# Week 12
# Programming Assignment Week 12
# Description: A program that allows the user to input a location (city,
# country or zip code), gathers data from openweathermap.org and prints weather
# information in a readable format for said location
# Author: Kalyan Pothineni
# 11/10/2022
######################################
# Change#:1
# Change(s) Made: Added convert temperature
# Date of Change: 11/12/2022
# Author: Kalyan Pothineni
# Submission date: 11/19/2022
######################################
# Change#:2
# Change(s) Made: Add extended temperature, next 36hours
# Date of Change: 11/14/2022
# Author: Kalyan Pothineni
# Submission date: 11/19/2022
######################################
# Change#:3
# Change(s) Made: Include error handling, try/block
# Date of Change: 11/16/2022
# Author: Kalyan Pothineni
# Submission date: 11/19/2022
######################################
import json
import time
import requests

print('Welcome to Weather Now! Access current weather data.\n'
"\nFor a precise forecast, please enter the 5 digit U.S. Zip Code for you "
"location \n"
"or the city's name, comma, and 2-letter country code, as highlighted below.\n"
'Selections made without a country code may return inaccurate results / cities'
'.\n'
"Examples...London, GB / New York, US / Madrid, ES...Let's Begin!\n"
)

'''
Main function for the program, allows user to input a zip code or city
to receive current/future forecast
'''
def main():
    url = 'https://api.openweathermap.org/data/2.5/weather'
    url_ext = 'https://api.openweathermap.org/data/2.5/forecast'
    location = input('Please enter the Zip Code or City, Country: ')
    while True:
        try:
            weather_current(location, url)
            weather_extended(location, url_ext)
            print('')
            more_weather()
            break
        except LookupError:
            print('')
            more_weather()
            break

'''
Makes a GET request to the url for current weather,
verifies connection is made, parses and displays the data
'''
def weather_current(location, url):
    if location.isdigit() is True:
        query_params = {'zip': location,
                        'APPID': 'e0658f792164bea0f30488a83ec7f9c9'}
    else:
        query_params = {'q': location,
                        'APPID': 'e0658f792164bea0f30488a83ec7f9c9'}
    response = requests.get(url, params=query_params, timeout=(5, 14))
    try_web(response, location)
    if response.status_code == 200:
        print(f"{'':-<100}\n"
              'Connected....Location Found')
    current_parsed = json.loads(response.text)
    current_formatted(current_parsed)

'''
Makes a GET request to the url for extended forecast,
parses and displays the data
'''
def weather_extended(location, url_ext):
    if location.isdigit() is True:
        query_params = {'zip': location, 'cnt': 16,
                        'APPID': 'e0658f792164bea0f30488a83ec7f9c9'}
    else:
        query_params = {'q': location, 'cnt': 16,
                        'APPID': 'e0658f792164bea0f30488a83ec7f9c9'}
    response = requests.get(url_ext, params=query_params, timeout=(5, 14))
    try_web(response, location)
    ext_parsed = json.loads(response.text)
    ext_formatted(ext_parsed)

'''
Converts Kelvin temperatures to Fahrenheit and Celsius
'''
def convert_temp(temp):
    f_degree = round((((temp - 273.15)*9)/5)+32)
    c_degree = round(temp - 273.15)
    return f'{f_degree}{chr(176)}F / {c_degree}{chr(176)}C'

'''
Try Except block to test the request was successful,
additionally checking if the city or zip code entered is valid by using
404 status code
'''
def try_web(response, location):
    try:
        response.raise_for_status()
    except requests.HTTPError as error0:
        if response.status_code == 404:
            if location.isdigit() is True:
                print(f"The zip code entered '{location}' "
                      f"was not found or is not valid.")
            else:
                if location.__contains__(','):
                    print(f"The city entered '"
                          f"{location[0:-2].title() + location[-2:].upper()}' "
                          f"was not found.")
                else:
                    print(f"The city entered '{location.title()}' "
                          f"was not found.")
        else:
            print('Even we do not have access to single digit zip codes.')
            print(f'{error0}')
    except requests.ConnectionError as error1:
        print('Error Connecting')
        print(error1)
    except requests.Timeout as error2:
        print('Timeout Error')
        print(error2)
    except requests.RequestException as error3:
        print('Something Else Went Wrong')
        print(error3)

'''
Decodes the JSON data, formats the time variables to match proper
time zones, then formats the printable output of the current weather
'''
def current_formatted(parsed):
    city = str(json.dumps(parsed['name'])).replace('"', '')
    country = str(json.dumps(parsed['sys']['country'])).replace('"', '')
    timezone = int(json.dumps(parsed['timezone']))
    epoch_time = int(json.dumps(parsed['dt']))
    true_time = epoch_time + timezone
    current_time = time.strftime("%A, %b %d, %Y %I:%M %p (local time)",
                                 time.gmtime(true_time))
    temp = float(json.dumps(parsed['main']['temp']))
    temp_kelvin = float(json.dumps(parsed['main']['temp']))
    real_feel = float(json.dumps(parsed['main']['feels_like']))
    temp_min = float(json.dumps(parsed['main']['temp_min']))
    temp_max = float(json.dumps(parsed['main']['temp_max']))
    pressure = float(json.dumps(parsed['main']['pressure']))
    humidity = float(json.dumps(parsed['main']['humidity']))
    conditions = str(json.dumps(parsed['weather'][0]['description'])).\
        replace('"', '').title()
    print(f"{'':-<100}\n"
          f'Weather Report for {city}, {country} on {current_time}:\n'
          f'Current Temperature {convert_temp(temp)}\n'
          f'Current Temperature in Kelvin {(temp_kelvin)}\n'
          f'Feels Like {convert_temp(real_feel)}\n'
          f'High Temperature {convert_temp(temp_max)}\n'
          f'Low Temperature {convert_temp(temp_min)}\n'
          f'Current Conditions: {conditions}\n'
          f'Atmospheric pressure: {pressure} hPa\n'
          f'Humidity: {humidity}%\n'
          f"{'':-<100}"
          )

"""
Extended format, decodes the JSON data, formats the time variables to match 
time to the time zones, then formats the printable output of the extended 
forecast
"""
def ext_formatted(parsed):
    print(f"{'36 Hour Forecast':30}{'Temperature':22}{'Conditions'}")
    # For loop to pull the data for every six (6) hours,
    # approximate 36 hour forecast data return
    for i in range(1, 15, 2):
        epoch_time = int(json.dumps(parsed['list'][i]['dt']))
        timezone = int(json.dumps(parsed['city']['timezone']))
        true_time = epoch_time + timezone
        future_time = time.strftime("%a, %b %d %I:%M %p", time.gmtime(true_time))
        temp = float(json.dumps(parsed['list'][i]['main']['temp']))
        conditions = str(json.dumps(parsed['list'][i]['weather'][0]
                                    ['description'])).replace('"', '').title()
        print(f'{future_time:30}{convert_temp(temp):22}{conditions}')

'''
Allows the user to look up another location or exit the program
'''
def more_weather():
    option = str(input('Would you like to enter another location, Yes or No? '
                       )).lower().strip()
    # while loop for a yes selection or to exit the program
    # (and to catch input errors)
    while not (option == 'yes' or option == 'no'):
        option = str(input('You did not enter a valid selection.\n'
                           'Please enter Yes to search another location '
                           'or No to exit: ')).lower().strip()
    if option == 'yes':
        print('')
        main()
    if option == 'no':
        print('Thank you for using Weather Now! Goodbye')

if __name__ == "__main__":
    main()
