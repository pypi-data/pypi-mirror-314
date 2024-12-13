# cdsapi_wrapper.py
import cdsapi
from pymongo import MongoClient
from datetime import datetime

# MongoDB Configuration
client = MongoClient("mongodb+srv://admin:admin@cluster0.ykmd9.mongodb.net/")  # Replace with your MongoDB URI
db = client["cds_data"]  # Replace with your database name
collection = db["downloads"]  # Replace with your collection name

# Function to check for overlap
def is_overlap(range1_min, range1_max, range2_min, range2_max):
    return not (range1_max < range2_min or range2_max < range1_min)

def variable_overlap(list1, list2):
    # Convert to sets for easier comparison
    set1 = set(list1)
    set2 = set(list2)
    return set1.issubset(set2) and set1 != set2

# Wrapper function for cdsapi.Client.retrieve
def cdsapi_retrieve_with_check(self, dataset, request):
    # Construct the query for MongoDB
    query = {
        "source": "cds",
        "product_type": request.get("product_type"),
        "variable": request.get("variable"),
        "year": request.get("year"),
        "month": request.get("month"),
        "day": request.get("day"),
        "daily_statistic": request.get("daily_statistic"),
        "time_zone": request.get("time_zone"),
        "frequency": request.get("frequency"),
        "area": request.get("area"),
        "Name": "",
    }

    # Check for overlap with existing requests in the database
    existing_requests = collection.find()
    for existing_request in existing_requests:
        date1_year_list = [int(i) for i in query["year"]]
        date1_month_list = [int(i) for i in query["month"]]
        date1_day_list = [int(i) for i in query["day"]]
        date2_year_list = [int(i) for i in existing_request["year"]]
        date2_month_list = [int(i) for i in existing_request["month"]]
        date2_day_list = [int(i) for i in existing_request["day"]]
        
        date_overlap = 0
        for i in range(len(date1_year_list)):
            for j in range(len(date1_month_list)):
                for k in range(len(date1_day_list)):
                    date1 = datetime(date1_year_list[i], date1_month_list[j], date1_day_list[k])
                    for i1 in range(len(date2_year_list)):
                        for j1 in range(len(date2_month_list)):
                            for k1 in range(len(date2_day_list)):
                                date2 = datetime(date2_year_list[i1], date2_month_list[j1], date2_day_list[k1])
                                if date1 == date2:
                                    date_overlap = 1
                                    break
                            if date_overlap == 1:
                                break
                        if date_overlap == 1:
                            break

        area_overlap = 1
        if existing_request["area"] == '':
            area_overlap = 0
        else:
            if query["area"] == '':
                area_overlap = 0
            else:
                max_lat1 = query["area"][0]
                min_lat1 = query["area"][2]
                max_lon1 = query["area"][1]
                min_lon1 = query["area"][3]

                max_lat2 = existing_request["area"][0]
                min_lat2 = existing_request["area"][2]
                max_lon2 = existing_request["area"][1]
                min_lon2 = existing_request["area"][3]

                area_overlap = is_overlap(min_lat1, max_lat1, min_lat2, max_lat2) and is_overlap(min_lon1, max_lon1, min_lon2, max_lon2)

        var_overlap = variable_overlap(request.get("variable"), existing_request["variable"])

        if date_overlap and var_overlap and existing_request["product_type"] == request.get("product_type") and area_overlap:
            print("Duplicate request found in MongoDB. Skipping download.")
            print("Already downloaded by:", existing_request["Name"])
            return

    print("No duplicate found in MongoDB. Proceeding with the download...")
    Name = input("Enter your name: ")
    query["Name"] = Name

    # Call the original cdsapi retrieve method
    self.retrieve(dataset, request).download()

    # Save the metadata to MongoDB after a successful download
    collection.insert_one(query)
    print("Request parameters saved to MongoDB.")

# Override the cdsapi.Client.retrieve method
cdsapi.Client.retrieve = cdsapi_retrieve_with_check
