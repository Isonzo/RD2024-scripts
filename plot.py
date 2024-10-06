import pandas as pd
import plotly.express as px

# Function to read the CSV and plot a choropleth map of the US
def plot_state_data(csv_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Standardize state names to uppercase to avoid duplicates
    df['State/Province'] = df['State/Province'].str.upper()

    # Aggregate data by state and sum the 'Number' column
    state_data = df.groupby('State/Province').agg({'Number': 'sum'}).reset_index()

    # Plotting with Plotly
    fig = px.choropleth(
        state_data,
        locations='State/Province',
        locationmode='USA-states',
        color='Number',
        scope='usa',
        title='Number of Milkweed sightings per State',
        color_continuous_scale='Viridis',
        labels={'Number': 'Number of Milkweed'},
        hover_name='State/Province'
    )

    # Show the figure
    fig.show()

# Use the function with your CSV file
csv_file_path = './full_milkweed_2024.csv'  # Replace with your CSV file path
plot_state_data(csv_file_path)

