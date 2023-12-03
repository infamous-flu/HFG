import json
import pandas as pd
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt

jobs = pd.read_csv("job_numbers.csv")
jobs['ISO_A2'] = [x.upper() for x in jobs['ISO_A2']]
# proportion_safe_water = proportion_safe_water[["Geographical area name", "Year", "Value"]]
# print(proportion_safe_water.head())
# proportion_safe_water = proportion_safe_water.rename(columns={"Geographical area name":"ADMIN"})
# 
# proportion_safe_water = proportion_safe_water.loc[proportion_safe_water["Year"] == 2022]
# 
# 
world = gpd.read_file("countries.geojson")
africa = pd.read_csv("african_countries.csv")

fig, ax = plt.subplots(figsize=(10, 10))
joined = pd.merge(world, africa, on="ADMIN", how="inner")
joined.plot(ax=ax, color="grey", edgecolor="white")
joined = pd.merge(joined, jobs, on="ISO_A2", how="inner")
joined['id'] = [int(x) for x in joined['id']]
joined = joined.sort_values(by=["id"])
# 
print(joined)
# 
joined.plot(ax=ax, column='number', cmap='RdYlGn', edgecolor="white", legend=True)
ax.set_facecolor("black")
ax.set_title("Number of Water Related Jobs in Each Country")
plt.show()