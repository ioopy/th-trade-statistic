import json
import csv
import os
import streamlit as st

def create_region_file(json_file_path, csv_file_path, countries_json_path, year):
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

        # Separate records into main and summary rows
        main_records = [record for record in data if record.get("RowType") != "S"]
        summary_records = [record for record in data if record.get("RowType") == "S"]

        # Add the "Region" field and map country_id to Code2 for main records
        for record in main_records:
            record["Region"] = country_code_map.get(record.get("country_id", ""), "")

        # Sort main records by ID and country_id
        main_records.sort(key=lambda x: (x.get("country_id", ""), x.get("month_id", ""), x.get("ID", "")))

        # Add the "Region" field for summary records
        for record in summary_records:
            record["Region"] = country_code_map.get(record.get("country_id", ""), "")

        # Create the CSV file
        with open(csv_file_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
            # Define column headers
            headers = ["Month", "Year", "Region", "HS Code", "Title", "Quantity", "Value", "Accu Quantity", "Accu Value", "Share"]
            
            # Create CSV writer
            writer = csv.DictWriter(csv_file, fieldnames=headers)

            # Write the header
            writer.writeheader()

            # Write the main data rows with mapped fields
            for record in main_records:
                writer.writerow({
                    "Month": record.get("month_name", ""),
                    "Year": year,
                    "Region": record.get("Region", ""),
                    "HS Code": f"'{str(record.get('ID', ''))}",
                    "Title": record.get("ProductName", ""),
                    "Quantity": record.get("QuantityMonth", ""),
                    "Value": record.get("ValueMonth", ""),
                    "Accu Quantity": record.get("Quantity", ""),
                    "Accu Value": record.get("Value", ""),
                    "Share": record.get("Share", ""),
                })

            # Append the summary rows at the end
            for record in summary_records:
                writer.writerow({
                    "Month": record.get("month_name", ""),
                    "Year": year,
                    "Region": record.get("Region", ""),
                    "HS Code": f"{str(record.get('ID', ''))}",
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


def create_countries_file(json_file_path, csv_file_path, countries_json_path, year):
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

        # Separate records into two lists: `main_records` and `summary_records`
        main_records = [record for record in data if record.get("RowType") != "S"]
        summary_records = [record for record in data if record.get("RowType") == "S"]

        # Add the "Region" field and map country_id to Code2 for main records
        for record in main_records:
            record["Region"] = country_code_map.get(record.get("country_id", ""), "")

        # Sort main records by ID and country_id
        main_records.sort(key=lambda x: (x.get("country_id", ""), x.get("month_id", ""), x.get("ID", "")))

        # Add the "Region" field for summary records
        for record in summary_records:
            record["Region"] = country_code_map.get(record.get("country_id", ""), "")

        # Create the CSV file
        with open(csv_file_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
            # Define column headers
            headers = ["Month", "Year", "Country", "Im/Ex", "HS Code", "Title", "AgriQuantity", "AgriValue", "Sum AgriQuantity", "Sum AgriValue", "Share"]
            
            # Create CSV writer
            writer = csv.DictWriter(csv_file, fieldnames=headers)

            # Write the header
            writer.writeheader()

            # Write the main data rows with mapped fields
            for record in main_records:
                writer.writerow({
                    "Month": record.get("month_name", ""),
                    "Year": year,
                    "Country": record.get("Region", ""),
                    "Im/Ex": 'Export',
                    "HS Code": f"'{str(record.get('ID', ''))}",  # Ensure HS Code is treated as a string
                    "Title": record.get("ProductName", ""),
                    "AgriQuantity": record.get("QuantityMonth", ""),
                    "AgriValue": record.get("ValueMonth", ""),
                    "Sum AgriQuantity": record.get("Quantity", ""),
                    "Sum AgriValue": record.get("Value", ""),
                    "Share": record.get("Share", ""),
                })

            # Append the summary rows at the end
            for record in summary_records:
                writer.writerow({
                    "Month": record.get("month_name", ""),
                    "Year": year,
                    "Country": record.get("Region", ""),
                    "Im/Ex": 'Export',
                    "HS Code": f"{str(record.get('ID', ''))}",  # Ensure HS Code is treated as a string
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

def create_e03_countries_file(json_file_path, csv_file_path, countries_json_path, month, year, currency):
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

        # Separate records into two lists: `main_records` and `summary_records`
        main_records = [record for record in data if record.get("RowType") != "S"]
        summary_records = [record for record in data if record.get("RowType") == "S"]

        # Add the "Region" field and map country_id to Code2 for main records
        for record in main_records:
            record["Region"] = country_code_map.get(record.get("country_id", ""), "")

        # Sort main records by ID and country_id
        main_records.sort(key=lambda x: (x.get("country_id", ""), x.get("comcode", ""), x.get("Value0Month", "")), reverse=True)

        # Add the "Region" field for summary records
        for record in summary_records:
            record["Region"] = country_code_map.get(record.get("country_id", ""), "")


        # Create the CSV file
        with open(csv_file_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
            # Define column headers
            headers = ["Country", "Year", "Category", "Product",
                       f"Value {int(year) - 4} {currency}", f"Value {int(year) -3} {currency}", f"Value {int(year) - 2} {currency}", f"Value {int(year) - 1} {currency}", f"Value {int(year)} {currency}", 
                       f"{int(year) - 3}%", f"{int(year) - 2}%", f"{int(year) - 1}%", f"{int(year)}%", 
                       f"Ratio {int(year) - 3}", f"Ratio {int(year) - 2}", f"Ratio {int(year) - 1}", f"Ratio {int(year)}"]
            # Create CSV writer
            writer = csv.DictWriter(csv_file, fieldnames=headers)

            # Write the header
            writer.writeheader()

            # Write the main data rows with mapped fields
            for record in main_records:
                writer.writerow({
                    "Country": record.get("Region", ""),
                    "Year": year,
                    "Category": record.get("comcode", "")[10:],  # Ensure 'Category' is retrieved correctly
                    "Product": record.get("ProductName", ""),
                    f"Value {int(year) - 4} {currency}": record.get("Value4", ""),
                    f"Value {int(year) - 3} {currency}": record.get("Value3", ""),
                    f"Value {int(year) - 2} {currency}": record.get("Value2", ""),
                    f"Value {int(year) - 1} {currency}": record.get("Value1", ""),
                    f"Value {int(year)} {currency}": record.get("Value0Month", ""),
                    f"{int(year) - 3}%": record.get(f"Growth3", ""),
                    f"{int(year) - 2}%": record.get(f"Growth2", ""),
                    f"{int(year) - 1}%": record.get(f"Growth1", ""),
                    f"{int(year)}%": record.get(f"Growth0Month", ""),
                    f"Ratio {int(year) - 3}": record.get(f"Share3", ""),
                    f"Ratio {int(year) - 2}": record.get(f"Share2", ""),
                    f"Ratio {int(year) - 1}": record.get(f"Share1", ""),
                    f"Ratio {int(year)}": record.get(f"Share0Month", ""),
                })

        print(f"CSV file created successfully at: {csv_file_path}")
        return True
    except Exception as e:
        st.error(f"An error occurred while creating the CSV file: {e}")
        return False

def create_e03_month_countries_file(json_file_path, csv_file_path, countries_json_path, year, start_month, end_month, currency, lang="th"):
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

        # Separate records into two lists: `main_records` and `summary_records`
        main_records = [record for record in data if record.get("RowType") != "S"]
        summary_records = [record for record in data if record.get("RowType") == "S"]

        # Add the "Region" field and map country_id to Code2 for main records
        for record in main_records:
            record["Region"] = country_code_map.get(record.get("country_id", ""), "")

        # Sort main records by ID and country_id
        main_records.sort(key=lambda x: (x.get("country_id", ""), x.get("comcode", "")), reverse=True)

        # Add the "Region" field for summary records
        for record in summary_records:
            record["Region"] = country_code_map.get(record.get("country_id", ""), "")


        # Create the CSV file
        with open(csv_file_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
            months = [
                {"id": i + 1, "text": name_th if lang == "th" else name}
                for i, (name, name_th) in enumerate(
                    zip(
                        ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                        ["ม.ค", "ก.พ", "มี.ค", "เม.ย", "พ.ค", "มิ.ย", "ก.ค", "ส.ค", "ก.ย", "ต.ค", "พ.ย", "ธ.ค"],
                    )
                )
            ]
            # Define column headers
            static_headers = ["Country", "Year", "Category", "Product"]
            
            selected_months = [month["text"] for month in months if start_month <= month["id"] <= end_month]

            value_headers = [f"Value {month}. {year} {currency}" for month in selected_months]
            growth_headers = [f"{month}. {year} %" for month in selected_months]
            share_headers = [f"Ratio {month}. {year}" for month in selected_months]

            headers = static_headers + value_headers + growth_headers + share_headers
            # Create CSV writer
            writer = csv.DictWriter(csv_file, fieldnames=headers)

            # Write the header
            writer.writeheader()

            # Write the main data rows with mapped fields
            for record in main_records:
                row = {
                    "Country": record.get("Region", ""),
                    "Year": year,
                    "Category": record.get("comcode", "")[10:],  # Extract Category from comcode
                    "Product": record.get("ProductName", ""),
                }

                # Add dynamic values for each selected month
                for idx, month in enumerate(selected_months, start=start_month):
                    value_key = f"Value{idx}"  # Example: Value1Month, Value2Month, ...
                    growth_key = f"Growth{idx}"
                    share_key = f"Share{idx}"

                    row[f"Value {month}. {year} {currency}"] = record.get(value_key, "")
                    row[f"{month}. {year} %"] = record.get(growth_key, "")
                    row[f"Ratio {month}. {year}"] = record.get(share_key, "")

                # Write the row to the CSV file
                writer.writerow(row)



        print(f"CSV file created successfully at: {csv_file_path}")
        return True
    except Exception as e:
        st.error(f"An error occurred while creating the CSV file: {e}")
        return False