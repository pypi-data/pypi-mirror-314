import copernicusmarine
from pymongo import MongoClient

# MongoDB Configuration
client = MongoClient("mongodb+srv://admin:admin@cluster0.ykmd9.mongodb.net/")  # Replace with your MongoDB URI
db = client["copernicus_data"]  # Replace with your database name
collection = db["downloads"]  # Replace with your collection name

# Backup the original subset function
original_subset = copernicusmarine.subset

def subset_with_mongodb_check(**kwargs):
    # Construct the query for MongoDB
    query = {
        "dataset_id": kwargs.get("dataset_id"),
        "variables": kwargs.get("variables"),
        "longitude_range": {
            "min": kwargs.get("minimum_longitude"),
            "max": kwargs.get("maximum_longitude"),
        },
        "latitude_range": {
            "min": kwargs.get("minimum_latitude"),
            "max": kwargs.get("maximum_latitude"),
        },
        "datetime_range": {
            "start": kwargs.get("start_datetime"),
            "end": kwargs.get("end_datetime"),
        },
        "depth_range": {
            "min": kwargs.get("minimum_depth"),
            "max": kwargs.get("maximum_depth"),
        },
    }

    # Check if the query already exists in the database
    existing_entry = collection.find_one(query)

    if existing_entry:
        print("Duplicate request found in MongoDB. Request rejected.")
        return

    print("No duplicate found in MongoDB. Proceeding with the download...")

    # Call the original copernicusmarine.subset function
    original_subset(**kwargs)

    # Save the metadata to MongoDB after a successful download
    collection.insert_one(query)
    print("Request parameters saved to MongoDB.")

# Override the copernicusmarine.subset function
copernicusmarine.subset = subset_with_mongodb_check