# from osxphotos import PhotoInfo
import osxphotos
# import folium
import argparse
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Extract photos within a date range.")
    parser.add_argument('--start-date', type=str, required=True, help='Start date in YYYY-MM-DD format')
    parser.add_argument('--end-date', type=str, required=True, help='End date in YYYY-MM-DD format')
    args = parser.parse_args()

    # Convert start_date and end_date to offset-naive datetime objects
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d").replace(tzinfo=None)
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d").replace(tzinfo=None)

    # start working on the photos
    photosdb = osxphotos.PhotosDB()
    
    photos = photosdb.photos()
    print(len(photos))

    for p in photos:
        if start_date <= p.date.replace(tzinfo=None) <= end_date:
            print(f"{p.date}, {p.title}, {p.keywords}, {p.persons}, {p.latitude}, {p.longitude}")

    # photos = [p for p in photosdb.photos if p.date >= args.start_date and p.date <= args.end_date]
    # # photos = sorted([p for p in photos if p.selfie], key=lambda p: p.date)

    # # create a map
    # m = folium.Map(location=[45.5236, -122.6750], zoom_start=15)

    # # add the photos to the map
    # for photo in photos:
    #     folium.Marker(location=[photo.latitude, photo.longitude], popup=photo.title).add_to(m)

    # # save the map to an HTML file
    # m.save("map.html")

if __name__ == "__main__":
    main()
