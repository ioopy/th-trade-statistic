from menu import menu_with_redirect
import streamlit as st
from datetime import datetime
import json
from utils.fetch_data import fetch_export03, fetch_years
from utils.exporter import create_e03_countries_file, create_e03_month_countries_file
import os

from utils.func import hide_header_icons

st.set_page_config(page_title="Comcode Export")
menu_with_redirect()
hide_header_icons()


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

def generate_years(start_year=2000, selected_language="en"):
    current_year = datetime.now().year
    return [
        {"id": str(year), "text": str(year + 543) if selected_language == "th" else str(year)}
        for year in range(current_year, start_year - 1, -1)
    ]

def create_selectbox(label, options, default_index=0, selected_language="en"):
    selected_value = st.selectbox(label, [opt["text"] for opt in options], index=default_index)
    return next(option for option in options if option["text"] == selected_value)


def create_multiselect(label, options, default_values, selected_language="en"):
    selected_values = st.multiselect(
        label,
        [f"{opt['Code2']} : {opt['name' + selected_language]}" for opt in options],
        default=default_values
    )
    return [
        {"id": opt["id"], "text": f"{opt['Code2']} : {opt['name' + selected_language]}"}
        for opt in options
        if f"{opt['Code2']} : {opt['name' + selected_language]}" in selected_values
    ]

def create_multiselect2(label, options, default_values):
    """Create a multiselect and return the selected options."""
    selected_values = st.multiselect(label, [f"{opt['text']}" for opt in options], default=default_values)
    return [
        {"id": opt["id"], "text": f"{opt['text']}"}
        for opt in options
        if f"{opt['text']}" in selected_values
    ]

