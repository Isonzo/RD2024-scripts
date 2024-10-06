import pandas as pd
import plotly.express as px
import sys

# Function to read the CSV and plot data on a US map
def plot_lat_lon_data(csv_file_path, title, gradient_label):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        
        # Ensure necessary columns exist in the CSV
        required_columns = ['Latitude', 'Longitude', 'Number', 'Town', 'State/Province']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"The CSV file is missing the following required columns: {', '.join(missing_columns)}")
        
        # Create the scatter_geo plot
        fig = px.scatter_geo(
            df,
            lat='Latitude',
            lon='Longitude',
            color='Number',  # Use size='Number' if you prefer marker sizes to represent 'Number'
            hover_name='Town',
            hover_data={
                'State/Province': True,
                'Number': True,
                'Latitude': False,
                'Longitude': False
            },
            scope='usa',
            title=title,
            color_continuous_scale='Viridis',
            labels={'Number': gradient_label}
        )
        
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
    if len(sys.argv) != 4:
        print('Usage: python program.py csv_file_path "Plot Title" "Gradient Label"')
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    title = sys.argv[2]
    gradient_label = sys.argv[3]
    
    plot_lat_lon_data(csv_file_path, title, gradient_label)

