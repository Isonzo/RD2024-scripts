import pandas as pd
import plotly.express as px

# Step 1: Read and Preprocess the Data
def process_pesticide_data(csv_file):
    # Define column names based on your data structure
    column_names = [
        'SampleID', 'Type', 'PesticideCode', 'PesticideName', 'Category',
        'Concentration', 'Limit', 'ResultQualifier', 'ResultQualifier2',
        'Column9', 'Column10', 'Column11', 'Column12', 'Column13', 'Column14', 'Column15'
    ]

    # Read the CSV data
    df = pd.read_csv(csv_file, names=column_names, header=None)

    # Step 2: Extract State Information
    df['State'] = df['SampleID'].str[:2]

    # Convert concentration to numeric, coerce errors to NaN
    df['Concentration'] = pd.to_numeric(df['Concentration'], errors='coerce')

    # Drop rows with NaN concentration
    df = df.dropna(subset=['Concentration'])

    # Step 3: Aggregate Data per State
    state_concentration = df.groupby('State')['Concentration'].median().reset_index()

    # Step 4: Identify the Most Common Pesticide per State
    pesticide_counts = df.groupby(['State', 'PesticideName']).size().reset_index(name='Counts')
    idx = pesticide_counts.groupby('State')['Counts'].idxmax()
    most_common_pesticide = pesticide_counts.loc[idx].reset_index(drop=True)

    # Step 5: Determine Neonicotinoid Status
    neonicotinoids = [
        'Imidacloprid', 'Thiamethoxam', 'Clothianidin',
        'Acetamiprid', 'Dinotefuran', 'Nitenpyram', 'Thiacloprid'
    ]
    most_common_pesticide['IsNeonicotinoid'] = most_common_pesticide['PesticideName'].isin(neonicotinoids)

    # Merge concentration and pesticide data
    state_data = pd.merge(state_concentration, most_common_pesticide[['State', 'IsNeonicotinoid']], on='State')

    return state_data

# Step 6: Visualize the Data
def visualize_pesticide_data(state_data):
    # Create a choropleth map
    fig = px.choropleth(
        state_data,
        locations='State',
        locationmode="USA-states",
        color='Concentration',
        scope="usa",
        hover_data={'IsNeonicotinoid': True},
        color_continuous_scale="Blues",
        labels={'Concentration': 'Avg Concentration'},
    )

    # Update hover template to include neonicotinoid status
    fig.update_traces(
        hovertemplate="<b>%{location}</b><br>" +
                      "Avg Concentration: %{z:.2f}<br>" +
                      "Most Common Pesticide is Neonicotinoid: %{customdata[0]}"
    )

    fig.update_layout(
        title_text='Pesticide Concentration per State',
        geo=dict(showlakes=True, lakecolor='rgb(85,173,240)'),
    )

    fig.show()

# Example usage
csv_file = './USDA_PDP_AnalyticalResults.csv'  # Replace with your CSV file path
state_data = process_pesticide_data(csv_file)
visualize_pesticide_data(state_data)

