# this script was used to make and troubleshoot the ipynb
# ipynb made with p2j

# # region
# # Dependencies and Setup
# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# import requests, json, time
# from scipy.stats import linregress
# from citipy import citipy  # Incorporated citipy to determine city based on latitude and longitude
# # Import API key
# from config import weather_api_key
# from iso3166 import countries_by_alpha2
#
#
# def k_to_c(temp):
#     return temp - 273.15
#
#
# def kmh_to_mph(speed):
#     return speed * 0.621371
#
#
# def north_or_south(latitude):
#     return latitude < 0
#
#
# api_key = weather_api_key
# # endregion
#
# # Output File (CSV)
# output_file = "output_data/cities.csv"
#
# # Range of latitudes and longitudes
# lat_range = (-90, 90)
# lng_range = (-180, 180)
#
# lats = [np.random.uniform(lat_range[0], lat_range[1]) for i in range(3000)]
# lngs = [np.random.uniform(lng_range[0], lng_range[1]) for i in range(3000)]
#
# lat_lngs = list(zip(lats, lngs))
#
# cities = []
#
# for lat_lng in lat_lngs:
#     city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
#     city = city.strip()
#     # If the city is unique, then add it to a our cities list
#     if city not in cities:
#         cities.append(city)
#
# len(cities)
#
# temp_dict = {}
#
# ol = []
# i, j = 0, 0
#
# for city in cities:
#     if i < 500:
#         search_str = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
#         resp = requests.get(search_str)
#
#         if resp.status_code == 200:
#             resp = resp.json()
#             vs = [
#                     resp['coord'],
#                     k_to_c(resp['main']['temp']),
#                     resp['main']['humidity'],
#                     kmh_to_mph(resp['wind']['speed']),
#                     # resp['sys']['country'],
#                     countries_by_alpha2[resp['sys']['country']][0]
#             ]
#             i += 1
#             temp_dict[city] = vs
#             print(f'Request {j}: {city} request successful.')
#         else:
#             print(f'Request {j}: {city} request failed.')
#         j += 1
#     else:
#         print(
#                 '500 successful requests made.'
#                 f'{round(i/j*100, 2)}% of requests succeeded.'
#         )
#         break
