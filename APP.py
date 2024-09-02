import streamlit as st
import pandas as pd

# Import necessary functions
from functions1 import (
    process_company_data, scrape_table, scrape_table_with_links,
    get_quarterly_income_statements, calculate_number_of_shares, 
    calculate_firm_metrics, calculate_adjusted_statistics, calculate_combined_metrics,
    transpose_and_clean_df, clean_and_convert_to_float, calculate_investment_rate,
    set_api_key, configure_genai, function_1, function_2
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
    
    if company_name:
        # Get the links only once
        df_links = function_2() 
        
        # Call the function and capture the full_url
        full_url = process_company_data(company_name, df_links)

        # Ensure full_url is valid before using it in scraping functions
        if full_url:
            df_table = scrape_table(full_url)
            df_links_peers = scrape_table_with_links(full_url)
            st.write(df_table)
            st.write(df_links_peers)
        else:
            st.error("No valid URL found for the company.")

        
# Run functions in the background without displaying their outputs
# Get quarterly income statements based on scraped peer links
quarterly_income_statements = get_quarterly_income_statements(df_links_peers)

# Calculate the number of shares for the company data
df_shares = calculate_number_of_shares(dfp)

# Calculate firm metrics using TTM sales and shares data
TTM_Net_Profit_f1, share_f1, TTM_Sales_f1 = calculate_firm_metrics(ttm_sales_df, df_shares)
# Assume company_name and dfp (processed data) are available from the earlier step
if company_name:
        # Fetch or reuse the previously processed data (assuming it's in dfp, ttm_sales_df)
        # You might need to ensure dfp and ttm_sales_df are generated in the Process Company Data step

    column_name = st.text_input("Enter the column name for adjustment calculations:")

if column_name:
 # Assuming the processed data is stored in dfp and ttm_sales_df
    dfp = pd.DataFrame()  # Placeholder, use actual processed data
    ttm_sales_df = pd.DataFrame()  # Placeholder, use actual TTM sales data
    df_shares = calculate_number_of_shares(dfp)

 # Calculate firm metrics
TTM_Net_Profit_f1, share_f1, _ = calculate_firm_metrics(ttm_sales_df, df_shares)

# Calculate and display adjusted statistics
adjusted_stats = calculate_adjusted_statistics(dfp, column_name, TTM_Net_Profit_f1, share_f1)
st.write(adjusted_stats)