def main():
    st.title("สินค้าส่งออกสำคัญของไทยรายประเทศ")

    # Language Selection
    selected_language = st.radio("Select Language", ["th", "en"], index=0, horizontal=True)

    # Year and Month Selection
    year_api_url = "https://tradereport.moc.go.th/lookup/years"
    years = fetch_years(year_api_url, generate_years, selected_language)
    selected_year = create_selectbox("Select Year", years, selected_language=selected_language)

    frequency = [
        {"id": "year", "text": "ปี" if selected_language == "th" else "Year"},
        {"id": "quarter", "text": "ไตรมาส" if selected_language == "th" else "Quarter"},
        {"id": "month", "text": "เดือน" if selected_language == "th" else "Month"},
    ]
    selected_frequency = create_selectbox("Select Frequency", frequency, selected_language=selected_language)

    quarters = [
        {"id": str(i), "text": f"ไตรมาส {i}" if selected_language == "th" else f"Quarter {i}"}
        for i in range(1, 5)
    ]


    months = [
        {"id": i + 1, "text": name_th if selected_language == "th" else name}
        for i, (name, name_th) in enumerate(
            zip(
                ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."],
            )
        )
    ]

    growth = [
        {"id": "Y", "text": "Compared to the previous year"},
        {"id": "M", "text": "Compared to the previous month"}
    ]

    report_type = ""
    selected_quarters = quarters[0]
    if "quarter" in selected_frequency['id']:
        selected_quarters = create_selectbox("Select Quarter", quarters)
        report_type = "quarter"

    is_display_same = []
    if "year" in selected_frequency['id']:
        report_type = "year"
        displaySame = st.checkbox("Show the same period of the previous year.")
        if displaySame:
            is_display_same = ['Y']
        
    selected_start_month = months[0]
    selected_end_month = months[0]
    selected_growth = growth[0]
    if "month" in selected_frequency['id']:
        report_type = "month"
        col1, col2 = st.columns(2)
        with col1:
            selected_start_month = create_selectbox("Select Start Month", months)
        with col2:
            selected_end_month = create_selectbox("Select End Month", months)

        selected_growth = create_selectbox("Select Growth (Value)", growth)

    # Currency Selection
    currency = [
        {"id": "baht", "text": "บาท" if selected_language == "th" else "Baht"},
        {"id": "usd", "text": "ดอลลาร์สหรัฐ" if selected_language == "th" else "USD"},
        {"id": "mbaht", "text": "ล้านบาท" if selected_language == "th" else "Million Baht"},
        {"id": "musd", "text": "ล้านดอลลาร์สหรัฐ" if selected_language == "th" else "Million USD"},
    ]
    selected_currency = create_selectbox("Select Currency", currency, 2, selected_language=selected_language)

    growth_display_type = [
        {"id": "A", "text": "All"},
        {"id": "U", "text": "Increase"},
        {"id": "D", "text": "Reduce"}
    ]
    selected_growth_display_type = create_selectbox("Select Growth", growth_display_type)

    # Country Selection
    countries_json = load_data("data/countries.json")
    default_codes = ["2S", "3O", "AM", "BY", "KG", "KZ", "MD", "RU"]
    lang = "Th" if selected_language == "th" else "En"
    default_countries = [
        f"{country['Code2']} : {country['name' + lang]}"
        for country in countries_json
        if country["Code2"] in default_codes
    ]
    selected_countries = create_multiselect("Select Country (Multiple Selections Allowed)", countries_json, default_countries, selected_language=lang)


    comcode = [
        {"id": "1", "text": "000000000 รวมทั้งสิ้น" if selected_language == "th" else "000000000 Total Exports"},
        {"id": "2", "text": "100000000 สินค้าเกษตรกรรม (กสิกรรม,ปศุสัตว์,ประมง)" if selected_language == "th" else "100000000 Agricultural products"},
        {"id": "636", "text": "200000000 สินค้าอุตสาหกรรมการเกษตร" if selected_language == "th" else "200000000 Agro-industrial products"},
        {"id": "525", "text": "300000000 สินค้าอุตสาหกรรม" if selected_language == "th" else "300000000 Principle manufacturing products"},
        {"id": "122", "text": "400000000 สินค้าแร่และเชื้อเพลิง" if selected_language == "th" else "400000000 Mining and fuel products"},
        {"id": "142", "text": "500000000 อื่น ๆ (ธุรกรรมพิเศษ เช่น ของที่ออกไปกับตน)" if selected_language == "th" else "500000000 Others (special transaction : articles, accompanied with the owner, covered by r"}
    ]
    # selected_comcode = create_selectbox("Select Product", comcode)
    default_codes = ["2", "636"]
    default_comcode = [
        f"{c['text']}"
        for c in comcode
        if c["id"] in default_codes
    ]
    selected_comcode = create_multiselect2("SelSelect Product", comcode, default_comcode)


    default_value = 15
    show_output = st.number_input("Show", value=default_value)
    

    # Define file paths
    json_countries_file_path = f"data/{report_type}_e03_countries.json"  # Replace with your JSON file path
    csv_countries_file_path = f"data/{report_type}_e03_countries.csv"   # Replace with your desired CSV output path
    countries_json = "data/countries.json"

    # Buttons
    if st.button("Search"):
        payload = {
            "year": selected_year,
            "frequency": selected_frequency,
            "quarter": selected_quarters,
            "month": selected_start_month,
            "endmonth": selected_end_month,
            "currency": selected_currency,
            "country": selected_countries,
            "comcode": selected_comcode,
            "limit": {
                "id": show_output,  # Replace with dynamic limit selection
                "text": f"{show_output} Item",  # Adjust dynamically if needed
            },
            "displaySame": is_display_same,  # Adjust dynamically if needed
            "growth": selected_growth,
            "growthDisplayType": selected_growth_display_type,
            "lang": selected_language,
            "sort": {
                "id": "value_desc",
                "text": "มูลค่า (จากมากไปน้อย)"
            },
        }

        # Clear old CSV files
        for file_path in [csv_countries_file_path]:
            if os.path.exists(file_path):
                os.remove(file_path)  

        with st.spinner("Fetching data... Please wait."):
            # st.write(payload)
            fetch_export03(payload, selected_countries, report_type)
        st.success("Data fetch complete!")

        with st.spinner("Begin create countries file... Please wait."):
            year_display = selected_year['id'] if selected_language == "en" else str(int(selected_year['id']) + 543)
            if report_type == "year":
                is_countries_successful = create_e03_countries_file(json_countries_file_path, csv_countries_file_path, countries_json, "", year_display, selected_currency['text'])
            else:
                is_countries_successful = create_e03_month_countries_file(json_countries_file_path, csv_countries_file_path, countries_json, year_display, selected_start_month['id'], selected_end_month['id'], selected_currency['text'], selected_language)
            
            if is_countries_successful:
                st.success("Create countries file complete!")

    if os.path.exists(csv_countries_file_path):
        st.download_button(
            label="Download Export Countries CSV",
            data=open(csv_countries_file_path, 'rb'),
            file_name="export_countries.csv",
            mime="text/csv"
        )


if __name__ == "__main__":
    main()
