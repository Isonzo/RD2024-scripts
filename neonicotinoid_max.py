import pandas as pd
import plotly.express as px

# Step 1: Read and Preprocess the Data
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

    # Step 2: Get the highest concentration neonicotinoid per state
    highest_neonic_per_state = df_neonic.loc[df_neonic.groupby('State')['Concentration'].idxmax()]

    # Extract state, concentration, and pesticide name
    state_neonic_data = highest_neonic_per_state[['State', 'PesticideName', 'Concentration']]

    return state_neonic_data

# Step 6: Visualize the Data
def visualize_neonicotinoid_data(state_data):
    # Create a choropleth map
    fig = px.choropleth(
        state_data,
        locations='State',
        locationmode="USA-states",
        color='Concentration',
        scope="usa",
        color_continuous_scale="Reds",
        labels={'Concentration': 'Highest Neonicotinoid Concentration'},
        hover_name='State',
        hover_data={
            'PesticideName': True,
            'Concentration': ':.2f'
        }
    )

    fig.update_layout(
        title_text='Highest Neonicotinoid Concentration per State',
        geo=dict(showlakes=True, lakecolor='rgb(85,173,240)'),
    )

    fig.show()

# Example usage
csv_file = "C:/Users/arpan/Downloads/drive-download-20241005T170524Z-001/USB Drive/USDA_PDP_AnalyticalResults.csv"  # Replace with your CSV file path
state_neonic_data = process_neonicotinoid_data(csv_file)
visualize_neonicotinoid_data(state_neonic_data)
