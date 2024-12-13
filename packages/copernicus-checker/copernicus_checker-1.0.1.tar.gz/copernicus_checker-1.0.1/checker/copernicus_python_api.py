import copernicusmarine
from pymongo import MongoClient
from datetime import datetime

# MongoDB Configuration
client = MongoClient("mongodb+srv://admin:admin@cluster0.ykmd9.mongodb.net/")  # Replace with your MongoDB URI
db = client["copernicus_data"]  # Replace with your database name
collection = db["downloads"]  # Replace with your collection name

# Backup the original subset function
original_subset = copernicusmarine.subset

# Function to normalize datetime string (ensures the format is correct)
def normalize_datetime_string(date_string):
    # Split the datetime string into date and time parts
    date_part, time_part = date_string.split("T")
    
    # Split the date part into year, month, and day
    year, month, day = date_part.split("-")
    
    # Pad month and day with leading zeros if necessary
    month = month.zfill(2)
    day = day.zfill(2)
    
    # Reassemble the datetime string with the correct format
    return f"{year}-{month}-{day}T{time_part}"

# Function to check for overlap
def is_overlap(range1_min, range1_max, range2_min, range2_max):
    return not (range1_max < range2_min or range2_max < range1_min)

def variable_overlap(list1, list2):
    # Convert to sets for easier comparison
    set1 = set(list1)
    set2 = set(list2)
    
    # Check if all elements of set1 are in set2
    # And ensure the sets are not exactly the same
    return set1.issubset(set2)

# Main function to check for duplicate requests and interact with MongoDB
def subset_with_mongodb_check(**kwargs):
    # Normalize the datetime strings to ensure correct formatting
    start_datetime = normalize_datetime_string(kwargs["start_datetime"])
    end_datetime = normalize_datetime_string(kwargs["end_datetime"])

    # Construct the query for MongoDB
    query = {
        "source": "copernicusmarine",
        "dataset_id": kwargs.get("dataset_id"),
        "variables": kwargs.get("variables"),
        "minimum_longitude": kwargs.get("minimum_longitude"),
        "maximum_longitude": kwargs.get("maximum_longitude"),
        "minimum_latitude": kwargs.get("minimum_latitude"),
        "maximum_latitude": kwargs.get("maximum_latitude"),
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "minimum_depth": kwargs.get("minimum_depth"),
        "maximum_depth": kwargs.get("maximum_depth"),
    }

    # Check for overlap with existing requests in the database
    existing_requests = collection.find()
    for existing_request in existing_requests:

        # Check for overlapping longitude
        longitude_overlap = is_overlap(
            kwargs["minimum_longitude"],
            kwargs["maximum_longitude"],
            existing_request["minimum_longitude"],
            existing_request["maximum_longitude"],
        )

        # Check for overlapping latitude
        latitude_overlap = is_overlap(
            kwargs["minimum_latitude"],
            kwargs["maximum_latitude"],
            existing_request["minimum_latitude"],
            existing_request["maximum_latitude"],
        )

        # Check for overlapping date range
        date_overlap = is_overlap(
            datetime.fromisoformat(query["start_datetime"]),
            datetime.fromisoformat(query["end_datetime"]),
            datetime.fromisoformat(existing_request["start_datetime"]),
            datetime.fromisoformat(existing_request["end_datetime"]),
        )

        # Check for overlapping variable list
        var_overlap = variable_overlap(kwargs["variables"], existing_request["variables"])

        # If there's an overlap, reject the request
        if longitude_overlap and latitude_overlap and date_overlap and var_overlap:
            
            print("\nDuplicate request found in MongoDB. Request rejected.\n")
            print("Duplicate request details:")
            print("File is already downloaded by : ",existing_request["Name"])
            return

    print("No duplicate found in MongoDB. Proceeding with the download...")
    Name=input("Enter your name : ")
    query["Name"]=Name
    # Call the original copernicusmarine.subset function
    original_subset(**kwargs)

    # Save the metadata to MongoDB after a successful download
    collection.insert_one(query)
    print("Request parameters saved to MongoDB.")

# Override the copernicusmarine.subset function
copernicusmarine.subset = subset_with_mongodb_check