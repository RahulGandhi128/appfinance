import streamlit as st
import pandas as pd

# Import necessary functions
from functions1 import (
    function_1, function_2, function_3, function_4, function_5, function_6,
    function_7, process_company_data
)

# Streamlit App
st.title("Financial Data Scraping and Analysis")

# Select Functionality
st.sidebar.title("Select Functionality")
selected_function = st.sidebar.selectbox(
    "Choose a function to run:",
    [
        "Scrape Nifty50 Data",
        "Scrape Company Names and Links",
        "Get Company Link",
        "Scrape Quarterly P&L",
        "Scrape Income Statement",
        "Scrape Balance Sheet",
        "Scrape Cash Flow Statement",
        "Process Company Data"
    ]
)

def safe_run_function(func, *args):
    try:
        result = func(*args)
        st.write(result)
    except Exception as e:
        st.error(f"Error running {func.__name__}: {e}")

# Run the selected function
if selected_function == "Scrape Nifty50 Data":
    st.header("Nifty50 Data")
    safe_run_function(function_1)

elif selected_function == "Scrape Company Names and Links":
    st.header("Company Names and Links")
    safe_run_function(function_2)

elif selected_function == "Get Company Link":
    st.header("Get Company Link")
    company_name = st.text_input("Enter Company Name:")
    if company_name:
        df_links = function_2()  # You need df_links to use this function
        safe_run_function(function_3, company_name, df_links)

elif selected_function == "Scrape Quarterly P&L":
    st.header("Scrape Quarterly P&L")
    company_link = st.text_input("Enter Company Link:")
    if company_link:
        safe_run_function(function_4, company_link)

elif selected_function == "Scrape Income Statement":
    st.header("Scrape Income Statement")
    company_link = st.text_input("Enter Company Link:")
    if company_link:
        safe_run_function(function_5, company_link)

elif selected_function == "Scrape Balance Sheet":
    st.header("Scrape Balance Sheet")
    company_link = st.text_input("Enter Company Link:")
    if company_link:
        safe_run_function(function_6, company_link)

elif selected_function == "Scrape Cash Flow Statement":
    st.header("Scrape Cash Flow Statement")
    company_link = st.text_input("Enter Company Link:")
    if company_link:
        safe_run_function(function_7, company_link)

elif selected_function == "Process Company Data":
    st.header("Process Company Data")
    company_name = st.text_input("Enter Company Name:")
    if company_name:
        df_links = function_2()
        safe_run_function(process_company_data, company_name)

# Additional functionalities or outputs can be added as per your requirement
