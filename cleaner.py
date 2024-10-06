import pandas as pd

# Function to remove outliers from the 'Number' column and save to a new CSV
def remove_outliers(csv_file_path, output_csv_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Calculate Q1 (25th percentile) and Q3 (75th percentile)
    Q1 = df['Number'].quantile(0.25)
    Q3 = df['Number'].quantile(0.75)

    # Calculate Interquartile Range (IQR)
    IQR = Q3 - Q1

    # Define lower and upper bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Remove rows with 'Number' column values outside the bounds
    df_cleaned = df[(df['Number'] >= lower_bound) & (df['Number'] <= upper_bound)]

    # Save the cleaned DataFrame to a new CSV file
    df_cleaned.to_csv(output_csv_file_path, index=False)

    print(f"Cleaned data saved to {output_csv_file_path}")

# Use the function with your CSV file paths
csv_file_path = './fall/monarch_larva_concatenated.csv'  # Replace with your input CSV file path
output_csv_file_path = './fall/monarch_larva_cleaner.csv'  # Replace with desired output CSV file path
remove_outliers(csv_file_path, output_csv_file_path)

