import geopandas as gpd
import matplotlib.pyplot as plt

# Load the shapefile from your local path (update the path to match your extracted location)
usa = gpd.read_file("./shapely/ne_110m_admin_1_states_provinces.shp")


usa = usa[usa.name == "United States of America"]  # Filter for the USA

usa.plot(figsize=(10, 10), color='lightblue', edgecolor='black', aspect='auto')
plt.title("Map of the USA")
plt.show()

usa.plot(figsize=(10, 10), color='lightblue', edgecolor='black')
plt.title("Map of the USA")
plt.show()


