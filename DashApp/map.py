from urllib.request import urlopen
import json

import pandas as pd
import geopandas as gpd
import plotly.express as px

proportion_safe_water = pd.read_csv("access_to_improved_water_source.csv")
proportion_safe_water = proportion_safe_water[["Geographical area name", "Year", "Value"]]
print(proportion_safe_water.head())
proportion_safe_water = proportion_safe_water.rename(columns={"Geographical area name":"ADMIN"})

proportion_safe_water = proportion_safe_water.loc[proportion_safe_water["Year"] > 2000]

world = gpd.read_file("countries.geojson")
africa = pd.read_csv("african_countries.csv")
joined = pd.merge(world, africa, on="ADMIN", how="inner")
joined = pd.merge(joined, proportion_safe_water, on="ADMIN", how="inner")
joined['id'] = [int(x) for x in joined['id']]
joined = joined.sort_values(by=["id"])

print(joined.head())

fig = px.choropleth_mapbox(joined, geojson=world, locations='ADMIN', color='Value',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()