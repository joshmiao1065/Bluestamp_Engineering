# Import the 'pandas' library and give it the nickname 'pd' for easier use later.
# Pandas helps us work with data tables (like Excel sheets in code form).
import pandas as pd

# Import the 'plotly.express' library and call it 'px'.
# Plotly Express helps us create interactive graphs and maps.
import plotly.express as px

# Import specific tools from the 'dash' library:
# - 'Dash': The main framework to build the web app.
# - 'dcc' (Dash Core Components): Adds interactive elements like graphs.
# - 'html': Lets us write HTML (the language of web pages) in Python.
# - 'Input' & 'Output': Connects user actions (like clicks) to updates on the screen.
from dash import Dash, dcc, html, Input, Output


# --- DATA LOADING AND CLEANING ---

# Read a CSV file (a spreadsheet-like file) named "Terrestrial_Marine protected areas.csv" into a variable called 'df' (short for DataFrame, which is like a table in Python).
df = pd.read_csv("Terrestrial_Marine protected areas.csv")

# Clean up column names by removing extra spaces at the start or end.
# Example: "  Country " becomes "Country".
df.columns = df.columns.str.strip()

# Rename columns to make them shorter and easier to work with:
# - "Country and area" → "Country"
# - "latest year available" → "Year"
# - The long protected areas column → "ProtectedAreaPct"
df = df.rename(columns={
    "Country and area": "Country",
    "latest year available": "Year",
    "Terrestrial and marine protected areas (% of total territorial area)": "ProtectedAreaPct"
})

# Remove rows where the "ProtectedAreaPct" column is empty or just spaces:
# - `str(x).strip()` removes spaces from the value.
# - `.ne("")` keeps only rows where the value is NOT empty.
df = df[df["ProtectedAreaPct"].apply(lambda x: str(x).strip()).ne("")]

# Convert the "ProtectedAreaPct" column from text (like "5.2") to a number (like 5.2) so we can do math and color the map.
df["ProtectedAreaPct"] = df["ProtectedAreaPct"].astype(float)


# --- SETTING UP THE WEB APP ---

# Create a new Dash web application and name it 'app'.
# `__name__` tells Dash where to find files (needed for advanced features).
app = Dash(__name__)

# Define the layout (structure) of the web page:
# - `html.Div` is a container that holds everything.
# - Inside it, we have:
#   1. A big heading (`html.H1`) saying "Global Biodiversity Protection Map".
#   2. An empty graph (`dcc.Graph`) with ID "world-map" and a height of 700 pixels.
#   3. A box (`html.Div`) with ID "country-info" for displaying country details later.
app.layout = html.Div([
    html.H1("Global Biodiversity Protection Map"),
    dcc.Graph(id="world-map", style={"height": "700px"}),
    html.Div(id="country-info", style={"padding": "20px", "fontSize": "18px"})
])


# --- MAKING THE APP INTERACTIVE ---

# This is a "callback": a function that runs when a user interacts with the app.
# Here, it updates the map and info box when a country is clicked.
# - `Output("world-map", "figure")`: The map will be updated with a new figure.
# - `Output("country-info", "children")`: The info box will show new text.
# - `Input("world-map", "clickData")`: The trigger is clicking the map.
@app.callback(
    Output("world-map", "figure"), #updates how the map is appeared on your screen
    Output("country-info", "children"), #update the info displayed on the info box
    Input("world-map", "clickData") #clicking on stuff triggers these changes
)

# Define the function that runs when the map is clicked.
# `click_data` stores which country was clicked (or `None` if nothing was clicked yet).
def update_map(click_data):
    # Create a world map where:
    # - Countries are colored based on "ProtectedAreaPct".
    # - Hovering shows the country name.
    # - Colors use the "Viridis" scale (yellow = high, purple = low).
    # - The scale ranges from 0% to 60%.
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

    # Improve the map's appearance:
    # - Show country borders (`showcountries`).
    # - Show coastlines (`showcoastlines`).
    # - Fit the map to the data (`fitbounds`).
    fig.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations")

    # If a country was clicked (`click_data` exists):
    if click_data:
        # Get the name of the clicked country from the click data.
        country_clicked = click_data["points"][0]["location"]

        # Find the row in the data for the clicked country.
        info_row = df[df["Country"] == country_clicked]

        # If data exists for this country:
        if not info_row.empty:
            # Get the first matching row (`.iloc[0]`).
            row = info_row.iloc[0]

            # Create a formatted string with the country's details, separated by tabs (`\t`).
            info = f"""
            Country: {row['Country']} \t   
            Year: {row['Year']}\t  
            Protected Area: {row['ProtectedAreaPct']}%
            """
        else:
            # If no data exists, show a message.
            info = f"No data available for {country_clicked}."
    else:
        # If no country was clicked yet, show instructions.
        info = "Click on a country to see detailed biodiversity data."

    # Return the updated map and info text to display.
    return fig, info


# --- RUN THE APP ---

# This block runs only if the script is executed directly (not imported as a module).
# It starts the Dash app in debug mode (auto-reloads when code changes).
if __name__ == "__main__":
    app.run(debug=True)