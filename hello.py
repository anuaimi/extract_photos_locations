import osxphotos
# import folium

def main():
    print("Hello from extract-photos-locations!")
    photosdb = osxphotos.PhotosDB()
    photos = photosdb.photos()

if __name__ == "__main__":
    main()
