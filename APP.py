import streamlit as st
import pandas as pd

# Import necessary functions
from functions1 import (
    function_1, function_2, function_3, function_4, function_5, function_6,
    function_7, process_company_data, scrape_table, scrape_table_with_links,
    get_quarterly_income_statements, calculate_number_of_shares, 
    calculate_firm_metrics, calculate_adjusted_statistics, calculate_combined_metrics,
    transpose_and_clean_df, clean_and_convert_to_float, calculate_investment_rate,
    set_api_key, configure_genai
)

# Streamlit App
st.title("Financial Data Scraping and Analysis")

# Inputs
company_name = st.text_input("Enter Company Name:")
company_link = None

if company_name:
    st.write("Running all functions in sequence...")

    # Step 1: Scrape Nifty50 Data
    st.header("Nifty50 Data")
    nifty50_df = function_1()
    st.write(nifty50_df)

    # Step 2: Scrape Company Names and Links
    st.header("Company Names and Links")
    df_links = function_2()
    st.write(df_links)

    # Step 3: Get Company Link
    st.header("Get Company Link")
    company_link = function_3(company_name, df_links)
    st.write(f"Company Link: {company_link}")

    # Step 4: Scrape Quarterly P&L
    if company_link:
        st.header("Scrape Quarterly P&L")
        pnl_df = function_4(company_link)
        st.write(pnl_df)

    # Step 5: Scrape Income Statement
    st.header("Scrape Income Statement")
    if company_link:
        income_df = function_5(company_link)
        st.write(income_df)

    # Step 6: Scrape Balance Sheet
    st.header("Scrape Balance Sheet")
    if company_link:
        balance_df = function_6(company_link)
        st.write(balance_df)

    # Step 7: Scrape Cash Flow Statement
    st.header("Scrape Cash Flow Statement")
    if company_link:
        cash_flow_df = function_7(company_link)
        st.write(cash_flow_df)

    # Step 8: Process Company Data
    st.header("Process Company Data")
    if company_name:
        process_company_data(company_name)
        st.write("Company data processing complete.")

    st.success("All functions have been executed successfully!")
else:
    st.warning("Please enter a company name to proceed.")
