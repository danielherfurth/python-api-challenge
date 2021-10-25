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
        # max_intensity=
        dissipating=False,
        point_radius=5
)

fig.add_layer(heatmap)

#%%
# select decent weather

temp_mask = df['max_temp'].between(60, 90)
humid_mask = df['humidity'].between(50, 90)
cloud_mask = df['clouds'] < 10

# mask based on conditions
masked_df = df[temp_mask & humid_mask & cloud_mask]

# check for nulls
masked_df.isna().sum()

#%%
# find hotels within 5e3 m of my locations

hotels=[]



for c in masked_df:
    lat, long = masked_df['lat'], masked_df['long']
    coords = list(zip(lat.astype(str), long.astype(str)))
    coords = [', '.join(coord) for coord in coords]
    param_dict = {
            'location': coords,
            'radius': 5000,
            'type': 'lodging',
            'key': g_key
    }
    url_base = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

    resp = requests.get(url_base, param_dict).json()
    print(resp)

#%%
resp = {'html_attributions': [], 'next_page_token': 'Aap_uEDYOso7Qrh3L7kWYmLJ6QFvqN3-zw8JDXOysFoJoxfrXT9Hjc1Pq1TjRv5OVr33NhRh1ZFpd_LPUOirVh4NAcq5Ua52y030hH8BcAAxW3mBAOgRYr2slT7TkNxayvhGyi7phQmtttm4woBhotBbnNNGm88YHnFfPD396ymDJed7aJF93MlKYu1bLD-sSVBPSgZHVGeMXfYBQ20OchlVUWb6kNbL5rjn6SHJat6Zj-DG8Z7VyybHr89BiCkRhg63m8vyw3WeOs6SrRAKCS946mlqAMOvis5iyt0LtLCPEDOAbLK45fTvIsOMlAu4eRrHw1-86rNda6rKcnrbeq7wVPc6d_-ATgMeM8VRaea5KUg4C0evOcvMXk2kYRWEahZ7rxsuxSsi7RXZFAOXSGgepBR6_cATLQEOPpT3GVT4jGUCg6Hl_6oZAWwM', 'results': [{'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.6315101, 'lng': 69.60906349999999}, 'viewport': {'northeast': {'lat': 21.6328904302915, 'lng': 69.6104694302915}, 'southwest': {'lat': 21.6301924697085, 'lng': 69.60777146970848}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'Lords Inn Porbandar', 'opening_hours': {'open_now': True}, 'photos': [{'height': 4613, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/101678568484381488362">Lords Inn Porbandar</a>'], 'photo_reference': 'Aap_uEBVc0RO_CNsrePTebx2k_KGiZJTS2BTvO7qxHpNRXZk3csC1Vj42CSV5DDrEod7Jp6QbOukYDHkI_vSfZg3kB173NOIsiURV2CnpJJ8KorDBCIhyx0IVggQe1YdK7j4IIbv4riyRLJldgPozetBlQ_sLyY7kx37Vf81R48sKPq5-BGj', 'width': 6912}], 'place_id': 'ChIJbyk_zkI0VjkRoPjmK6QVSek', 'plus_code': {'compound_code': 'JJJ5+JJ Porbandar, Gujarat, India', 'global_code': '7JHFJJJ5+JJ'}, 'rating': 4.1, 'reference': 'ChIJbyk_zkI0VjkRoPjmK6QVSek', 'scope': 'GOOGLE', 'types': ['lodging', 'restaurant', 'food', 'point_of_interest', 'establishment'], 'user_ratings_total': 2492, 'vicinity': 'near Circuit House, Chopati Road, GEB Colony, Porbandar'}, {'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.6388424, 'lng': 69.6066767}, 'viewport': {'northeast': {'lat': 21.6402440802915, 'lng': 69.60804023029151}, 'southwest': {'lat': 21.6375461197085, 'lng': 69.60534226970849}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'Hotel Kuber', 'photos': [{'height': 3840, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/110313216263554635074">Hotel Kuber</a>'], 'photo_reference': 'Aap_uEA_jgE2auQ5RuSoSxWpHQ57y6Eopmv7Qpf7qE6X_kScrMavtzaPqAVYTk1tfj2xwDG0mNl3exYOrr05poCy0FfGk1tNUsM4ngtb92dImdqDTiS-TWKUrcyL1dqck6cwB763tceBY_BbofxhoFjaXfvGa5MKRydAwuR_RX691k-2l4xX', 'width': 5760}], 'place_id': 'ChIJx7EdC0U0VjkRevfYkrTKi_k', 'plus_code': {'compound_code': 'JJQ4+GM Porbandar, Gujarat, India', 'global_code': '7JHFJJQ4+GM'}, 'rating': 4, 'reference': 'ChIJx7EdC0U0VjkRevfYkrTKi_k', 'scope': 'GOOGLE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 323, 'vicinity': 'near Swami Narayan Temple, ST Road, near Swami Narayan Temple, Porbandar'}, {'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.6391366, 'lng': 69.6068574}, 'viewport': {'northeast': {'lat': 21.6404820302915, 'lng': 69.60822688029151}, 'southwest': {'lat': 21.6377840697085, 'lng': 69.6055289197085}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'CAPITAL O72082 Hotel Indraprasth', 'photos': [{'height': 3456, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/103984191922463380972">Niraj Vadoliya</a>'], 'photo_reference': 'Aap_uECxqrYMz4jBVFimtoZNbuPj1NtFIkOfABpy7jC4HFDDcbMTowpPp0ktX9FcyPdmQyplz_9B75dyZo6s3hO27oC48WrYqFMNKuww466PBsgZzX-774SMUt_oawq10-7BE-fyH1PojkIPPJKpVk4X6wot-3DguyxRHQbYPnYvw_LqR9x_', 'width': 4608}], 'place_id': 'ChIJTbaLdEU0VjkRMrOmXbRPrB0', 'plus_code': {'compound_code': 'JJQ4+MP Porbandar, Gujarat, India', 'global_code': '7JHFJJQ4+MP'}, 'rating': 3.8, 'reference': 'ChIJTbaLdEU0VjkRMrOmXbRPrB0', 'scope': 'GOOGLE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 150, 'vicinity': 'Rani Baug, Panch Hatdi, Porbandar'}, {'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.6381752, 'lng': 69.6051877}, 'viewport': {'northeast': {'lat': 21.6395151302915, 'lng': 69.6065753302915}, 'southwest': {'lat': 21.63681716970849, 'lng': 69.6038773697085}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'Hotel Sheetal', 'opening_hours': {'open_now': True}, 'photos': [{'height': 427, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/113260772095632392463">Hotel Sheetal</a>'], 'photo_reference': 'Aap_uEAy8HlEObKnzcST1cJAk5CVckxuhlKQOeMdz_W_josIIBr83CK5fwo1OuJke_ZO9tg4QV7u69cLYA8AEIHHkHiznMT2sp_4VZF-ilDPojwNqN1hNE9SwAxy4FT5uorEvDNXD8xzEyce6G4uAljOWRxh56My65clN1glxKLPXHTAqqm9', 'width': 640}], 'place_id': 'ChIJq6qqqls0VjkR3MUbQGKPBkk', 'plus_code': {'compound_code': 'JJQ4+73 Porbandar, Gujarat, India', 'global_code': '7JHFJJQ4+73'}, 'rating': 3.6, 'reference': 'ChIJq6qqqls0VjkR3MUbQGKPBkk', 'scope': 'GOOGLE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 400, 'vicinity': 'near Arya samaj, Opposite Head Post Office, near Arya samaj, Porbandar'}, {'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.6417954, 'lng': 69.60633100000001}, 'viewport': {'northeast': {'lat': 21.6431491302915, 'lng': 69.6076622802915}, 'southwest': {'lat': 21.6404511697085, 'lng': 69.6049643197085}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'Hotel President', 'opening_hours': {'open_now': False}, 'photos': [{'height': 3024, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/109302773419903907356">Dipesh Shah</a>'], 'photo_reference': 'Aap_uEBqYNbYgT7ompZHtc3AquFngENqnxjkkYu4OJ6SQN9CiNI_zrfKHbKyR6GnO_C6PAv8JFv1kAFiEihh8huK79U9W4jFM--8qdjVYLfujpvOi3gwGg2y1WFUPFNp1jOdpbTHyIDNZIgsUpFny5tweJWo9vzmz_4sadJEloetbnu3g7tZ', 'width': 4032}], 'place_id': 'ChIJt01i6_A0VjkR-SBZfKZJj3k', 'plus_code': {'compound_code': 'JJR4+PG Porbandar, Gujarat, India', 'global_code': '7JHFJJR4+PG'}, 'rating': 3.7, 'reference': 'ChIJt01i6_A0VjkR-SBZfKZJj3k', 'scope': 'GOOGLE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 120, 'vicinity': 'Prabhu Complex, opposite Porbandar'}, {'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.6404954, 'lng': 69.60747830000001}, 'viewport': {'northeast': {'lat': 21.6418520302915, 'lng': 69.60879503029152}, 'southwest': {'lat': 21.63915406970849, 'lng': 69.60609706970851}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'Hotel Atithi', 'opening_hours': {'open_now': True}, 'photos': [{'height': 2250, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/113385723011407742959">Ravin Patel</a>'], 'photo_reference': 'Aap_uEAXWH8gqcW2QVGpvpVETOEDG4Jfc2Aub9ENd_VG0cPxtb-z1Cj1zMOhgLHpQwbidGJpkGMqcDC7Zlf0p22DJO3PnuoCXy5_edyTmGreDCwW_UgG45sCuHAnw5DUgMCemsrmj-Nr-CWXsx_iP9Fveplh6ui2LZLLhIpVD-a403XP4lpA', 'width': 4000}], 'place_id': 'ChIJG3r6YkU0VjkRYbGD27cbvJ0', 'plus_code': {'compound_code': 'JJR4+5X Porbandar, Gujarat, India', 'global_code': '7JHFJJR4+5X'}, 'rating': 4.4, 'reference': 'ChIJG3r6YkU0VjkRYbGD27cbvJ0', 'scope': 'GOOGLE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 140, 'vicinity': 'Panch Hatdi, Porbandar'}, {'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.6397325, 'lng': 69.607304}, 'viewport': {'northeast': {'lat': 21.6410815302915, 'lng': 69.6086512802915}, 'southwest': {'lat': 21.63838356970849, 'lng': 69.60595331970849}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'Cctv zone & Computer', 'opening_hours': {'open_now': False}, 'photos': [{'height': 1324, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/108177603746732515129">Cctv zone &amp; Computer</a>'], 'photo_reference': 'Aap_uEAz1nkv7Pgsq4DjSGiIZK4zl8JIY07jj42KtdUG_xH0ui2NrXVemYdqqevhTOru_fWosnaYs4lbd4muq7scyM2ImSmrumNwWoCVyiY2o0RkbeuXDlHDl1wAv3_OzKfuPW2raSK_vpLAXJEY02QjN46vX73ucjtORkwGYdibxNKWWuUc', 'width': 1093}], 'place_id': 'ChIJyS9TfEU0VjkR4eLc8FIInxk', 'plus_code': {'compound_code': 'JJQ4+VW Porbandar, Gujarat, India', 'global_code': '7JHFJJQ4+VW'}, 'rating': 3.6, 'reference': 'ChIJyS9TfEU0VjkR4eLc8FIInxk', 'scope': 'GOOGLE', 'types': ['lodging', 'electronics_store', 'point_of_interest', 'store', 'establishment'], 'user_ratings_total': 43, 'vicinity': 'Hotel silver palace ground floor S t, road, Porbandar'}, {'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.642611, 'lng': 69.605375}, 'viewport': {'northeast': {'lat': 21.6439496302915, 'lng': 69.6067586302915}, 'southwest': {'lat': 21.6412516697085, 'lng': 69.60406066970849}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'OYO 4470 Hotel Azura', 'opening_hours': {'open_now': True}, 'place_id': 'ChIJ1SFCGU80VjkRdW9nDy9CCSc', 'plus_code': {'compound_code': 'JJV4+24 Porbandar, Gujarat, India', 'global_code': '7JHFJJV4+24'}, 'rating': 4.2, 'reference': 'ChIJ1SFCGU80VjkRdW9nDy9CCSc', 'scope': 'GOOGLE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 10, 'vicinity': 'Sudama Road Near Harish Talkies'}, {'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.6426181, 'lng': 69.60532169999999}, 'viewport': {'northeast': {'lat': 21.6439486302915, 'lng': 69.6067303802915}, 'southwest': {'lat': 21.6412506697085, 'lng': 69.60403241970849}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'Hotel Azura', 'opening_hours': {'open_now': True}, 'photos': [{'height': 2592, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/113835359468700501939">Hotel Azura</a>'], 'photo_reference': 'Aap_uEAng7kLFPXOTQdUraInVhVxubi74BzCObz9BBgxIYS1BJtas6Bx2xYAWWeBS74S45OJmItaqh6tCn-0CyK2-00CtchAXr43FngjPYKE0W5DaQHzAE6zjPhsMKy3soGGDMgbpmYnoyqr4r9QE8hXh-NNvTLknZ3WzBKcA0MOObpsdTNw', 'width': 3888}], 'place_id': 'ChIJ4fVpGU80VjkRMngtx3EG-js', 'plus_code': {'compound_code': 'JJV4+24 Porbandar, Gujarat, India', 'global_code': '7JHFJJV4+24'}, 'rating': 4.1, 'reference': 'ChIJ4fVpGU80VjkRMngtx3EG-js', 'scope': 'GOOGLE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 308, 'vicinity': 'Sudama Puri, Bhatia Bazar Old, Porbandar'}, {'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.6297793, 'lng': 69.6134122}, 'viewport': {'northeast': {'lat': 21.6311282802915, 'lng': 69.61476118029151}, 'southwest': {'lat': 21.6284303197085, 'lng': 69.61206321970849}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'Hotel Toran Tourist Bungalow, Porbandar', 'photos': [{'height': 3120, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/118248978531431183395">OJAS MODI</a>'], 'photo_reference': 'Aap_uED2phYvueoSPBir98v82YNn4vU-XRty3orZ--POHLlVkiWqR0_0t99TA7TZX49uXWWCFyp6KR__AdBDVNs8zDlTJ593TqONPPVuosnduxQyOK7hacqjpiv9yN8TiPQzk5E02OrLJMo3Tp-xzANK6mMh4QXtDV0vfv4TJngw3DquDVbt', 'width': 4160}], 'place_id': 'ChIJyQoyR0M0VjkRDLum72H8vGg', 'plus_code': {'compound_code': 'JJH7+W9 Porbandar, Gujarat, India', 'global_code': '7JHFJJH7+W9'}, 'rating': 4.2, 'reference': 'ChIJyQoyR0M0VjkRDLum72H8vGg', 'scope': 'GOOGLE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 315, 'vicinity': 'Uttara Road, GEB Colony, Porbandar'}, {'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.6407889, 'lng': 69.62677049999999}, 'viewport': {'northeast': {'lat': 21.6420632802915, 'lng': 69.6281854302915}, 'southwest': {'lat': 21.6393653197085, 'lng': 69.62548746970849}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'Hotel Kaveri International', 'photos': [{'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111172240548984110088">Kishan Thanki</a>'], 'photo_reference': 'Aap_uED8LR9a9DTySngPEMRJI21b9VO62pBTIzpZH0zSPShVatHOiweL2jbrYNnw7is7kE4dsOhDsEoU2ka8pdFoRUuP_LIRS7srj6qPL49O9QVELn07KWGYIN57cDZ5GtY9c1F6QG0bVL16l7mZUDLmkWkU-5bRuSA_JxMTzIO9tA_YAqQs', 'width': 1280}], 'place_id': 'ChIJRbKgwFA0VjkRS9smuo6Udn8', 'plus_code': {'compound_code': 'JJRG+8P Porbandar, Gujarat, India', 'global_code': '7JHFJJRG+8P'}, 'rating': 4, 'reference': 'ChIJRbKgwFA0VjkRS9smuo6Udn8', 'scope': 'GOOGLE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 496, 'vicinity': 'India'}, {'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.6394303, 'lng': 69.6120521}, 'viewport': {'northeast': {'lat': 21.6407792802915, 'lng': 69.61340108029151}, 'southwest': {'lat': 21.63808131970849, 'lng': 69.6107031197085}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'Hotel Anand', 'place_id': 'ChIJ1w6i81o0VjkRGEc4gvEuE84', 'plus_code': {'compound_code': 'JJQ6+QR Porbandar, Gujarat, India', 'global_code': '7JHFJJQ6+QR'}, 'rating': 4.5, 'reference': 'ChIJ1w6i81o0VjkRGEc4gvEuE84', 'scope': 'GOOGLE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 2, 'vicinity': 'near khakh chowk, MG Road, near khakh chowk, Porbandar'}, {'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.6406774, 'lng': 69.6068682}, 'viewport': {'northeast': {'lat': 21.6419296302915, 'lng': 69.6081904302915}, 'southwest': {'lat': 21.6392316697085, 'lng': 69.6054924697085}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'Hotel Moon Palace', 'photos': [{'height': 1080, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/112355199387065500075">Hitesh Odedara</a>'], 'photo_reference': 'Aap_uEBJB1eaBGsTIxMH5pJL_frvgioQQPe9-EksQZHrG24HDKbhCs-ocQydE3P8TL5GxvWNTL9MLQHjcE4V8XBbVImSJ7X80mn230FTUa4_ETdjm2q7QKLoyaQ3QSjUuYQKtBTsDioAaXoHwc29sQIrGbGJLUPtJAuU2Sw16ra5Pc5RHYDD', 'width': 1920}], 'place_id': 'ChIJVQO-hk80VjkRNC8CjSjryos', 'plus_code': {'compound_code': 'JJR4+7P Porbandar, Gujarat, India', 'global_code': '7JHFJJR4+7P'}, 'rating': 4, 'reference': 'ChIJVQO-hk80VjkRNC8CjSjryos', 'scope': 'GOOGLE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 645, 'vicinity': 'M. G. Road, MG Road, Porbandar'}, {'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.639009, 'lng': 69.61292159999999}, 'viewport': {'northeast': {'lat': 21.6403108302915, 'lng': 69.6141671302915}, 'southwest': {'lat': 21.63761286970849, 'lng': 69.6114691697085}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'Hotel Harmony', 'photos': [{'height': 794, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/114525923798855627329">Milan Soni</a>'], 'photo_reference': 'Aap_uEDkZYesoa96UoYrLgP4UkgpjhO_YUGSeqyNOJGy4LMcwpwIDcn9XYmM-RnHI63SwACviu5UW5XhLRJOOZ73gKRc_athvZtblFOXpwlCMKcPEERA9DTiiNxWVLesOHtlvZVeLIBiY6H1XljqlISIVZ2hNOtVdwn6YqyOFGKl6z3sqHy-', 'width': 1080}], 'place_id': 'ChIJ6Vn_WVo0VjkRpG0idvlyUMM', 'plus_code': {'compound_code': 'JJQ7+J5 Porbandar, Gujarat, India', 'global_code': '7JHFJJQ7+J5'}, 'rating': 4.2, 'reference': 'ChIJ6Vn_WVo0VjkRpG0idvlyUMM', 'scope': 'GOOGLE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 511, 'vicinity': 'near ICICI Bank, Old Fuwara, M. G. Road, near ICICI Bank, Porbandar'}, {'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.642255, 'lng': 69.609313}, 'viewport': {'northeast': {'lat': 21.6436356302915, 'lng': 69.6106646802915}, 'southwest': {'lat': 21.6409376697085, 'lng': 69.60796671970849}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'Sanyasi Ashram', 'place_id': 'ChIJz5dP3k80VjkRIAX7l_rDK0I', 'plus_code': {'compound_code': 'JJR5+WP Porbandar, Gujarat, India', 'global_code': '7JHFJJR5+WP'}, 'rating': 5, 'reference': 'ChIJz5dP3k80VjkRIAX7l_rDK0I', 'scope': 'GOOGLE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 4, 'vicinity': 'Sardar Vallabh Patel Road, near Sanyasi Ashram, Panch Hatdi, Porbandar'}, {'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.64285439999999, 'lng': 69.6078417}, 'viewport': {'northeast': {'lat': 21.6441798302915, 'lng': 69.6092822302915}, 'southwest': {'lat': 21.6414818697085, 'lng': 69.60658426970849}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'Narashih meghaji hostel', 'place_id': 'ChIJrdhcov01VjkRgFcJL1Qo9D4', 'plus_code': {'compound_code': 'JJV5+44 Porbandar, Gujarat, India', 'global_code': '7JHFJJV5+44'}, 'reference': 'ChIJrdhcov01VjkRgFcJL1Qo9D4', 'scope': 'GOOGLE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'vicinity': '311-3-1, Kadia Plot, Area, Porbandar'}, {'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.6413022, 'lng': 69.60767109999999}, 'viewport': {'northeast': {'lat': 21.64265423029151, 'lng': 69.6089971302915}, 'southwest': {'lat': 21.6399562697085, 'lng': 69.60629916970849}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'Kuber Corner', 'place_id': 'ChIJV8GKkU80VjkRD6fv1E1zf6w', 'plus_code': {'compound_code': 'JJR5+G3 Porbandar, Gujarat, India', 'global_code': '7JHFJJR5+G3'}, 'rating': 3.4, 'reference': 'ChIJV8GKkU80VjkRD6fv1E1zf6w', 'scope': 'GOOGLE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 11, 'vicinity': 'kuber corner khakh chowk, Porbandar'}, {'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.6407074, 'lng': 69.60784199999999}, 'viewport': {'northeast': {'lat': 21.6420528802915, 'lng': 69.60921003029151}, 'southwest': {'lat': 21.6393549197085, 'lng': 69.60651206970849}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'Hotel maansarovar', 'place_id': 'ChIJvecuwdk1VjkR_MptxlLVY7s', 'plus_code': {'compound_code': 'JJR5+74 Porbandar, Gujarat, India', 'global_code': '7JHFJJR5+74'}, 'rating': 4, 'reference': 'ChIJvecuwdk1VjkR_MptxlLVY7s', 'scope': 'GOOGLE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 1, 'vicinity': 'Unnamed Road, Panch Hatdi, Porbandar'}, {'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.6414677, 'lng': 69.6072594}, 'viewport': {'northeast': {'lat': 21.6428293302915, 'lng': 69.6085575802915}, 'southwest': {'lat': 21.6401313697085, 'lng': 69.6058596197085}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'Sandeep bhai', 'opening_hours': {'open_now': True}, 'photos': [{'height': 4160, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/100490909011995988202">sandeep kumar Rajput</a>'], 'photo_reference': 'Aap_uEAE4IAu3Mm-Q5grpWIFZ8g8i5YXCo4-h_uq8-eSoD2XDwdsvlzVIBhHkIsuu-D1K-8wmtkA8cowBJO9Brfnko1ZPZg6y5fmdgm6O4MeufyrWS7RhvX5LbdQvmXhRKPAwHRc0ycsFk7tMaSSDCbrOFNfD0w9br3Ot6Or6zrYfqZ9XPXU', 'width': 2340}], 'place_id': 'ChIJ7RzUvl01VjkR9Irmn-ginbI', 'reference': 'ChIJ7RzUvl01VjkR9Irmn-ginbI', 'scope': 'GOOGLE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'vicinity': 'JJR4+HWJ, Panch Hatdi, Porbandar'}, {'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 21.6411715, 'lng': 69.60723449999999}, 'viewport': {'northeast': {'lat': 21.6424669802915, 'lng': 69.60856943029151}, 'southwest': {'lat': 21.6397690197085, 'lng': 69.60587146970849}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png', 'icon_background_color': '#909CE1', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet', 'name': 'Hotel Sudama', 'opening_hours': {'open_now': True}, 'photos': [{'height': 4160, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/118386533729947853670">HITEN PATEL</a>'], 'photo_reference': 'Aap_uEDXN0HZvHOEXvGsHQvXnm4A1-oepGg5wDnsigjJi5Ux5r1CIjN0QHvfb_8OElKH0dK8qknxED2_CyULHK_Df8j2t1V7mzFirjN_IjpvixR08DWbknZdzriCNnMq53ymMyBylhYhoR-bkNhhBdkyvQY1zHTK0g8D4MY5YS5Djylj9mcl', 'width': 2340}], 'place_id': 'ChIJpbNRFeM1VjkRxXMv04B9DC4', 'plus_code': {'compound_code': 'JJR4+FV Porbandar, Gujarat, India', 'global_code': '7JHFJJR4+FV'}, 'rating': 5, 'reference': 'ChIJpbNRFeM1VjkRxXMv04B9DC4', 'scope': 'GOOGLE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 3, 'vicinity': 'near sudama mandir, Opp. Talpad school, near sudama mandir, Porbandar'}], 'status': 'OK'}
resp