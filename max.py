import pandas as pd

# Read the CSV file
csv_file_path = './fall/monarch_adult_cleaned.csv'  # Replace with your CSV file path
df = pd.read_csv(csv_file_path)

# Find the highest value in the 'Number' column
max_value = df['Number'].max()

# Print the highest value
print("The highest value in the 'Number' column is:", max_value)

