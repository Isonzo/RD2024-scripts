import requests
from bs4 import BeautifulSoup
import csv

# Base URL components
base_url = 'https://journeynorth.org/sightings/querylist.html'
map = 'monarch-larva-spring'
params = {
    'season': 'spring',
    'map': map,
    'year': '',  # We'll fill this in the loop
    'submit': 'View Data'
}

# Years to scrape
start_year = 2024
end_year = 1997

# Loop over the years from 2024 to 1997
for year in range(start_year, end_year - 1, -1):
    print(f"Scraping data for year {year}...")
    params['year'] = str(year)
    # Construct the URL with query parameters
    response = requests.get(base_url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table element by its ID
        table = soup.find('table', {'id': 'querylist'})

        # Ensure the table exists
        if table:
            # Extract rows from the table body to skip the header row
            tbody = table.find('tbody')
            rows = tbody.find_all('tr') if tbody else []

            # Open a CSV file to save the data
            filename = f'{map}_{year}.csv'
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)

                # Write headers to the CSV file
                headers = ["Index", "Date", "Town", "State/Province", "Latitude", "Longitude", "Number", "Image"]
                csvwriter.writerow(headers)

                # Loop through each row and extract the cells (columns)
                for row in rows:
                    # Extract cells from the row
                    cells = row.find_all('td')

                    # Skip rows without the expected number of cells
                    if len(cells) != 8:
                        continue

                    # Process each cell
                    row_data = []

                    # Index
                    index_text = cells[0].get_text(strip=True)
                    row_data.append(index_text)

                    # Date
                    date_link = cells[1].find('a')
                    date_text = date_link.get_text(strip=True) if date_link else cells[1].get_text(strip=True)
                    row_data.append(date_text)

                    # Town
                    town_text = cells[2].get_text(strip=True)
                    row_data.append(town_text)

                    # State/Province
                    state_text = cells[3].get_text(strip=True)
                    row_data.append(state_text)

                    # Latitude
                    lat_text = cells[4].get_text(strip=True)
                    row_data.append(lat_text)

                    # Longitude
                    lon_text = cells[5].get_text(strip=True)
                    row_data.append(lon_text)

                    # Number
                    number_text = cells[6].get_text(strip=True)
                    row_data.append(number_text)

                    # Image
                    image_cell = cells[7]
                    img_tag = image_cell.find('img')
                    if img_tag:
                        img_src = img_tag.get('src', '')
                        # Check if image is a spacer or meaningful
                        if 'spacer.gif' in img_src:
                            image_value = 0
                        else:
                            image_value = 1
                    else:
                        image_value = 0  # No image tag
                    row_data.append(image_value)

                    # Write the extracted row data to the CSV file
                    csvwriter.writerow(row_data)

            print(f"Data for year {year} has been written to {filename}")
        else:
            print(f"No data table found for year {year}.")
    else:
        print(f"Failed to retrieve data for year {year}. Status code: {response.status_code}")

