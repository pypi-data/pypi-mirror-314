import argparse
from pymongo import MongoClient
from datetime import datetime
import copernicusmarine

# Connect to MongoDB
client = MongoClient("mongodb+srv://admin:admin@cluster0.ykmd9.mongodb.net/")  # Replace with your connection string
db = client["copernicus_data"]  # Database name
collection = db["downloads"]  # Collection name

# Function to check for overlap
def is_overlap(range1_min, range1_max, range2_min, range2_max):
    """
    Check if two ranges overlap.
    """
    return not (range1_max < range2_min or range2_max < range1_min)

def variable_overlap(list1, list2):
    # Convert to sets for easier comparison
    set1 = set(list1)
    set2 = set(list2)
    
    # Check if all elements of set1 are in set2
    # And ensure the sets are not exactly the same
    return set1.issubset(set2)

# Function to detect duplicates
def detect_duplicates(data):
    # Find all requests in the database
    existing_requests = collection.find()

    for existing_request in existing_requests:
        # Check if start_datetime is already a datetime object
        # if isinstance(existing_request["start_datetime"], str):
        #     # Convert existing datetime string to datetime object if it's a string
        #     existing_request["start_datetime"] = datetime.fromisoformat(existing_request["start_datetime"])
        # elif not isinstance(existing_request["start_datetime"], datetime):
        #     # Handle any non-string, non-datetime cases
        #     raise TypeError("start_datetime is not a valid type")

        # if isinstance(existing_request["end_datetime"], str):
        #     # Convert existing datetime string to datetime object if it's a string
        #     existing_request["end_datetime"] = datetime.fromisoformat(existing_request["end_datetime"])
        # elif not isinstance(existing_request["end_datetime"], datetime):
        #     # Handle any non-string, non-datetime cases
        #     raise TypeError("end_datetime is not a valid type")

        # if isinstance(existing_request["variable"], str):
        #     # Convert existing variable string to list if it's a string
        #     existing_request["variable"] = existing_request["variable"].split("+")
        # elif not isinstance(existing_request["variable"], list):
        #     # Handle any non-string, non-list cases
        #     raise TypeError("variable is not a valid type")
        
        # Check for overlapping longitude
        longitude_overlap = is_overlap(
            data["minimum_longitude"],
            data["maximum_longitude"],
            existing_request["minimum_longitude"],
            existing_request["maximum_longitude"],
        )

        # Check for overlapping latitude
        latitude_overlap = is_overlap(
            data["minimum_latitude"],
            data["maximum_latitude"],
            existing_request["minimum_latitude"],
            existing_request["maximum_latitude"],
        )

        start = existing_request["start_datetime"]
        if isinstance(start, str):
            start = datetime.fromisoformat(existing_request["start_datetime"])
        end = existing_request["end_datetime"]
        if isinstance(end, str):
            end = datetime.fromisoformat(existing_request["end_datetime"])
        # Check for overlapping date range
        date_overlap = is_overlap(
            datetime.fromisoformat(data["start_datetime"]),
            datetime.fromisoformat(data["end_datetime"]),
            start,
            end,
        )

        # print(date_overlap)
        # print(longitude_overlap)
        # print(latitude_overlap)

        var_list = data["variables"]
        existing_var_list = existing_request["variables"]
        is_subset = variable_overlap(var_list, existing_var_list)

        # print(is_subset)
        # print(var_list)
        # print(existing_var_list)
        # If both date and region overlap, it's a duplicate
        if date_overlap and longitude_overlap and latitude_overlap and is_subset:
            return "Duplicate data found." , existing_request["Name"]

    # No duplicates found
    return "No duplicate data found." , ""

# Function to handle command-line input
def parse_arguments():
    parser = argparse.ArgumentParser(description="Download Copernicus dataset and store in MongoDB.")
    
    # Create a subparser for handling hierarchical commands
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")
    
    # Add the "copernicusmarine" command
    copernicusmarine_parser = subparsers.add_parser("copernicusmarine", help="Copernicus Marine dataset commands")
    
    # Add a subparser under "copernicusmarine" for the "subset" command
    subset_parser = copernicusmarine_parser.add_subparsers(dest="subcommand", required=True)
    subset_cmd = subset_parser.add_parser("subset", help="Subset function from Copernicus Marine API")
    
    # Add arguments for the "subset" command
    subset_cmd.add_argument('--dataset-id', type=str, required=True, help="Dataset ID")
    subset_cmd.add_argument('--variable', type=str, nargs='+', required=True, help="Variable(s) of the dataset")
    subset_cmd.add_argument('--minimum-longitude', type=float, required=True, help="Minimum longitude of the region")
    subset_cmd.add_argument('--maximum-longitude', type=float, required=True, help="Maximum longitude of the region")
    subset_cmd.add_argument('--minimum-latitude', type=float, required=True, help="Minimum latitude of the region")
    subset_cmd.add_argument('--maximum-latitude', type=float, required=True, help="Maximum latitude of the region")
    subset_cmd.add_argument('--start-datetime', type=str, required=True, help="Start datetime (ISO 8601 format)")
    subset_cmd.add_argument('--end-datetime', type=str, required=True, help="End datetime (ISO 8601 format)")
    subset_cmd.add_argument('--minimum-depth', type=float, required=True, help="Minimum depth of the dataset")
    subset_cmd.add_argument('--maximum-depth', type=float, required=True, help="Maximum depth of the dataset")
    
    return parser.parse_args()

def download_dataset(request_data):
    # Example CLI command to download the dataset
    # Modify it according to your actual download mechanism
    copernicusmarine.subset(
        dataset_id=request_data["dataset_id"],
        variables=request_data["variables"],
        minimum_longitude=request_data["minimum_longitude"],
        maximum_longitude=request_data["maximum_longitude"],
        minimum_latitude=request_data["minimum_latitude"],
        maximum_latitude=request_data["maximum_latitude"],
        start_datetime=request_data["start_datetime"],
        end_datetime=request_data["end_datetime"],
        minimum_depth=request_data["minimum_depth"],
        maximum_depth=request_data["maximum_depth"],
    )

# Main program execution
if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_arguments()

    # Check if the subcommand is 'copernicusmarine subset'
    # if args.command == "copernicusmarine" and args.subcommand == "subset":
        # Prepare the request data
    request_data = {
        "source": "copernicusmarine",
        "dataset_id": args.dataset_id,
        "variables": args.variable,
        "minimum_longitude": args.minimum_longitude,
        "maximum_longitude": args.maximum_longitude,
        "minimum_latitude": args.minimum_latitude,
        "maximum_latitude": args.maximum_latitude,
        "start_datetime": args.start_datetime,
        "end_datetime": args.end_datetime,
        "minimum_depth": args.minimum_depth,
        "maximum_depth": args.maximum_depth,
        "Name":""
    }

    # Convert start_datetime and end_datetime to datetime objects
    # request_data["start_datetime"] = datetime.fromisoformat(request_data["start_datetime"])
    # request_data["end_datetime"] = datetime.fromisoformat(request_data["end_datetime"])

    # Check for duplicates
    result, name = detect_duplicates(request_data)
    # print(result)
    # Insert if no duplicate
    if result == "No duplicate data found.":
        Name=input("Enter your name : ")
        download_dataset(request_data)
        print("Did you download the dataset? (0 for no, 1 for yes)")
        download = int(input())
        if(download):
            request_data["Name"]=Name
            collection.insert_one(request_data)
            print("Request stored in the database.")
    else:
        print(result)
        print("\nDuplicate request details:")
        print("File is already downloaded by : ",name)