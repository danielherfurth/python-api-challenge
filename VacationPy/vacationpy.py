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

df = pd.read_csv(r'./WeatherPy/cities_2.csv')

df.rename(columns={'Unnamed: 0': 'city'}, inplace=True)
df.head()

gmaps.configure(g_key)

locs = df[['lat', 'long']]
humidity = df.humidity

fig_layout = {
        'width':'1200px',
        'height':'600px',
        'border':'2px solid black',
        'padding':'2px',
        'margin':'0 auto 0 auto'
}

fig = gmaps.figure(layout=fig_layout)

heatmap = gmaps.heatmap_layer(
        locs,
        weights=humidity,
        max_intensity=df.humidity.max(),
        dissipating=False,
        point_radius=5
)

fig.add_layer(heatmap)


# select decent weather
temp_mask = df['max_temp'].between(70, 90)
humid_mask = df['humidity'].between(50, 90)
cloud_mask = df['clouds'] < 8

# mask based on conditions
masked_df = df[temp_mask & humid_mask & cloud_mask]

# print(len(masked_df))
# check for nulls
masked_df.isna().sum()
len(masked_df)

# find hotels within 5e3 m of my locations
hotels = []

for i in masked_df['city']:
    lat = masked_df['lat']
    long = masked_df['long']
    coords = list(zip(lat.astype(str), long.astype(str)))
    coords = [', '.join(coord) for coord in coords]

    param_dict = {
            'location': coords,
            'radius': 5000,
            'type': 'lodging',
            'key': g_key
    }

    url_base = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

    try:
        resp = requests.get(url_base, param_dict).json()
        outputs = resp['results'][0]['name']
        hotels.append(outputs)
    except:
        hotels.append(np.nan)
        print(f'Unable to find {i}.')


hotel_names = [outputs[i]['name'] for i in range(len(masked_df.city))]
print(len(hotel_names) == len(masked_df.city))
masked_df['hotel'] = hotel_names

masked_df.reset_index(drop=True)

# Using the template add the hotel marks to the heatmap
info_box_template = """
<dl>
<dt>Name</dt><dd>{hotel}</dd>
<dt>City</dt><dd>{city}</dd>
<dt>Country</dt><dd>{country}</dd>
</dl>
"""
# Store the DataFrame Row
# NOTE: be sure to update with your DataFrame name
hotel_info = [info_box_template.format(**row) for index, row in masked_df.iterrows()]
locations = masked_df[["lat", "long"]]

markers = gmaps.marker_layer(locations, info_box_content=hotel_info)
fig.add_layer(markers)
