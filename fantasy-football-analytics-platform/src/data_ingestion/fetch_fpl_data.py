import requests
import json
import os
from datetime import datetime
import boto3

# === CONFIG ===
FPL_API_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
NOW = datetime.now().strftime("%Y-%m-%d")
LOCAL_FILE = f"data/raw/fpl_data_{NOW}.json"

UPLOAD_TO_S3 = True
S3_BUCKET = "fantasy-fpl-thomas-bucket"
S3_KEY = f"raw/fpl_data_{NOW}.json"

def fetch_fpl_data():
    print("Fetching data from FPL API...")
    response = requests.get(FPL_API_URL)
    response.raise_for_status()
    data = response.json()

    os.makedirs(os.path.dirname(LOCAL_FILE), exist_ok=True)
    with open(LOCAL_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to: {LOCAL_FILE}")

    if UPLOAD_TO_S3:
        print("Uploading file to S3...")
        s3 = boto3.client("s3")
        s3.upload_file(LOCAL_FILE, S3_BUCKET, S3_KEY)
        print(f"File uploaded to: s3://{S3_BUCKET}/{S3_KEY}")

if __name__ == "__main__":
    fetch_fpl_data()
