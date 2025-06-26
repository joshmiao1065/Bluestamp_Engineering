import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load the data
df = pd.read_csv("Terrestrial_Marine protected areas.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Rename columns for clarity
df = df.rename(columns={
    "Country and area": "Country",
    "latest year available": "Year",
    "Terrestrial and marine protected areas (% of total territorial area)": "ProtectedAreaPct"
})

# Clean data
df = df[df["ProtectedAreaPct"].apply(lambda x: str(x).strip()).ne("")]
df["ProtectedAreaPct"] = df["ProtectedAreaPct"].astype(float)

# Initialize Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Global Biodiversity Protection Map"),
    dcc.Graph(id="world-map", style={"height": "700px"}),
    html.Div(id="country-info", style={"padding": "20px", "fontSize": "18px"})
])

# Callback for updating map and displaying info
@app.callback(
    Output("world-map", "figure"),
    Output("country-info", "children"),
    Input("world-map", "clickData")
)
def update_map(click_data):
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="ProtectedAreaPct",
        hover_name="Country",
        color_continuous_scale="Viridis",
        title="Protected Terrestrial & Marine Areas (% of Territory)",
        range_color=(0, 60)
    )
    fig.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations")
    
    # Click information
    if click_data:
        country_clicked = click_data["points"][0]["location"]
        info_row = df[df["Country"] == country_clicked]
        if not info_row.empty:
            row = info_row.iloc[0]
            info = f"""
            Country: {row['Country']} \t   
            Year: {row['Year']}\t  
            Protected Area: {row['ProtectedAreaPct']}%
            """
        else:
            info = f"No data available for {country_clicked}."
    else:
        info = "Click on a country to see detailed biodiversity data."

    return fig, info

# Run app
if __name__ == "__main__":
    app.run(debug=True)
