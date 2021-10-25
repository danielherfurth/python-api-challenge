# %%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import gmaps
import os
from config import g_key
from config import weather_api_key as api_key
from iso3166 import countries_by_alpha2
from citipy import citipy


# region
# natively display more info in dfs in pycharm
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
# endregion

#region
def spaceless_lowers(dataframe):
    """
    Params:
        dataframe: a dataframe with columns that have spaces and uppercase letters
    Returns:
        a dataframe with the spaces replaced with _ and all caps made lowercase.
    """
    try:
        cols = dataframe.columns
        cols = [col.replace(' ', '_').lower() for col in cols]
        dataframe.columns = cols

        return dataframe

    except NameError:
        print('There is an unresolved reference to the dataframe in the function\'s argument.\n'
              'Make sure that the dataframe has been read and defined.')


def find_cities():
    for r, d, files in os.walk('.'):
        for name in files:
            if name == 'cities.csv':
                data = os.path.join(r, name)
                return data


def k_to_f(temp):
    temp = round((temp - 273.15) * 9 / 5 + 32, 2)
    return temp


def kmh_to_mph(speed):
    return speed * 0.621371


def north_or_south(latitude):
    return latitude < 0

#endregion
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

print(len(cities))

#%%

temp_dict = {}
# {city:[lat, max_temp, humidity, windspeed, clouds]}
i, j = 0, 0

for city in cities:
    if i < 500:
        search_str = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        resp = requests.get(search_str)
        if resp.status_code == 200:
            resp = resp.json()
            vs = [
                    resp['coord']['lat'],
                    resp['coord']['lon'],
                    k_to_f(resp['main']['temp_max']),
                    resp['main']['humidity'],
                    kmh_to_mph(resp['wind']['speed']),
                    resp['clouds']['all'],
                    countries_by_alpha2[resp['sys']['country']][0],
                    resp['dt']
            ]
            temp_dict[city] = vs
            i += 1
            print(f'Request {j}: {city} request successful.')
        else:
            print(f'Request {j}: {city} request failed.')
        j += 1
    else:
        print(
                f'{i} successful requests made.\n'
                f'{round(i / j * 100, 2)}% of requests succeeded.'
        )
        break

#%%

dft = pd.DataFrame(temp_dict).T
dft.columns = ['Latitude', 'Max Temperature (F)', 'Humidity (%)', 'Wind Speed (mph)', 'Clouds (%)']
dft['is_south'] = dft['Latitude'].apply(lambda x: 1 if x < 0 else 0)
dft.head()

#%%
search_str = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
resp = requests.get(search_str)
resp.json()