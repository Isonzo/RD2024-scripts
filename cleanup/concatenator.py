import pandas as pd
import argparse
import os
import sys

def concatenate_csvs(input_csv_paths, output_csv_path):
    """
    Concatenates multiple CSV files by removing their first columns and combining the remaining data.

    Parameters:
    - input_csv_paths (list of str): Paths to the input CSV files.
    - output_csv_path (str): Path where the concatenated CSV will be saved.
    """
    try:
        concatenated_df = pd.DataFrame()
        columns_reference = None  # To check column consistency across CSVs

        for idx, csv_path in enumerate(input_csv_paths):
            print(f"Loading '{csv_path}'...")
            if not os.path.isfile(csv_path):
                print(f"Error: The file '{csv_path}' does not exist.")
                sys.exit(1)
            
            df = pd.read_csv(csv_path)
            
            # Ensure the CSV has at least two columns to remove the first one
            if df.shape[1] < 2:
                print(f"Error: The CSV '{csv_path}' does not have enough columns to remove the first one.")
                sys.exit(1)
            
            # Remove the first column
            df = df.iloc[:, 1:]
            print(f"Removed the first column from '{csv_path}'.")
            
            # Check for column consistency
            if columns_reference is None:
                columns_reference = df.columns
                print(f"Reference columns set from '{csv_path}'.")
            else:
                if not df.columns.equals(columns_reference):
                    print(f"Warning: The columns in '{csv_path}' do not match the reference columns.")
                    print(f"Reference columns: {list(columns_reference)}")
                    print(f"Current CSV columns: {list(df.columns)}")
                    print("Proceeding with concatenation, but the resulting CSV may have mismatched columns.")
            
            # Append to the concatenated dataframe
            concatenated_df = pd.concat([concatenated_df, df], ignore_index=True)
            print(f"Appended data from '{csv_path}'.")

        # Write the concatenated dataframe to the output CSV file
        print(f"Writing the concatenated data to '{output_csv_path}'...")
        concatenated_df.to_csv(output_csv_path, index=False)
        print("Concatenation completed successfully!")

    except pd.errors.EmptyDataError:
        print(f"Error: One of the input CSV files is empty.")
        sys.exit(1)
    except pd.errors.ParserError as pe:
        print(f"Error parsing CSV files: {pe}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(
        description='Concatenate multiple CSV files by removing their first columns.'
    )
    
    # Add arguments for input CSVs and output CSV
    parser.add_argument(
        'input_csvs',
        metavar='INPUT_CSV',
        type=str,
        nargs='+',
        help='Paths to the input CSV files to be concatenated.'
    )
    parser.add_argument(
        '-o', '--output',
        dest='output_csv',
        type=str,
        required=True,
        help='Path to save the concatenated CSV file.'
    )

    # Parse the arguments
    args = parser.parse_args()

    # Call the concatenate function with the provided arguments
    concatenate_csvs(args.input_csvs, args.output_csv)

if __name__ == '__main__':
    main()

