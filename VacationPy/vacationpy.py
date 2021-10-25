# %%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import gmaps
import os
from config import g_key



# region
# natively display more info in dfs in pycharm
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
# endregion

#region
# def spaceless_lowers(dataframe):
#     """
#     Params:
#         dataframe: a dataframe with columns that have spaces and uppercase letters
#     Returns:
#         a dataframe with the spaces replaced with _ and all caps made lowercase.
#     """
#     try:
#         cols = dataframe.columns
#         cols = [col.replace(' ', '_').lower() for col in cols]
#         dataframe.columns = cols
#
#         return dataframe
#
#     except NameError:
#         print('There is an unresolved reference to the dataframe in the function\'s argument.\n'
#               'Make sure that the dataframe has been read and defined.')
#
#
# def find_cities():
#     for r, d, files in os.walk('.'):
#         for name in files:
#             if name == 'cities.csv':
#                 data = os.path.join(r, name)
#                 return data
#
#
# def k_to_f(temp):
#     temp = round((temp - 273.15) * 9 / 5 + 32, 2)
#     return temp
#
#
# def kmh_to_mph(speed):
#     return speed * 0.621371
#
#
# def north_or_south(latitude):
#     return latitude < 0
#

#%%

#%%
df = pd.read_csv(r'./WeatherPy/cities_2.csv')

df.rename(columns={'Unnamed: 0': 'city'}, inplace=True)
df.head()

#%%
gmaps.configure(g_key)

locs = df[['lat', 'long']]
humidity