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

    # Step 3: Aggregate Neonicotinoid Data per State
    state_neonic_concentration = df_neonic.groupby('State')['Concentration'].median().reset_index()

    # Optional: Include states with zero concentration
    all_states = df['State'].unique()
    state_neonic_concentration = pd.DataFrame({'State': all_states}).merge(
        state_neonic_concentration, on='State', how='left'
    )
    state_neonic_concentration['Concentration'] = state_neonic_concentration['Concentration'].fillna(0)

    return state_neonic_concentration

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
        labels={'Concentration': 'Avg Neonicotinoid Concentration'},
        hover_data={'Concentration': ':.2f'}
    )

    fig.update_layout(
        title_text='Average Neonicotinoid Concentration per State',
        geo=dict(showlakes=True, lakecolor='rgb(85,173,240)'),
    )

    fig.show()

# Example usage
csv_file = './USDA_PDP_AnalyticalResults.csv'  # Replace with your CSV file path
state_neonic_data = process_neonicotinoid_data(csv_file)
visualize_neonicotinoid_data(state_neonic_data)

