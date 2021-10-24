# %%
"""In this example, you'll be creating a Python script to visualize the weather of 500+ cities across the
world of varying distance from the equator. To accomplish this, you'll be utilizing a simple Python library, 
the OpenWeatherMap API, and a little common sense to create a representative model of weather across world cities.

The first requirement is to create a series of scatter plots to showcase the following relationships:

Temperature (F) vs. Latitude
Humidity (%) vs. Latitude
Cloudiness (%) vs. Latitude
Wind Speed (mph) vs. Latitude
After each plot, add a sentence or two explaining what the code is analyzing.

The second requirement is to run linear regression on each relationship. This time, separate the plots into Northern
Hemisphere (greater than or equal to 0 degrees latitude) and Southern Hemisphere (less than 0 degrees latitude):

Northern Hemisphere - Temperature (F) vs. Latitude
Southern Hemisphere - Temperature (F) vs. Latitude
Northern Hemisphere - Humidity (%) vs. Latitude
Southern Hemisphere - Humidity (%) vs. Latitude
Northern Hemisphere - Cloudiness (%) vs. Latitude
Southern Hemisphere - Cloudiness (%) vs. Latitude
Northern Hemisphere - Wind Speed (mph) vs. Latitude
Southern Hemisphere - Wind Speed (mph) vs. Latitude
"""

# region
# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests, json, time
from scipy.stats import linregress


def k_to_c(temp):
    return temp - 273.15


def kmh_to_mph(speed):
    return speed * 0.621371


def north_or_south(latitude):
    return latitude < 0


# %%
# Import API key
from config import weather_api_key

api_key = weather_api_key

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# endregion

# %%
# Output File (CSV)
output_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)

lats = [np.random.uniform(lat_range[0], lat_range[1]) for i in range(3000)]
lngs = [np.random.uniform(lng_range[0], lng_range[1]) for i in range(3000)]

lat_lngs = list(zip(lats, lngs))

cities = []

for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    city = city.strip()
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

len(cities)

# %%
temp_dict = {}

ol = []
i = 0

for city in cities:
    search_str = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    resp = requests.get(search_str)
    if resp.status_code == 200:
        if i < 500:
            resp = resp.json()
            vs = [
                    resp['coord']['lat'],
                    k_to_c(resp['main']['temp']),
                    resp['main']['humidity'],
                    kmh_to_mph(resp['wind']['speed']),
            ]
            i += 1
            temp_dict[city] = vs

# %%
temp_dict = {}
i = 0

for city in cities:
    if i < 500:
        search_str = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        resp = requests.get(search_str)
        if resp.status_code == 200:
            temp_k = resp.json()['main']['temp']
            temp_c = k_to_c(temp_k)
            temp_dict[city] = temp_c
            print(f'Request {i}: {city} successfully acquired.')
            i += 1
        else:
            print(f'{city} received 404.')

# %%
# search_str = f'http://api.openweathermap.org/data/2.5/weather?q={cities[0]}&appid={api_key}'
# resp = requests.get(search_str).json()  # ['main']['temp']
# print(resp)
# print(k_to_c(resp))

# %%
# i = 0
# for city in cities[:100]:
#     if i < 520:
#         if i % 2 == 0:
#             print(city)
#         i += 1
#     else:
#         break

# %%
# l = 'coord main visibility'.split()
# temp_dict = {}
#
# # for val in l:
# #     temp_dict[val] = resp[val]
#
#
# 'coord temp humidity clouds wind_speed'

# %%
# temp_dict={}
#
# ol = []
#
#
# for city in cities[0:3]:
#     search_str = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
#     resp = requests.get(search_str).json()
#
#     vs = [
#             resp['coord']['lat'],
#             k_to_c(resp['main']['temp']),
#             resp['main']['humidity'],
#             kmh_to_mph(resp['wind']['speed']),
#     ]
#
#     temp_dict[city] = vs
#
# print(temp_dict)
