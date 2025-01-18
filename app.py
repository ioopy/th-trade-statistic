import streamlit as st
import streamlit_authenticator as stauth
from menu import menu
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator.utilities.exceptions import (LoginError)
import os

from utils.func import hide_header_icons 

st.set_page_config(page_title="Trade statistic")

hide_header_icons()

with open('conifg.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Load secrets
usernames = st.secrets["credentials"]["usernames"]
passwords = st.secrets["credentials"]["passwords"]
names = st.secrets["credentials"]["names"]
logged_in = st.secrets["credentials"]["logged_in"]

# Create a dictionary of credentials
credentials = {
    "usernames": {
        usernames[i]: {
            "name": names[i],
            "password": passwords[i],
            "logged_in": logged_in[i]
        } for i in range(len(usernames))
    }
}

# Initialize authenticator
authenticator = stauth.Authenticate(
    credentials, 
    config['cookie']['name'],   
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

print(config['cookie']['name'])

try:
    authenticator.login()
except LoginError as e:
    st.error(e)

if st.session_state["authentication_status"]:
    st.session_state.authenticator = authenticator
    menu(True) 
    csv_file_path = "data/export_region.csv"   # Replace with your desired CSV output path
    csv_countries_file_path = "data/export_countries.csv" 

    for file_path in [csv_file_path, csv_countries_file_path]:
        if os.path.exists(file_path):
            os.remove(file_path) 
    st.switch_page("pages/Ehscode02.py")
elif st.session_state["authentication_status"] is False:
    st.error("Username/password is incorrect")

with open('conifg.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(config, file, default_flow_style=False)