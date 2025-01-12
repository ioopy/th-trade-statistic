import streamlit as st
from datetime import datetime
import json
from utils.fetch_data import fetch
from utils.exporter import create_region_file, create_countries_file
import os

def download_file_button(file_path, button_text):
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            file_data = file.read()
            file_name = os.path.basename(file_path)
            st.download_button(
                label=button_text,
                data=file_data,
                file_name=file_name,
                mime="text/csv"
            )


def load_data(file_path):
    """Load data from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def generate_years(start_year=2000):
    """Generate a list of years from the current year to the start year."""
    current_year = datetime.now().year
    return [{"id": str(year), "text": str(year)} for year in range(current_year, start_year - 1, -1)]

def create_selectbox(label, options, default_index=0):
    """Create a selectbox and return the selected option."""
    selected_value = st.selectbox(label, [opt["text"] for opt in options], index=default_index)
    return next(option for option in options if option["text"] == selected_value)

def create_multiselect(label, options, default_values):
    """Create a multiselect and return the selected options."""
    selected_values = st.multiselect(label, [f"{opt['Code2']} : {opt['nameEn']}" for opt in options], default=default_values)
    return [
        {"id": opt["id"], "text": f"{opt['Code2']} : {opt['nameTh']}"}
        for opt in options
        if f"{opt['Code2']} : {opt['nameEn']}" in selected_values
    ]

def main():
    st.title("Criteria for Export TH Trade statistic Data")

    # Year and Month Selection
    years = generate_years()
    months = [
        {"id": i + 1, "text": name}
        for i, name in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    ]

    col1, col2 = st.columns(2)
    with col1:
        selected_year = create_selectbox("Select Year", years)
    with col2:
        selected_month = create_selectbox("Select Month", months, default_index=datetime.now().month - 1)

    # Currency Selection
    currency = [
        {"id": "baht", "text": "Baht"},
        {"id": "usd", "text": "USD"},
        {"id": "mbaht", "text": "Million Baht"},
        {"id": "musd", "text": "Million USD"},
    ]
    selected_currency = create_selectbox("Select Currency", currency, default_index=1)

    # Country Selection
    countries_json = load_data("data/countries.json")
    default_codes = ["2S", "3O", "AM", "BY", "KG", "KZ", "MD", "RU"]
    default_countries = [
        f"{country['Code2']} : {country['nameEn']}"
        for country in countries_json
        if country["Code2"] in default_codes
    ]
    selected_countries = create_multiselect("Select Country (Multiple Selections Allowed)", countries_json, default_countries)

    # Harmonize Digits Selection
    harmonize_options = [
        {"id": "2", "text": "2 digits"},
        {"id": "4", "text": "4 digits"},
        {"id": "6", "text": "6 digits"},
        {"id": "8", "text": "8 digits"},
        {"id": "11", "text": "11 digits"},
    ]
    selected_harmonize = create_selectbox("Select Harmonize Digits", harmonize_options, default_index=1)

    # HS Code and Order By Selection
    col1, col2 = st.columns(2)
    with col1:
        hs_code = st.text_input("Enter HS Code (max 11 characters)", max_chars=11)
    with col2:
        order_by_options = [
            {"id": "value_desc", "text": "Value (from highest to lowest)"},
            {"id": "value_asc", "text": "Value (from lowest to highest)"},
            {"id": "hscode_desc", "text": "Hscode (from highest to lowest)"},
            {"id": "hscode_asc", "text": "Hscode (from lowest to highest)"},
        ]
        selected_order = create_selectbox("Select Order By", order_by_options, default_index=1)

    # Language Selection
    selected_language = st.radio("Select Language", ["th", "en"], index=1, horizontal=True)

    # Define file paths
    json_file_path = "data/export_region.json"  # Replace with your JSON file path
    csv_file_path = "data/export_region.csv"   # Replace with your desired CSV output path
    json_countries_file_path = "data/export_countries.json"  # Replace with your JSON file path
    csv_countries_file_path = "data/export_countries.csv"   # Replace with your desired CSV output path
    region_json = "data/countries.json"
    countries_json = "data/countries.json"

    # Buttons
    if st.button("Search"):
        payload = {
            "year": selected_year,
            "month": selected_month,
            "currency": selected_currency,
            "hscodedigits": selected_harmonize["id"],
            "hscode": hs_code,
            "sort": selected_order,
            "lang": selected_language
        }

        # Clear old CSV files
        for file_path in [csv_file_path, csv_countries_file_path]:
            if os.path.exists(file_path):
                os.remove(file_path)  # Delete the file

        with st.spinner("Fetching data... Please wait."):
            fetch(payload, selected_countries)
        st.success("Data fetch complete!")

        with st.spinner("Begin create region file... Please wait."):
            is_region_successful = create_region_file(json_file_path, csv_file_path, region_json, selected_month['text'], selected_year['text'])
            if is_region_successful:
                st.success("Create region file complete!")

        with st.spinner("Begin create countries file... Please wait."):
            is_countries_successful = create_countries_file(json_countries_file_path, csv_countries_file_path, countries_json, selected_month['text'], selected_year['text'])
            if is_countries_successful:
                st.success("Create countries file complete!")

    # Add download buttons for the new files
    if os.path.exists(csv_file_path):
        st.download_button(
            label="Download Export Region CSV",
            data=open(csv_file_path, 'rb'),
            file_name="export_region.csv",
            mime="text/csv"
        )

    if os.path.exists(csv_countries_file_path):
        st.download_button(
            label="Download Export Countries CSV",
            data=open(csv_countries_file_path, 'rb'),
            file_name="export_countries.csv",
            mime="text/csv"
        )


if __name__ == "__main__":
    main()
