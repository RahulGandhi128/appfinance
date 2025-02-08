import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import html
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# URLs to scrape
URLS = [
    'https://www.screener.in/screens/261242/nifty-50/?limit=50&page=1',
    'https://www.screener.in/screens/261242/nifty-50/?limit=50&page=2'
]

def scrape_company_links(url):
    """Scrapes company names and their links from the given Screener URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        tree = html.fromstring(response.content)

        rows_xpath = '/html/body/main/div[2]/div[5]/table/tbody/tr[position()>1]'
        name_xpath = './td[2]/a/text()'
        link_xpath = './td[2]/a/@href'

        rows = tree.xpath(rows_xpath)
        data = []

        for row in rows:
            name = row.xpath(name_xpath)[0].strip() if row.xpath(name_xpath) else None
            link = row.xpath(link_xpath)[0].strip() if row.xpath(link_xpath) else None
            if name and link:
                data.append((name, link))

        return data
    except Exception as e:
        print(f"Error scraping company links from {url}: {e}")
        return []

def get_company_links():
    """Aggregates company names and links from all predefined URLs."""
    all_data = []
    for url in URLS:
        all_data.extend(scrape_company_links(url))
    return pd.DataFrame(all_data, columns=['Company Name', 'Link'])

def get_company_link(company_name, df_links):
    """Retrieves the link of a given company from the DataFrame."""
    match = df_links[df_links['Company Name'].str.lower() == company_name.lower()]
    return match['Link'].values[0] if not match.empty else "Company not found."

def scrape_nifty50_table(url):
    """Scrapes the full financial data table from Screener's Nifty 50 page."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        tree = html.fromstring(response.content)

        header_xpath = '/html/body/main/div[2]/div[5]/table/tbody/tr[1]/th'
        rows_xpath = '/html/body/main/div[2]/div[5]/table/tbody/tr[position()>1]'

        header_elements = tree.xpath(header_xpath)
        header = [element.text_content().strip() for element in header_elements]

        if not header:
            raise ValueError("Header extraction failed, please check the XPath.")

        rows = tree.xpath(rows_xpath)
        data = [[col.text_content().strip() for col in row.xpath('./td')] for row in rows if row.xpath('./td')]

        if not data:
            raise ValueError("Data extraction failed, please check the XPath.")

        return pd.DataFrame(data, columns=header)
    except Exception as e:
        print(f"Error scraping financial data from {url}: {e}")
        return None

def scrape_quarterlypnl_sheet(url):
    """Scrapes the quarterly P&L sheet from the given company URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table')
        if not table:
            print(f"Table not found for URL: {url}")
            return None

        header_row = table.find('thead').find('tr')
        headers = [th.text.strip() for th in header_row.find_all('th')]

        data_rows = table.find('tbody').find_all('tr')
        data = [[td.text.strip() for td in row.find_all('td')] for row in data_rows]

        return pd.DataFrame(data, columns=headers)
    except Exception as e:
        print(f"Error scraping quarterly P&L sheet for URL {url}: {e}")
        return None
    
def get_income_statement(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.select_one('section:nth-of-type(5) > div:nth-of-type(3) > table')
        if not table:
            print(f"Table not found for URL: {url}")
            return None
        headers = [th.text.strip() for th in table.select_one('thead > tr').find_all('th')]
        data = [[td.text.strip() for td in row.find_all('td')] for row in table.select('tbody > tr')]
        return pd.DataFrame(data, columns=headers)
    except Exception as e:
        print(f"Error scraping data for URL {url}: {e}")
        return None

def scrape_table(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)
    
    table_xpath = '/html/body/main/section[3]/div[2]/div[3]/table/tbody'
    headers = [header.text.strip() for header in driver.find_elements(By.XPATH, table_xpath + '/tr[1]/th')]
    rows = driver.find_elements(By.XPATH, table_xpath + '/tr')[1:]
    data = [[cell.text.strip() for cell in row.find_elements(By.TAG_NAME, 'td')] for row in rows]
    driver.quit()
    return pd.DataFrame(data, columns=headers)

def calculate_statistics(df, column_name):
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame")
    column_data = pd.to_numeric(df[column_name], errors='coerce').dropna()
    return {
        'Average': column_data.mean(),
        '25th Percentile': column_data.quantile(0.25),
        '50th Percentile (Median)': column_data.median(),
        '75th Percentile': column_data.quantile(0.75),
        '90th Percentile': column_data.quantile(0.90)
    }

def calculate_adjusted_statistics(df, column_name, price, pe):
    statistics = calculate_statistics(df, column_name)
    price, pe = pd.to_numeric(price, errors='coerce'), pd.to_numeric(pe, errors='coerce')
    adjusted_statistics = {key: (value * price) / pe for key, value in statistics.items() if np.issubdtype(type(value), np.number)}
    return adjusted_statistics

def process_company(company_name, get_company_link):
    company_link = get_company_link(company_name)
    if company_link == "Company not found.":
        print(company_link)
        return
    full_url = "https://www.screener.in" + company_link
    income_statement_df = get_income_statement(full_url)
    if income_statement_df is not None:
        print(f"Company: {company_name} - Income Statement")
        print(income_statement_df[:-2])
    df = scrape_table(full_url)
    print(df)
    pe, price = pd.to_numeric(df.iloc[0, 3], errors='coerce'), pd.to_numeric(df.iloc[0, 2], errors='coerce')
    adjusted_statistics = calculate_adjusted_statistics(df, 'P/E', price, pe)
    print(f"Relative valuation at Peer s' 'P/E' stats:")
    for stat, value in adjusted_statistics.items():
        print(f"Price at {stat}: {value:.2f}")
    print("Current price-", price)

