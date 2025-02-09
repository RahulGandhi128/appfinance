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
from selenium.webdriver.chrome.options import Options


st.set_page_config(layout="wide")

# Define the company list and links manually
COMPANY_DATA = [
    ["Reliance Industr", "/company/RELIANCE/consolidated/"],
    ["TCS", "/company/TCS/consolidated/"],
    ["HDFC Bank", "/company/HDFCBANK/consolidated/"],
    ["Bharti Airtel", "/company/BHARTIARTL/consolidated/"],
    ["ICICI Bank", "/company/ICICIBANK/consolidated/"],
    ["Infosys", "/company/INFY/consolidated/"],
    ["St Bk of India", "/company/SBIN/consolidated/"],
    ["Life Insurance", "/company/LICI/consolidated/"],
    ["Hind. Unilever", "/company/HINDUNILVR/consolidated/"],
    ["ITC", "/company/ITC/consolidated/"],
    ["Larsen & Toubro", "/company/LT/consolidated/"],
    ["HCL Technologies", "/company/HCLTECH/consolidated/"],
    ["Sun Pharma.Inds.", "/company/SUNPHARMA/consolidated/"],
    ["Bajaj Finance", "/company/BAJFINANCE/consolidated/"],
    ["O N G C", "/company/ONGC/consolidated/"],
    ["Tata Motors", "/company/TATAMOTORS/consolidated/"],
    ["NTPC", "/company/NTPC/consolidated/"],
    ["Maruti Suzuki", "/company/MARUTI/consolidated/"],
    ["Kotak Mah. Bank", "/company/KOTAKBANK/consolidated/"],
    ["Axis Bank", "/company/AXISBANK/consolidated/"],
    ["Adani Enterp.", "/company/ADANIENT/consolidated/"],
    ["M & M", "/company/M&M/consolidated/"],
    ["Coal India", "/company/COALINDIA/consolidated/"],
    ["UltraTech Cem.", "/company/ULTRACEMCO/consolidated/"],
    ["Hind.Aeronautics", "/company/HAL/"],
    ["Adani Ports", "/company/ADANIPORTS/consolidated/"],
    ["Avenue Super.", "/company/DMART/consolidated/"],
    ["Titan Company", "/company/TITAN/consolidated/"],
    ["Power Grid Corpn", "/company/POWERGRID/consolidated/"],
    ["Asian Paints", "/company/ASIANPAINT/consolidated/"],
    ["Adani Green", "/company/ADANIGREEN/consolidated/"],
    ["Bajaj Auto", "/company/BAJAJ-AUTO/consolidated/"],
    ["Wipro", "/company/WIPRO/consolidated/"],
    ["Bajaj Finserv", "/company/BAJAJFINSV/consolidated/"],
    ["Adani Power", "/company/ADANIPOWER/consolidated/"],
    ["Siemens", "/company/SIEMENS/"],
    ["Trent", "/company/TRENT/consolidated/"],
    ["I O C L", "/company/IOC/consolidated/"],
    ["Nestle India", "/company/NESTLEIND/"],
    ["I R F C", "/company/IRFC/"],
    ["Zomato Ltd", "/company/ZOMATO/consolidated/"],
    ["JSW Steel", "/company/JSWSTEEL/consolidated/"],
    ["Bharat Electron", "/company/BEL/consolidated/"],
    ["Hindustan Zinc", "/company/HINDZINC/"],
    ["DLF", "/company/DLF/consolidated/"],
    ["Jio Financial", "/company/JIOFIN/consolidated/"],
    ["Varun Beverages", "/company/VBL/consolidated/"],
    ["Tata Steel", "/company/TATASTEEL/consolidated/"],
    ["Grasim Inds", "/company/GRASIM/consolidated/"],
    ["Interglobe Aviat", "/company/INDIGO/"]
]

df_links = pd.DataFrame(COMPANY_DATA, columns=['Company Name', 'Link'])

def scrape_table(url):
    """Scrapes financial table using Selenium (Headless mode)."""
    options = Options()
    options.add_argument("--headless")  # Run without UI
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Avoid memory issues

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(5)  # Allow content to load

        headers = [header.text.strip() for header in driver.find_elements(By.XPATH, '//table/thead/tr/th')]
        rows = driver.find_elements(By.XPATH, '//table/tbody/tr')

        data = [[cell.text.strip() for cell in row.find_elements(By.TAG_NAME, 'td')] for row in rows]
        return pd.DataFrame(data, columns=headers)

    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

    finally:
        driver.quit()  # Always close driver

