import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


# Import necessary functions
from functions1 import (
    process_company_data, scrape_table, scrape_table_with_links,
    get_quarterly_income_statements, calculate_number_of_shares, 
    calculate_firm_metrics, calculate_adjusted_statistics, calculate_combined_metrics,
    transpose_and_clean_df, clean_and_convert_to_float, calculate_investment_rate,
    set_api_key, configure_genai, function_1, function_2, get_company_link
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
        "Process Company Data","Calculate Adjusted Statistics"
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


        
# if full_url:
#     # Scrape the links table before passing it to other functions
#     df_links_peers = scrape_table_with_links(full_url)

#     # Ensure df_links_peers is not None or empty before proceeding
#     if df_links_peers is not None and not df_links_peers.empty:
#         # Now pass df_links_peers to get_quarterly_income_statements
#         quarterly_income_statements = get_quarterly_income_statements(df_links_peers)
#     else:
#         st.error("df_links_peers is not generated or it's empty.")

# # Calculate the number of shares for the company data
# df_shares = calculate_number_of_shares(dfp)

# # Calculate firm metrics using TTM sales and shares data
# TTM_Net_Profit_f1, share_f1, TTM_Sales_f1 = calculate_firm_metrics(ttm_sales_df, df_shares)
# # Assume company_name and dfp (processed data) are available from the earlier step
# if company_name:
#         # Fetch or reuse the previously processed data (assuming it's in dfp, ttm_sales_df)
#         # You might need to ensure dfp and ttm_sales_df are generated in the Process Company Data step

#     column_name = st.text_input("Enter the column name for adjustment calculations:")

# if column_name:
#  # Assuming the processed data is stored in dfp and ttm_sales_df
#     dfp = pd.DataFrame()  # Placeholder, use actual processed data
#     ttm_sales_df = pd.DataFrame()  # Placeholder, use actual TTM sales data
#     df_shares = calculate_number_of_shares(dfp)

#  # Calculate firm metrics
# TTM_Net_Profit_f1, share_f1, _ = calculate_firm_metrics(ttm_sales_df, df_shares)

# # Calculate and display adjusted statistics
# adjusted_stats = calculate_adjusted_statistics(dfp, column_name, TTM_Net_Profit_f1, share_f1)
# st.write(adjusted_stats)
