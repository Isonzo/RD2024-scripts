import pandas as pd
import plotly.express as px
import numpy as np

# Function to read the CSV and plot data on a US map with a gradual color gradient based on the date
def plot_lat_lon_data_with_gradual_gradient(csv_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Convert the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')
    
    # Convert 'Date' to numeric format (timestamps in milliseconds)
    df['DateNumeric'] = df['Date'].astype('int64') / 1e9  # Convert nanoseconds to seconds
    
    # Create the scatter_geo plot
    fig = px.scatter_geo(
        df,
        lat='Latitude',
        lon='Longitude',
        color='DateNumeric',  # Use the numeric date for color mapping
        hover_name='Town',
        hover_data={
            'State/Province': True,
            'Number': True,
            'Latitude': False,
            'Longitude': False
        },
        scope='usa',
        title='Butterfly Sightings in the US Over Time',
        color_continuous_scale='inferno',  # Choose a color scale suitable for gradients
    )
    
    # Create tick values and labels for the color bar
    num_ticks = 5
    tickvals = np.linspace(df['DateNumeric'].min(), df['DateNumeric'].max(), num_ticks)
    ticktext = pd.to_datetime(tickvals * 1e9).strftime('%Y-%m-%d')  # Convert back to datetime for labels

    # Update the color bar with custom ticks
    fig.update_layout(coloraxis_colorbar=dict(
        title='Date',
        tickvals=tickvals,
        ticktext=ticktext,
    ))
    
    # Adjust marker size (optional)
    fig.update_traces(marker=dict(size=8))
    
    # Show the figure
    fig.show()

# Use the function with your CSV file
csv_file_path = './full_1997.csv'  # Replace with your actual CSV file path
plot_lat_lon_data_with_gradual_gradient(csv_file_path)

