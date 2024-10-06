import pandas as pd
import plotly.express as px

# Step 1: Read and Preprocess the Neonicotinoid Data
def process_neonicotinoid_data(csv_file):
    # Define column names based on your data structure
    column_names = [
        'SampleID', 'Type', 'PesticideCode', 'PesticideName', 'Category',
        'Concentration', 'Limit', 'ResultQualifier', 'ResultQualifier2',
        'Column9', 'Column10', 'Column11', 'Column12', 'Column13', 'Column14', 'Column15'
    ]

    # Read the CSV data
    df = pd.read_csv(csv_file, names=column_names, header=None)

    # Extract State Information
    df['State'] = df['SampleID'].str[:2]

    # Convert concentration to numeric, coerce errors to NaN
    df['Concentration'] = pd.to_numeric(df['Concentration'], errors='coerce')

    # Drop rows with NaN concentration
    df = df.dropna(subset=['Concentration'])

    # Define neonicotinoid pesticides
    neonicotinoids = [
        'Imidacloprid', 'Thiamethoxam', 'Clothianidin',
        'Acetamiprid', 'Dinotefuran', 'Nitenpyram', 'Thiacloprid'
    ]

    # Filter the DataFrame to include only neonicotinoid pesticides
    df_neonic = df[df['PesticideName'].isin(neonicotinoids)]

    # Aggregate Neonicotinoid Data per State (using median concentration)
    state_neonic_concentration = df_neonic.groupby('State')['Concentration'].mean().reset_index()

    return state_neonic_concentration

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
def combine_data(neonic_data, milkweed_data, larva_data):
    combined_data = pd.merge(neonic_data, milkweed_data, on='State', how='outer')
    combined_data = pd.merge(combined_data, larva_data, on='State', how='outer')

    # Fill NaN values with 0 (for states missing in any dataset)
    combined_data = combined_data.fillna(0)

    return combined_data

# Step 5: Visualize the Data on a US Map with a Dropdown Menu
def visualize_data_on_map(combined_data):
    import plotly.graph_objects as go

    # Create a dictionary of data for each variable
    data_dict = {
        'Neonicotinoid Concentration': {
            'data': combined_data,
            'z': combined_data['Concentration'],
            'colorscale': 'Reds',
            'colorbar_title': 'Concentration (Median)'
        },
        'Milkweed Sightings': {
            'data': combined_data,
            'z': combined_data['MilkweedCount'],
            'colorscale': 'Greens',
            'colorbar_title': 'Number of Sightings'
        },
        'Larva Count': {
            'data': combined_data,
            'z': combined_data['LarvaCount'],
            'colorscale': 'Blues',
            'colorbar_title': 'Number of Larva Sightings'
        }
    }

    # Initialize the figure
    fig = go.Figure()

    # Add a choropleth trace for each variable but make all except the first invisible
    first = True
    for idx, (key, value) in enumerate(data_dict.items()):
        fig.add_trace(go.Choropleth(
            locations=value['data']['State'],
            z=value['z'],
            locationmode='USA-states',
            colorscale=value['colorscale'],
            colorbar_title=value['colorbar_title'],
            zmin=value['z'].min(),
            zmax=value['z'].max(),
            visible=first,
            name=key
        ))
        first = False  # Only the first trace is visible by default

    # Update the layout
    fig.update_layout(
        title_text='US Map: Neonicotinoid Concentration, Milkweed Sightings, and Larva Count',
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
neonic_csv_file = './USDA_PDP_AnalyticalResults.csv'  # Replace with your neonicotinoid data CSV file path
milkweed_csv_file = './scrape/full_milkweed_2024.csv'         # Replace with your milkweed sightings CSV file path
larva_csv_file = './scrape/full_larva_2024.csv'                    # Replace with your larva sightings CSV file path

# Process each dataset
state_neonic_data = process_neonicotinoid_data(neonic_csv_file)
state_milkweed_data = process_milkweed_data(milkweed_csv_file)
state_larva_data = process_larva_data(larva_csv_file)

# Combine the data
combined_state_data = combine_data(state_neonic_data, state_milkweed_data, state_larva_data)

# Visualize the data on a US map with a dropdown menu
visualize_data_on_map(combined_state_data)

