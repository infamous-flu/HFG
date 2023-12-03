import json
import pandas as pd
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt

# Dataframe

spending_frame = pd.read_csv("spending.csv")
spending_frame = spending_frame[["Geographical area name","Year", "Units", "Value"]]
spending_frame = spending_frame.dropna()
constant_spending_frame = spending_frame.loc[spending_frame["Units"] == "Constant USD"]
last = spending_frame.loc[spending_frame["Year"] == 2021]
constant_spending_frame = pd.concat([constant_spending_frame, last])

constant_spending_frame ['Year'] = [int(x) for x in constant_spending_frame ['Year']]

# Plot

fig = plt.figure(figsize=[8,5])
ax = plt.subplot(111)

constant_spending_frame.plot(ax=ax, x="Year", y="Value", style="g-", legend=False)
ax.set_ylabel("Constant USD (millions)", fontsize=12)
ax.set_xlabel("Year", fontsize=12)
ax.set_title("Total official development assistance (gross disbursement) for water supply and sanitation", fontsize=12)

ax.set_xlim(2000, 2021)
ax.set_ylim(500, 3200)
ax.set_xticks(range(2000, 2021, 5))
ax.set_facecolor("black")

plt.show()