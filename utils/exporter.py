import json
import csv
import os
import streamlit as st

def create_region_file(json_file_path, csv_file_path, countries_json_path, month, year):
    try:
        # Load the countries data for region mapping
        with open(countries_json_path, 'r', encoding='utf-8') as countries_file:
            countries_data = json.load(countries_file)
        country_code_map = {country["id"]: country.get("Code2", "") for country in countries_data}
        country_code_map["606"] = "EAEU"  # Special mapping for 606
        country_code_map["546"] = "CIS"   # Special mapping for 546

        # Load the JSON data
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # Ensure the data is a list
        if not isinstance(data, list):
            st.error("Invalid JSON structure: Expected a list of records.")
            return

        if not data:
            st.warning(f"Region data not found", icon="⚠️")
            return

        # Add the "Region" field and map country_id to Code2
        for record in data:
            record["Region"] = country_code_map.get(record.get("country_id", ""), "")
        
        # Sort data by ID and country_id
        data.sort(key=lambda x: (x.get("country_id", ""), x.get("ID", "")))

        # Create the CSV file
        with open(csv_file_path, 'w', encoding='utf-8', newline='') as csv_file:
            # Define column headers
            headers = ["Month", "Year", "Region", "HS Code", "Title", "Quantity", "Value", "Accu Quantity", "Accu Value", "Share"]
            
            # Create CSV writer
            writer = csv.DictWriter(csv_file, fieldnames=headers)

            # Write the header
            writer.writeheader()

            # Write the data rows with mapped fields
            for record in data:
                writer.writerow({
                    "Month": month,
                    "Year": year,
                    "Region": record.get("Region", ""),
                    "HS Code": record.get("ID", ""),
                    "Title": record.get("ProductName", ""),
                    "Quantity": record.get("QuantityMonth", ""),
                    "Value": record.get("ValueMonth", ""),
                    "Accu Quantity": record.get("Quantity", ""),
                    "Accu Value": record.get("Value", ""),
                    "Share": record.get("Share", ""),
                })

        print(f"CSV file created successfully at: {csv_file_path}")
        return True
    except Exception as e:
        st.error(f"An error occurred while creating the CSV file: {e}")
        return False


def create_countries_file(json_file_path, csv_file_path, countries_json_path, month, year):
    try:
        # Load the countries data for region mapping
        with open(countries_json_path, 'r', encoding='utf-8') as countries_file:
            countries_data = json.load(countries_file)
        country_code_map = {country["id"]: country.get("Code2", "") for country in countries_data}
        country_code_map["606"] = "EAEU"  # Special mapping for 606
        country_code_map["546"] = "CIS"   # Special mapping for 546

        # Load the JSON data
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # Ensure the data is a list
        if not isinstance(data, list):
            st.error("Invalid JSON structure: Expected a list of records.")
            return

        if not data:
            st.warning(f"Countries data not found", icon="⚠️")
            return
        
        # Add the "Region" field and map country_id to Code2
        for record in data:
            record["Region"] = country_code_map.get(record.get("country_id", ""), "")
        
        # Sort data by ID and country_id
        data.sort(key=lambda x: (x.get("country_id", ""), x.get("ID", "")))

        # Create the CSV file
        with open(csv_file_path, 'w', encoding='utf-8', newline='') as csv_file:
            # Define column headers
            headers = ["Month", "Year", "Country", "Im/Ex", "HS Code", "Title", "AgriQuantity", "AgriValue", "Sum AgriQuantity", "Sum AgriValue", "Share"]
            
            # Create CSV writer
            writer = csv.DictWriter(csv_file, fieldnames=headers)

            # Write the header
            writer.writeheader()

            # Write the data rows with mapped fields
            for record in data:
                writer.writerow({
                    "Month": month,
                    "Year": year,
                    "Country": record.get("Region", ""),
                    "Im/Ex": 'Export',
                    "HS Code": record.get("ID", ""),
                    "Title": record.get("ProductName", ""),
                    "AgriQuantity": record.get("QuantityMonth", ""),
                    "AgriValue": record.get("ValueMonth", ""),
                    "Sum AgriQuantity": record.get("Quantity", ""),
                    "Sum AgriValue": record.get("Value", ""),
                    "Share": record.get("Share", ""),
                })

        print(f"CSV file created successfully at: {csv_file_path}")
        return True
    except Exception as e:
        st.error(f"An error occurred while creating the CSV file: {e}")
        return False
