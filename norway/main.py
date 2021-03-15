import pandas as pd
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from geopandas.tools import geocode

# Define functions
def url_list_2_df(url):
    req = requests.get(url, allow_redirects = True)
    data_list = eval(str(req.content, 'utf-8'))
    cols = data_list[0]
    
    data = pd.DataFrame(data_list[1:], columns = cols)
    data.index = data.iloc[:,0]
    data = data.drop(cols[0], axis = 1)
    return data
    
# URL for norway map
url = (
    "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/"
)
nor_geo = f"{url}/norway.json"

# Vaccine info from FHI
url_FHI = "https://www.fhi.no/api/chartdata/api"

# Numbers by county
data_counties_url = f"{url_FHI}/99112"
data_counties = url_list_2_df(data_counties_url)
#print(data_counties)

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



map_w.save("test.html")
