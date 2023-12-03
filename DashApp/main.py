import pandas as pd
import geopandas as gpd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

app = Dash(__name__)

# -- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")
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

# df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
# df.reset_index(inplace=True)
# print(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2022", "value": 2022},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018}],
                 multi=False,
                 value=2022,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = joined.copy()
    dff = dff[dff["Year"] == option_slctd]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        scope="asia",
        color='Value',
        hover_data=['ADMIN', 'Value'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)