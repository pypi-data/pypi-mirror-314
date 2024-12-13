import sys
import os
import re
import requests
from pymongo import MongoClient

# MongoDB Configuration
client = MongoClient("mongodb+srv://admin:admin@cluster0.ykmd9.mongodb.net/")  # Replace with your MongoDB URI
db = client["wget_data"]  # Replace with your database name
collection = db["downloads"]  # Replace with your collection name

def check_duplicate(url):
    # Check if the URL already exists in the database
    return collection.find_one({"url": url}) is not None

def save_to_mongodb(url, user_name):
    # Save the URL and user name to MongoDB
    collection.insert_one({"url": url, "user_name": user_name})
    print(f"URL saved to MongoDB for user {user_name}.")

def extract_url_from_command():
    # Extract the URL from the command-line arguments
    url = None
    for i, arg in enumerate(sys.argv):
        if arg.startswith('http'):  # A basic check for the URL
            url = arg
            break
    return url

def main():
    url = extract_url_from_command()
    if not url:
        print("Error: No URL found in the command.")
        return

    # Check for duplicates
    if check_duplicate(url):
        print("Duplicate URL found in the database. Skipping download.")
        print("Already downloaded by user: " , collection.find_one({"url": url})["user_name"])
        return

    # Ask for the user's name
    user_name = input("Please enter your name: ")
    os.system(f"wget -e robots=off --mirror --no-parent -r {url}")
    # After successful download, save the URL and user name to MongoDB
    save_to_mongodb(url, user_name)

if __name__ == "__main__":
    main()
