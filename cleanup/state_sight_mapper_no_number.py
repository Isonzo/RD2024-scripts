import pandas as pd
import plotly.express as px
import argparse
import os
import sys

def plot_state_data(csv_file_path, title, gradient_label):
    """
    Reads a CSV file and plots a choropleth map of the US based on the count of rows per state.

    Parameters:
    - csv_file_path (str): Path to the input CSV file.
    - title (str): Title of the choropleth map.
    - gradient_label (str): Label for the color gradient.
    """
    try:
        # Check if the CSV file exists
        if not os.path.isfile(csv_file_path):
            print(f"Error: The file '{csv_file_path}' does not exist.")
            sys.exit(1)
        
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        print(f"Successfully loaded '{csv_file_path}'.")

        # Ensure the required column exists
        if 'State/Province' not in df.columns:
            print("Error: The CSV file must contain a 'State/Province' column.")
            sys.exit(1)

        # Standardize state names to uppercase to avoid duplicates
        df['State/Province'] = df['State/Province'].str.upper()
        print("Standardized 'State/Province' names to uppercase.")

        # Count the number of sightings per state
        state_data = df['State/Province'].value_counts().reset_index()
        state_data.columns = ['State/Province', 'Count']
        print("Counted sightings per state.")

        # Optional: Validate state abbreviations (assuming two-letter abbreviations)
        # List of US state abbreviations
        us_states = {
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
            'DC'
        }
        invalid_states = state_data[~state_data['State/Province'].isin(us_states)]
        if not invalid_states.empty:
            print("Warning: The following state abbreviations are invalid or not recognized:")
            print(invalid_states['State/Province'].unique())
            print("They will still be plotted, but may not appear correctly on the map.")

        # Plotting with Plotly
        fig = px.choropleth(
            state_data,
            locations='State/Province',
            locationmode='USA-states',
            color='Count',
            scope='usa',
            title=title,
            color_continuous_scale='Viridis',
            labels={'Count': gradient_label},
            hover_name='State/Province'
        )
        print("Choropleth map created.")

        # Show the figure
        fig.show()
        print("Plot displayed successfully.")

    except pd.errors.EmptyDataError:
        print(f"Error: The file '{csv_file_path}' is empty.")
        sys.exit(1)
    except pd.errors.ParserError as pe:
        print(f"Error parsing CSV file: {pe}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(
        description='Plot a choropleth map of the US based on the count of rows per state.'
    )
    
    # Add arguments for CSV file, plot title, and gradient label
    parser.add_argument(
        'csv_file',
        type=str,
        help='Path to the input CSV file.'
    )
    parser.add_argument(
        'title',
        type=str,
        help='Title of the choropleth map.'
    )
    parser.add_argument(
        'gradient_label',
        type=str,
        help='Label for the color gradient.'
    )
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Call the plotting function with provided arguments
    plot_state_data(args.csv_file, args.title, args.gradient_label)

if __name__ == '__main__':
    main()

