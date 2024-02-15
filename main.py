import pandas as pd
import folium
from folium.plugins import HeatMap
import geopandas


map = folium.Map(location=(32.7555, -97.3308), zoom_start=12)

# GeoPath data to draw the lines of the zipcoes
geo_data = geopandas.read_file("datasets/kx-fort-worth-texas-zip-codes-SHP.zip")

# data to map the median household incomes to zipcodes
zipcode_data = pd.read_csv("datasets/census_data_output.csv")

folium.Choropleth(
    geo_data=geo_data,
    data=zipcode_data,
    fill_color="YlGn",
    columns=["ZIP_Code", "Median Household Income"],
    key_on="feature.properties.POSTAL",
    bins=8,
).add_to(map)


# Pins all local mediterranean restaunts
df = pd.read_csv("datasets/restaurants.csv")

for row in df.itertuples():

    folium.Marker(
        location=(row.Latitude, row.Longitude),
        tooltip=row.Name,
        popup=f"Rating: {row.Rating}",
        icon=folium.Icon(color="green"),
    ).add_to(map)


# Creates a heat map of the crime in the area
df = pd.read_csv("datasets/fort-worth-texas-crime-data.csv")
sample_size = 1000

location_data = pd.DataFrame(
    {"latitude": df["Latitude"].values, "longitude": df["Longitude"].values}
)
location_data["cordinates"] = list(
    zip(location_data["latitude"], location_data["longitude"])
)

random_vals = location_data["cordinates"].sample(n=sample_size).values


HeatMap(random_vals).add_to(map)
map.save("map.html")
print("\n--- map saved. you can open it in your local browser ---\n")
