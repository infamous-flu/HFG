import json
import pandas as pd
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt

proportion_safe_water = pd.read_csv("access_to_improved_water_source.csv")
proportion_safe_water = proportion_safe_water[["Geographical area name", "Year", "Value"]]
print(proportion_safe_water.head())
proportion_safe_water = proportion_safe_water.rename(columns={"Geographical area name":"ADMIN"})

proportion_safe_water = proportion_safe_water.loc[proportion_safe_water["Year"] > 2000]


world = gpd.read_file("countries.geojson")
africa = pd.read_csv("african_countries.csv")

fig, ax = plt.subplots(figsize=(10, 10))
joined = pd.merge(world, africa, on="ADMIN", how="inner")
joined.plot(ax=ax, color="grey")
joined = pd.merge(joined, proportion_safe_water, on="ADMIN", how="inner")
joined['id'] = [int(x) for x in joined['id']]
joined = joined.sort_values(by=["id"])

#print(joined)

joined.plot(ax=ax, column='Value', cmap='Greens', edgecolor="white", legend=True)
ax.set_facecolor("black")
ax.set_title("Access to Improved Water Source (% of Population)")
plt.show()