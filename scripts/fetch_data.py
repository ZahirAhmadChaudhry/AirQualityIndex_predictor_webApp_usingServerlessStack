import requests
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta

# Load API token from .env file
load_dotenv()
API_TOKEN = os.getenv("WAQI_TOKEN")

def extract_data_point(json_data):
    """Extract relevant fields from a WAQI API data point."""
    if json_data['status'] == 'ok':
        data = json_data['data']
        iaqi = data['iaqi']
        time = data['time']
        forecast = data['forecast']['daily']
        
        data_point = {
            'time': time['s'],
            'pm10': iaqi.get('pm10', {}).get('v'),
            'pm25': iaqi.get('pm25', {}).get('v'),
            'o3': iaqi.get('o3', {}).get('v'),
            'no2': iaqi.get('no2', {}).get('v'),
            'so2': iaqi.get('so2', {}).get('v')
        }
        return data_point
    else:
        print(f"Error: {json_data.get('message', 'Unknown error')}")
        return None

def fetch_and_extract_data(city):
    """Fetch data for a specific city and extract relevant information."""
    url = f"https://api.waqi.info/feed/{city}/?token={API_TOKEN}"
    
    response = requests.get(url)
    if response.ok:
        json_data = response.json()
        return extract_data_point(json_data)
    else:
        print(f"Failed to fetch data for {city}. Status code: {response.status_code}")
        return None

import os

def save_data_to_csv(data_point, filename=None):
    """Save the extracted data into a CSV file."""
    if filename is None:
        script_dir = os.path.dirname(__file__)  # get the directory of the current script
        data_dir = os.path.join(script_dir, '..', 'Data')  # get the Data directory
        filename = os.path.join(data_dir, 'current_air_quality_data.csv')  # get the full path to the CSV file

    if data_point is None:
        print("No data to save.")
        return

    df = pd.DataFrame([data_point])
    if not os.path.isfile(filename):
        df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, mode='a', header=False, index=False)

def main():
    city = 'Saint-Etienne'  # Replace with your city of interest
    print(f"Fetching current data for {city}...")
    data_point = fetch_and_extract_data(city)
    if data_point:
        save_data_to_csv(data_point)
        print(f"Current data for {city} fetched and saved.")
    else:
        print(f"No current data available for {city}.")

if __name__ == "__main__":
    main()