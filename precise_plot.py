import pandas as pd
import plotly.express as px

# Function to read the CSV and plot data on a US map
def plot_lat_lon_data(csv_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Create the scatter_geo plot
    fig = px.scatter_geo(
        df,
        lat='Latitude',
        lon='Longitude',
        color='Number',  # Use size='Number' if you prefer marker sizes to represent 'Number'
        hover_name='Town',
        hover_data={
            'State/Province': True,
            'Number': True,
            'Latitude': False,
            'Longitude': False
        },
        scope='usa',
        title='Butterfly Sightings in the US',
        color_continuous_scale='Viridis',
    )
    
    # Adjust marker size (optional)
    fig.update_traces(marker=dict(size=8))
    
    # Show the figure
    fig.show()

# Use the function with your CSV file
csv_file_path = './raw_fall/monarch_adult/monarch-adult-fall_2024.csv'  # Replace with your actual CSV file path
plot_lat_lon_data(csv_file_path)

