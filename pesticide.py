import pandas as pd

# Load the full dataset
df = pd.read_csv('USDA_PDP_AnalyticalResults.csv')  # Replace with your actual CSV file path
# Extract state information from the 'Sample ID' (first two letters)
df['State'] = df['Sample ID'].str[:2]

# Filter the dataset to only include California (CA)
ca_data = df[df['State']]

# Count the occurrences of each pesticide in California
pesticide_counts = ca_data['Pesticide Name'].value_counts()

# Display the counts of each pesticide
print(pesticide_counts)

