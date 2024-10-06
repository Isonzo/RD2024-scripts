import pandas as pd
import plotly.express as px
import numpy as np
import sys

# Function to read the CSV and plot data on a US map with a gradual color gradient based on the date
def plot_lat_lon_data_with_gradual_gradient(csv_file_path, title):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        
        # Ensure necessary columns exist in the CSV
        required_columns = ['Latitude', 'Longitude', 'Date', 'Town', 'State/Province', 'Number']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"The CSV file is missing the following required columns: {', '.join(missing_columns)}")
        
        # Inspect unique date formats (Optional but recommended)
        # Uncomment the following lines to see unique date formats
        # unique_dates = df['Date'].dropna().unique()
        # print("Sample Dates:", unique_dates[:10])
        
        # Convert the 'Date' column to datetime format without specifying the format
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Removed infer_datetime_format=True
        
        # Drop rows with invalid or missing dates
        initial_row_count = df.shape[0]
        df = df.dropna(subset=['Date'])
        final_row_count = df.shape[0]
        dropped_rows = initial_row_count - final_row_count
        if dropped_rows > 0:
            print(f"Warning: Dropped {dropped_rows} rows due to invalid or missing dates.")
        
        # Convert 'Date' to numeric format (timestamps in seconds)
        df['DateNumeric'] = df['Date'].astype('int64') / 1e9  # Convert nanoseconds to seconds
        
        # Add a formatted date column for hover
        df['DateFormatted'] = df['Date'].dt.strftime('%Y-%m-%d')
        
        # Determine minimum and maximum DateNumeric for color range
        min_date_numeric = df['DateNumeric'].min()
        max_date_numeric = df['DateNumeric'].max()
        
        # Create the scatter_geo plot
        fig = px.scatter_geo(
            df,
            lat='Latitude',
            lon='Longitude',
            color='DateNumeric',  # Use the numeric date for color mapping
            hover_name='Town',
            hover_data={
                'State/Province': True,
                'Number': True,
                'DateFormatted': True,
                'Latitude': False,
                'Longitude': False
            },
            scope='usa',
            title=title,
            color_continuous_scale='inferno',  # Choose a color scale suitable for gradients
            range_color=[min_date_numeric, max_date_numeric],  # Set color range based on data
            labels={'DateNumeric': 'Date'}
        )
        
        # Create tick values and labels for the color bar
        num_ticks = 5
        tickvals = np.linspace(min_date_numeric, max_date_numeric, num_ticks)
        ticktext = pd.to_datetime(tickvals * 1e9).strftime('%Y-%m-%d')  # Convert back to datetime for labels

        # Update the color bar with custom ticks
        fig.update_layout(coloraxis_colorbar=dict(
            title='Date',
            tickvals=tickvals,
            ticktext=ticktext,
        ))
        
        # Adjust marker size (optional)
        fig.update_traces(marker=dict(size=8))
        
        # Show the figure
        fig.show()
    
    except FileNotFoundError:
        print(f"Error: The file '{csv_file_path}' was not found. Please check the file path.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{csv_file_path}' is empty.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    # Check for the correct number of command-line arguments
    if len(sys.argv) != 3:
        print('Usage: python ChronoGeoPlotter.py csv_file_path "Plot Title"')
        sys.exit(1)
    
    # Assign command-line arguments to variables
    csv_file_path = sys.argv[1]
    title = sys.argv[2]
    
    # Call the plotting function with provided arguments
    plot_lat_lon_data_with_gradual_gradient(csv_file_path, title)