def get_income_statement(url):
    """Scrapes the income statement using BeautifulSoup (Fallback for Selenium)."""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.select_one('section:nth-of-type(5) > div:nth-of-type(3) > table')
        if not table:
            return None

        headers = [th.text.strip() for th in table.select_one('thead > tr').find_all('th')]
        data = [[td.text.strip() for td in row.find_all('td')] for row in table.select('tbody > tr')]
        return pd.DataFrame(data, columns=headers)

    except Exception as e:
        st.error(f"Error fetching income statement: {e}")
        return None

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

def classify_stocks_inplace(scrape_table_df):
    """Adds a 'Classification' column to the DataFrame."""
    if not isinstance(scrape_table_df, pd.DataFrame) or scrape_table_df.empty:
        return

    scrape_table_df["P/E"] = pd.to_numeric(scrape_table_df["P/E"], errors="coerce")
    pe_median = scrape_table_df["P/E"].median()
    scrape_table_df["Div Yld %"] = pd.to_numeric(scrape_table_df["Div Yld %"], errors="coerce")
    div_yield_median = scrape_table_df["Div Yld %"].median()

    def classify_row(row):
        if pd.isna(row["P/E"]) or pd.isna(row["Div Yld %"]):
            return None
        if row["P/E"] > pe_median and row["Div Yld %"] < div_yield_median:
            return f"{row['Name']} → Growth Stock"
        elif row["P/E"] < pe_median and row["Div Yld %"] > div_yield_median:
            return f"{row['Name']} → Value Stock"
        return None

    scrape_table_df["Classification"] = scrape_table_df.apply(classify_row, axis=1)

# Streamlit App UI
st.title("Financial Data Scraper & Analysis")

company_name = st.selectbox("Select a Company", df_links['Company Name'])

if st.button("Fetch Data"):
    company_link = df_links[df_links['Company Name'] == company_name]['Link'].values[0]
    full_url = "https://www.screener.in" + company_link

    # Scrape Income Statement
    income_statement_df = get_income_statement(full_url)
    if isinstance(income_statement_df, pd.DataFrame):
        st.subheader("Income Statement")
        st.dataframe(income_statement_df)

    # Scrape Financial Table using Selenium
    scrape_table_df = scrape_table(full_url)
    if isinstance(scrape_table_df, pd.DataFrame):
        classify_stocks_inplace(scrape_table_df)
        st.subheader("Sector Analysis")
        st.dataframe(scrape_table_df)

        column_name = 'P/E' if 'P/E' in scrape_table_df.columns else scrape_table_df.columns[0]
        pe, price = pd.to_numeric(scrape_table_df.iloc[0, 3], errors='coerce'), pd.to_numeric(scrape_table_df.iloc[0, 2], errors='coerce')

        statistics = calculate_statistics(scrape_table_df, column_name)
        adjusted_statistics = calculate_adjusted_statistics(scrape_table_df, column_name, price, pe)

        st.subheader("Statistics Of P/E Ratio")
        st.write(statistics)

        st.subheader("Price at Different P/E Ratios")
        st.write(adjusted_statistics)

        st.write(f"Current price: {price}")
        
st.markdown(
    """
    <style>
    /* Make DataFrame wider */
    .css-1d391kg { width: 100% !important; }

    /* Change ALL headings, subheadings, and normal text to yellow */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #FFD700 !important; /* Bright Yellow */
    }

    /* Improve table readability */
    table {
        width: 100% !important;
        border-collapse: collapse;
    }

    th, td {
        padding: 10px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }

    th {
        background-color: #4CAF50;
        color: white;
    }

    /* Reduce padding in sidebar */
    .css-1aumxhk {
        padding-top: 0px !important;
    }

    /* Make buttons larger */
    .stButton>button {
        font-size: 18px !important;
        border-radius: 8px;
        padding: 10px 20px;
        background-color: #000000; /* Black */
        color: #FFD700; /* Yellow */
        border: none;
    }

    .stButton>button:hover {
        background-color: #333333; /* Dark Gray */
    }

    /* Make background completely black */
    .stApp {
        background-color: #000000 !important; /* Black */
    }

    /* Ensure all section headers are yellow */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #FFD700 !important; /* Bright Yellow */
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div style="background-color:#000000;padding:10px;border-radius:10px;">'
    '<h2 style="color:#FFD700;text-align:center;">Sector Classification</h2>'
    '</div>',
    unsafe_allow_html=True
)
