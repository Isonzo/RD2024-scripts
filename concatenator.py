import pandas as pd

def concatenate_csvs(csv1_path, csv2_path, output_path):
    # Load CSV files
    df1 = pd.read_csv(csv1_path)
    df2 = pd.read_csv(csv2_path)

    # Remove the first column from both dataframes
    df1 = df1.iloc[:, 1:]
    df2 = df2.iloc[:, 1:]

    # Concatenate the two dataframes
    concatenated_df = pd.concat([df1, df2], ignore_index=True)

    # Write the concatenated dataframe to the output CSV file
    concatenated_df.to_csv(output_path, index=False)

# Example usage
concatenate_csvs('full_larva_2024.csv', './raw_spring/monarch_larva_first/monarch-larva-first_2024.csv', 'full_larva_2024.csv')

