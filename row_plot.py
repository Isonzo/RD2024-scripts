import pandas as pd
import plotly.express as px

# Function to read the CSV and plot a choropleth map of the US based on the count of rows per state
def plot_state_data(csv_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Standardize state names to uppercase to avoid duplicates
    df['State/Province'] = df['State/Province'].str.upper()

    # Count the number of milkweed sightings per state
    state_data = df['State/Province'].value_counts().reset_index()
    state_data.columns = ['State/Province', 'Count']

    # Plotting with Plotly
    fig = px.choropleth(
        state_data,
        locations='State/Province',
        locationmode='USA-states',
        color='Count',
        scope='usa',
        title='Number of Milkweed Sightings per State',
        color_continuous_scale='Viridis',
        labels={'Count': 'Number of Milkweed Sightings'},
        hover_name='State/Province'
    )

    # Show the figure
    fig.show()

# Use the function with your CSV file
csv_file_path = './full_milkweed_2024.csv'  # Replace with your CSV file path
plot_state_data(csv_file_path)

