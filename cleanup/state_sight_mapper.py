import pandas as pd
import plotly.express as px
import sys

# Function to read the CSV and plot a choropleth map of the US
def plot_state_data(csv_file_path, title, gradient_label):
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
        title=title,
        color_continuous_scale='Viridis',
        labels={'Number': gradient_label},
        hover_name='State/Province'
    )

    # Show the figure
    fig.show()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python program.py csv_file_path "Plot Title" "Gradient Label"')
        sys.exit(1)
    csv_file_path = sys.argv[1]
    title = sys.argv[2]
    gradient_label = sys.argv[3]
    plot_state_data(csv_file_path, title, gradient_label)

