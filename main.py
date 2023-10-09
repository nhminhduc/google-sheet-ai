import streamlit as st
from core.GoogleSheetPublic import fetch_data

st.title("Google Sheet Data")

data = fetch_data()

st.table(data)
