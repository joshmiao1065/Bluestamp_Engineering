import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv('Terrestrial_Marine protected areas.csv')

# Clean up column names (remove any special characters)
df.columns = ['CountryID', 'Country', 'LatestYear', 'ProtectedAreasPct']

# Create the interactive map
fig = px.choropleth(df, 
                    locations="Country",  # Column with country names
                    locationmode='country names',  # Set to use country names
                    color="ProtectedAreasPct",  # Values to color by
                    hover_name="Country",  # What shows up on hover
                    hover_data=['LatestYear', 'ProtectedAreasPct'],
                    color_continuous_scale=px.colors.sequential.YlGn,  # Green color scale
                    title='Terrestrial and Marine Protected Areas (% of total territorial area)',
                    labels={'ProtectedAreasPct':'Protected Areas %'})

# Customize the layout
fig.update_layout(
    margin={"r":0,"t":30,"l":0,"b":0},
    coloraxis_colorbar=dict(
        title="% Protected",
        thickness=20,
        len=0.75,
        yanchor="middle",
        y=0.5
    )
)

# Save the visualization as an HTML file
fig.write_html("protected_areas_map.html")

print("Visualization saved as 'protected_areas_map.html'. Open this file in your web browser.")