import argparse
import osxphotos
from datetime import datetime
import pytz
import geojson
import folium
import json

# const that is filename
GEOJSON_FILENAME = "trip.geojson"
MAP_FILENAME = "map.html"
JSON_FILENAME = "trip.json"

def get_desired_photos(start_date, end_date):
    photosdb = osxphotos.PhotosDB()
    photos = photosdb.photos()
    matching_photos = []

    # get the photos that are in the date range and have location data
    for p in photos:
        if start_date <= p.date <= end_date and p.latitude is not None and p.longitude is not None:
            matching_photos.append(p)

    # Sort the matching photos by date
    matching_photos.sort(key=lambda p: p.date)

    return matching_photos

def generate_geojson(photos):
    geojson_features = []

    line_coordinates = []
    for p in photos:
        line_coordinates.append((p.longitude, p.latitude))

    # Correct the creation of LineString
    line_string = geojson.LineString(line_coordinates)

    feature = geojson.Feature(
        geometry=line_string,
        properties={"description": "driving trip through southern France"}
    )

    # Create a FeatureCollection
    feature_collection = geojson.FeatureCollection([feature])

    with open(GEOJSON_FILENAME, 'w') as f:
        geojson.dump(feature_collection, f)


def generate_json(photos):
    json_data = []
    for p in photos:
        json_data.append({
            "date": p.date.strftime("%Y-%m-%d-%H:%M"),
            "city": p.place.address.city,
            "country": p.place.country_code,
            "latitude": p.latitude,
            "longitude": p.longitude
        })
    with open(JSON_FILENAME, 'w') as f:
        json.dump(json_data, f)


def build_map(photos):
    if not photos:
        print("No photos found")
        return

    # Calculate the bounding box of all the points
    min_lat = min(p.latitude for p in photos)
    max_lat = max(p.latitude for p in photos)
    min_lon = min(p.longitude for p in photos)
    max_lon = max(p.longitude for p in photos)

    # Calculate the center of the bounding box
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2

    # Calculate the zoom level based on the bounding box size
    lat_diff = max_lat - min_lat
    lon_diff = max_lon - min_lon
    max_diff = max(lat_diff, lon_diff)

    # Determine zoom level: smaller max_diff means a higher zoom level
    if max_diff < 0.01:
        zoom_level = 13
    elif max_diff < 0.1:
        zoom_level = 11
    elif max_diff < 1:
        zoom_level = 8
    else:
        zoom_level = 6

    # Create a map centered around the calculated center
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_level, tiles='OpenStreetMap')

    # Add the line between the photo locations
    line_coordinates = [(p.latitude, p.longitude) for p in photos]
    folium.PolyLine(line_coordinates, color="red", weight=5, opacity=0.8).add_to(m)

    # for p in photos:
    #     folium.Marker(location=[p.latitude, p.longitude], popup=p.title).add_to(m)

    # Save the map to an HTML file
    m.save(MAP_FILENAME)


def main():
    parser = argparse.ArgumentParser(description="Extract photos within a date range.")
    parser.add_argument('--start-date', type=str, required=True, help='Start date in YYYY-MM-DD format')
    parser.add_argument('--end-date', type=str, required=True, help='End date in YYYY-MM-DD format')
    args = parser.parse_args()

    # Convert start_date and end_date to timezone-aware datetime objects
    local_tz = pytz.timezone("America/Toronto")  # Replace with your local timezone
    start_date = local_tz.localize(datetime.strptime(args.start_date, "%Y-%m-%d"))
    end_date = local_tz.localize(datetime.strptime(args.end_date, "%Y-%m-%d"))

    photos = get_desired_photos(start_date, end_date)
    
    # for p in photos:
    #     formatted_date = p.date.strftime("%Y-%m-%d-%H:%M")
    #     print(f"{formatted_date}, {p.place.address.city},{p.place.country_code}, {p.latitude}, {p.longitude}")

    print(f"Found {len(photos)} photos")

    generate_geojson(photos)
    generate_json(photos)
 
    build_map(photos)


if __name__ == "__main__":
    main()
