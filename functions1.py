import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import html
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import numpy as np

# Define URLs
URLS = [
    'https://www.screener.in/screens/261242/nifty-50/?limit=50&page=1',
    'https://www.screener.in/screens/261242/nifty-50/?limit=50&page=2'
]

def scrape_company_links(url):
    """Scrapes company names and their links from Screener."""
    response = requests.get(url)
    tree = html.fromstring(response.content)
    rows = tree.xpath('/html/body/main/div[2]/div[5]/table/tbody/tr[position()>1]')
    data = [(row.xpath('./td[2]/a/text()')[0].strip(), row.xpath('./td[2]/a/@href')[0].strip()) for row in rows]
    return data

def get_company_links():
    """Aggregates company names and links."""
    all_data = []
    for url in URLS:
        all_data.extend(scrape_company_links(url))
    return pd.DataFrame(all_data, columns=['Company Name', 'Link'])

def get_company_link(company_name, df_links):
    """Retrieves the link of a given company."""
    match = df_links[df_links['Company Name'].str.lower() == company_name.lower()]
    return match['Link'].values[0] if not match.empty else None

def scrape_table(url):
    """Scrapes financial table using Selenium."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)
    headers = [header.text.strip() for header in driver.find_elements(By.XPATH, '/html/body/main/section[3]/div[2]/div[3]/table/tbody/tr[1]/th')]
    rows = driver.find_elements(By.XPATH, '/html/body/main/section[3]/div[2]/div[3]/table/tbody/tr')[1:]
    data = [[cell.text.strip() for cell in row.find_elements(By.TAG_NAME, 'td')] for row in rows]
    driver.quit()
    return pd.DataFrame(data, columns=headers)

def get_income_statement(url):
    """Scrapes the income statement."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.select_one('section:nth-of-type(5) > div:nth-of-type(3) > table')
    if not table:
        return None
    headers = [th.text.strip() for th in table.select_one('thead > tr').find_all('th')]
    data = [[td.text.strip() for td in row.find_all('td')] for row in table.select('tbody > tr')]
    return pd.DataFrame(data, columns=headers)

def calculate_statistics(df, column_name):
    """Calculates statistical metrics."""
    column_data = pd.to_numeric(df[column_name], errors='coerce').dropna()
    return {
        'Average': column_data.mean(),
        '25th Percentile': column_data.quantile(0.25),
        '50th Percentile': column_data.median(),
        '75th Percentile': column_data.quantile(0.75),
        '90th Percentile': column_data.quantile(0.90)
    }

def calculate_adjusted_statistics(df, column_name, price, pe):
    """Adjusts statistics based on price and PE."""
    statistics = calculate_statistics(df, column_name)
    price, pe = pd.to_numeric(price, errors='coerce'), pd.to_numeric(pe, errors='coerce')
    return {key: (value * price) / pe for key, value in statistics.items() if np.issubdtype(type(value), np.number)}

# Streamlit App
st.title("Financial Data Scraper & Analysis")
df_links = get_company_links()
company_name = st.text_input("Enter Company Name")

if st.button("Fetch Data"):
    company_link = get_company_link(company_name, df_links)
    if company_link:
        full_url = "https://www.screener.in" + company_link
        
        # Scrape Income Statement
        income_statement_df = get_income_statement(full_url)
        if income_statement_df is not None:
            st.subheader("Income Statement")
            st.dataframe(income_statement_df)
        
        # Scrape Financial Table
        df = scrape_table(full_url)
        st.subheader("Financial Data Table")
        st.dataframe(df)
        
        # Calculate and Display Statistics
        column_name = 'P/E' if 'P/E' in df.columns else df.columns[0]
        pe, price = pd.to_numeric(df.iloc[0, 3], errors='coerce'), pd.to_numeric(df.iloc[0, 2], errors='coerce')
        statistics = calculate_statistics(df, column_name)
        adjusted_statistics = calculate_adjusted_statistics(df, column_name, price, pe)
        
        st.subheader("Statistics")
        st.write(statistics)
        
        st.subheader("Adjusted Statistics")
        st.write(adjusted_statistics)
        
        st.write(f"Current price: {price}")
    else:
        st.error("Company not found.")
