import streamlit as st
import pandas as pd

# Import necessary functions
from functions1 import (
    process_company_data, scrape_table, scrape_table_with_links,
    get_quarterly_income_statements, calculate_number_of_shares, 
    calculate_firm_metrics, calculate_adjusted_statistics, calculate_combined_metrics,
    transpose_and_clean_df, clean_and_convert_to_float, calculate_investment_rate,
    set_api_key, configure_genai
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
        "Process Company Data"
    ]
)

# Run the selected function
if selected_function == "Scrape Nifty50 Data":
    st.header("Nifty50 Data")
    nifty50_df = function_1()
    st.write(nifty50_df)

elif selected_function == "Scrape Company Names and Links":
    st.header("Company Names and Links")
    df_links = function_2()
    st.write(df_links)

elif selected_function == "Process Company Data":
    st.header("Process Company Data")
    company_name = st.text_input("Enter Company Name:")
    if company_name:
        df_links = function_2()  # Fetch the company links only once
        process_company_data(company_name, df_links)
