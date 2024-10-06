import pandas as pd

# Load the CSV data
data = pd.read_csv('USDA_PDP_AnalyticalResults.csv')

df = pd.DataFrame(data)

# Extract state from the first two characters of the 'Sample ID'
df['State'] = df['Sample ID'].str[:2]


# Count the number of rows for each state
state_counts = df['State'].value_counts()

# Display the counts for each state
print(state_counts)

