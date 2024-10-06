import pandas as pd

# Load the CSV data
df = pd.read_csv('USDA_PDP_AnalyticalResults.csv')

# Count the occurrences of each pesticide in the entire dataset
pesticide_counts = df['Pesticide Name'].value_counts()

# Display the counts of each pesticide
print(pesticide_counts)
