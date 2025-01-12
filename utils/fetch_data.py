import json
import streamlit as st
import requests
import os
from datetime import datetime
import time
import random
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Referer": "https://tradereport.moc.go.th/th/stat/reporthscodeexport02",
        "Cookie": "cookiesession1=678A3E23BE230D32160066805188190E; lhc_per=vid|864c245076ced2ce8f1c; XSRF-TOKEN=eyJpdiI6IkJ0Y1BrdzBMb1lwWXYrdTRHNXV6Q2c9PSIsInZhbHVlIjoiV1pBR1hoeWVwYjZPOXorc1NhT2lVeXUyaWwvT0Y5MDRNajVhRnlFRXI1VTc0TkJ5TmppSld0VXZlOWJYQkR6MW1tQ2x3UVR2Tnp6dGIrOWNOS000SjZGek1FeUFsUmNVaFhYb0ZlTTVndDVucXpseDgyVmJQUUk0SlpkMnJ0anIiLCJtYWMiOiI1ZDc0ZGNiNGY0ZjE3YWZhZjA1MTY0OTRlZjkwNzllNDdmYWU2ZmMyNDBlYTliNTNhOGU1NTc4YmU3ZTk4NTVmIiwidGFnIjoiIn0%3D; thailands_trade_statistic_session=eyJpdiI6IlpkNjNKRWMzUk10dHRZTVg0ZVEyTnc9PSIsInZhbHVlIjoiT1pZSmo4SEk1NmRGZ0c4anhjT1kyZldOYi9zR0xyT3V1WUZsVnlzeDhJZHpnVEhzTm90WVFoTEp1VnFVQk4wMTZaSlNBL2RlT2VZZmlHeFQ5RU5RRnRNeWNOL3J2RlZSOEFKejlUMDRYYy8zUm92d1JwemZBNEZrOUxKTHl3cm8iLCJtYWMiOiJlNTkwNjY3YzljNzE2Mjk0YTk0ZDNlY2Q3N2VhMTQxYzc2MzYwNmQwMmMzZTIxNDQzM2Q4YzA5ODFhNTNlYTY1IiwidGFnIjoiIn0%3D"
    }
API_URL = "https://tradereport.moc.go.th/stat/reporthscodeexport02/result"

def fetch(payload, selected_countries):
    # File paths
    region_file_path = "data/export_region.json"
    countries_file_path = "data/export_countries.json"

    # Initialize the files with an empty JSON array
    for file_path in [region_file_path, countries_file_path]:
        if os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump([], file, ensure_ascii=False)  # Initialize as an empty JSON array

    # Process each selected country
    for country in selected_countries:
        country_id = country["id"]
        country_text = country["text"]

        # Update the country in the payload
        payload["country"] = country

        # Determine file path based on the country ID
        file_path = region_file_path if country_id in ["606", "546"] else countries_file_path

        try:
            # Make the API request
            response = requests.post(API_URL, json=payload, headers=headers, verify=False)
            response.raise_for_status()  # Raise an error for HTTP issues

            # Parse the response
            data = response.json()
            # Validate if records are present
            if "records" in data and data["records"]:  # Check if 'records' key exists and is not empty
                records = data["records"]  # Extract the `records` field

                # Filter records based on the `id` column
                filtered_records = [
                    record for record in records
                    if "ID" in record and (
                        (100 <= int(record["ID"]) <= 2399) or (4001 <= int(record["ID"]) <= 4099)
                    )
                ]

                if not filtered_records:
                    st.warning(f"Data not found for country {country_id} ({country_text}), skipping.", icon="⚠️")
                    continue  # Skip to the next country if no filtered records are found

                # Add the country_id to each filtered record
                for record in filtered_records:
                    record["country_id"] = country_id

                # Read the existing data from the file
                with open(file_path, 'r', encoding='utf-8') as file:
                    existing_data = json.load(file)  # Load the existing JSON array

                # Append the new filtered records to the existing data
                existing_data.extend(filtered_records)

                # Save the updated data back to the file
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(existing_data, file, ensure_ascii=False, indent=4)

                print(f"Filtered records for country {country_id} ({country_text}) saved to {file_path}")
            else:
                st.warning(f"Data not found for country {country_id} ({country_text}), skipping.", icon="⚠️")

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch data for {country_text}: {e}")

        # Add a random sleep time between requests
        sleep_time = random.uniform(1, 5)  # Random sleep between 1 and 5 seconds
        print(f"Sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)
