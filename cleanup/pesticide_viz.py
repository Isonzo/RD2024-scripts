import pandas as pd
import plotly.express as px

# Step 1: Read and Preprocess the Pesticide Data
def process_pesticide_data(csv_file):
    # Define column names based on your data structure
    column_names = [
        'SampleID', 'Type', 'PesticideCode', 'PesticideName', 'Category',
        'Concentration', 'Limit', 'ResultQualifier', 'ResultQualifier2',
        'Column9', 'Column10', 'Column11', 'Column12', 'Column13', 'Column14', 'Column15'
    ]

    # Read the CSV data
    df = pd.read_csv(csv_file, names=column_names, header=None, low_memory=False)

    # Extract State Information
    df['State'] = df['SampleID'].str[:2]

    # Convert concentration to numeric, coerce errors to NaN
    df['Concentration'] = pd.to_numeric(df['Concentration'], errors='coerce')

    # Drop rows with NaN concentration
    df = df.dropna(subset=['Concentration'])

    # Exclude New Hampshire from the pesticide data if needed
    # Comment out the next line if you want to include New Hampshire
    # df = df[df['State'] != 'NH']

    # Aggregate Pesticide Data per State (using median concentration)
    state_pesticide_concentration = df.groupby('State')['Concentration'].median().reset_index()

    return state_pesticide_concentration

# Step 2: Aggregate Milkweed Data by State
def process_milkweed_data(csv_file):
    df = pd.read_csv(csv_file)

    # Standardize state names to uppercase to avoid duplicates
    df['State/Province'] = df['State/Province'].str.upper()

    # Count the number of milkweed sightings per state
    state_milkweed = df['State/Province'].value_counts().reset_index()
    state_milkweed.columns = ['State', 'MilkweedCount']

    return state_milkweed

# Step 3: Aggregate Larva Data by State
def process_larva_data(csv_file):
    df = pd.read_csv(csv_file)

    # Standardize state names to uppercase to avoid duplicates
    df['State/Province'] = df['State/Province'].str.upper()

    # Count the number of larva sightings per state
    state_larva = df['State/Province'].value_counts().reset_index()
    state_larva.columns = ['State', 'LarvaCount']

    return state_larva

# Step 4: Combine the Aggregated Data
def combine_data(pesticide_data, milkweed_data, larva_data):
    # Collect all unique states from all datasets
    all_states = pd.concat([pesticide_data['State'], milkweed_data['State'], larva_data['State']]).unique()
    combined_data = pd.DataFrame({'State': all_states})

    # Merge datasets
    combined_data = combined_data.merge(pesticide_data, on='State', how='left')
    combined_data = combined_data.merge(milkweed_data, on='State', how='left')
    combined_data = combined_data.merge(larva_data, on='State', how='left')

    # Fill NaN values with 0 for counts and keep NaN for 'Concentration' where appropriate
    combined_data['MilkweedCount'] = combined_data['MilkweedCount'].fillna(0)
    combined_data['LarvaCount'] = combined_data['LarvaCount'].fillna(0)

    return combined_data

# Step 5: Visualize the Data on a US Map with a Dropdown Menu
def visualize_data_on_map(combined_data):
    import plotly.graph_objects as go

    # Create a dictionary of data for each variable
    data_dict = {
        'Median Pesticide Concentration': {
            'data': combined_data,
            'z_column': 'Concentration',
            'colorscale': 'Reds',
            'colorbar_title': 'Concentration (Median)'
        },
        'Milkweed Sightings': {
            'data': combined_data,
            'z_column': 'MilkweedCount',
            'colorscale': 'Greens',
            'colorbar_title': 'Number of Sightings'
        },
        'Larva Count': {
            'data': combined_data,
            'z_column': 'LarvaCount',
            'colorscale': 'Blues',
            'colorbar_title': 'Number of Larva Sightings'
        }
    }

    # Initialize the figure
    fig = go.Figure()

    # Add a choropleth trace for each variable but make all except the first invisible
    first = True
    for idx, (key, value) in enumerate(data_dict.items()):
        plot_data = value['data'].copy()

        # Get the 'z' values from the specified column
        z_values = plot_data[value['z_column']]

        fig.add_trace(go.Choropleth(
            locations=plot_data['State'],
            z=z_values,
            locationmode='USA-states',
            colorscale=value['colorscale'],
            colorbar_title=value['colorbar_title'],
            zmin=z_values.min(),
            zmax=z_values.max(),
            visible=first,
            name=key
        ))
        first = False  # Only the first trace is visible by default

    # Update the layout
    fig.update_layout(
        title_text='US Map: Median Pesticide Concentration, Milkweed Sightings, and Larva Count',
        geo_scope='usa',
    )

    # Create dropdown buttons
    buttons = []
    for i, key in enumerate(data_dict.keys()):
        button = dict(
            method='update',
            label=key,
            args=[
                {'visible': [j == i for j in range(len(data_dict))]},  # Update the visibility of traces
                {'title': f'US Map: {key}'}
            ]
        )
        buttons.append(button)

    # Add the dropdown to the layout
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=buttons,
                x=0.1,
                y=1.1,
                xanchor='left',
                yanchor='top'
            )
        ]
    )

    # Show the figure
    fig.show()

# Example usage
pesticide_csv_file = './USDA_PDP_AnalyticalResults.csv'  # Replace with your pesticide data CSV file path
milkweed_csv_file = './scrape/full_milkweed_2024.csv'    # Replace with your milkweed sightings CSV file path
larva_csv_file = './scrape/full_larva_2024.csv'          # Replace with your larva sightings CSV file path

# Process each dataset
state_pesticide_data = process_pesticide_data(pesticide_csv_file)
state_milkweed_data = process_milkweed_data(milkweed_csv_file)
state_larva_data = process_larva_data(larva_csv_file)

# Combine the data
combined_state_data = combine_data(state_pesticide_data, state_milkweed_data, state_larva_data)

# Visualize the data on a US map with a dropdown menu
visualize_data_on_map(combined_state_data)

