import pandas as pd
import folium
from folium import Marker
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import geopy
from geopandas.tools import geocode
import geopandas
import os


# Geopy init
geopy.geocoders.options.default_user_agent = __name__

# Get path to geojson data
cwd = os.getcwd()
path_fylke = f"{cwd}/Fylke"

# Define functions
def url_list_2_df(url):
    req = requests.get(url, allow_redirects = True)
    data_list = eval(str(req.content, 'utf-8'))
    cols = data_list[0]
    
    data = pd.DataFrame(data_list[1:], columns = cols)
    return data

def geocoder(row):
    try:
        point = geocode(row, provider = 'nominatim').geometry.iloc[0]
        return pd.Series({"Latitude": point.y, "Longitude": point.x, "geometry": point})
    except:
        return None

# URL for norway map
url = (
    "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/"
)
nor_geo = f"{url}/norway.json"

# Load county borders
json_counties_list = list(os.walk(path_fylke))[0][2]
#print(json_counties_list)
json_counties = pd.DataFrame([])
json_counties = pd.concat([
    geopandas.read_file(f"{path_fylke}/{fylke}") for fylke in json_counties_list[:-1]
    ])
print(json_counties.navn)
exit()

# Vaccine info from FHI
url_FHI = "https://www.fhi.no/api/chartdata/api"

# Numbers by county
data_counties_url = f"{url_FHI}/99112"
data_counties = url_list_2_df(data_counties_url)

data_counties[["Latitude", "Longitude", "geometry"]] = data_counties.apply(lambda x: geocoder(x.Fylke), axis = 1)
#print(data_counties.head())

# Numbers by communes
# Need to decode kommunenr
data_communes_url = f"{url_FHI}/99101"
data_communes = url_list_2_df(data_communes_url)
#print(data_communes.head())

# Create the map
center_lat = 65
center_long = 18
map_w = folium.Map(location=[center_lat, center_long], tiles = 'Stamen Terrain')
folium.FitBounds([(center_lat-5, center_long-5), (center_lat+5, center_long+5)]).add_to(map_w)

# Add count to map
for idx, row in data_counties.iterrows():
    Marker([row["Latitude"], row["Longitude"]], popup=row.Fylke).add_to(map_w)

map_w.save("test.html")
