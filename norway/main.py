import pandas as pd
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import requests
#from urllib.request import Request, urlopen

# URL for norway map
url = (
    "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/"
)
nor_geo = f"{url}/norway.json"
#data = pd.read_csv(nor_geo)
#print(data.head())

# Vaccine info from FHI
url_FHI = "https://www.fhi.no/api/chartdata/api"
data_url = f"{url_FHI}/99112"
req = requests.get(data_url, allow_redirects = True)
print(data_url)

#page = urlopen(req).read()
print(str(req.content, 'utf-8'))
data = pd.DataFrame(str(req.content, 'utf-8'))
print(data.head())

# Create the map
center_lat = 65
center_long = 18
map_w = folium.Map(location=[center_lat, center_long], tiles = 'Stamen Terrain')
folium.FitBounds([(center_lat-5, center_long-5), (center_lat+5, center_long+5)]).add_to(map_w)

map_w.save("test.html")
