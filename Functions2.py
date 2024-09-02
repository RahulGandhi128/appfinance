# Function 1: Scrape data from URLs and return a combined DataFrame
def function_1():
    import requests
    from lxml import html
    import pandas as pd

    # List of URLs to scrape
    urls = [
        'https://www.screener.in/screens/261242/nifty-50/?limit=50&page=1',
        'https://www.screener.in/screens/261242/nifty-50/?limit=50&page=2'
    ]

    # Function to scrape data from a single URL
    def scrape_data_from_url(url):
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Ensure we notice bad responses

        # Parse the content of the request with lxml
        tree = html.fromstring(response.content)

        # Define XPaths
        header_xpath = '/html/body/main/div[2]/div[5]/table/tbody/tr[1]/th'
        rows_xpath = '/html/body/main/div[2]/div[5]/table/tbody/tr[position()>1]'

        # Extract header
        header_elements = tree.xpath(header_xpath)
        header = [element.text_content().strip() for element in header_elements]

        # Check if header is correctly extracted
        if not header:
            raise ValueError("Header extraction failed, please check the XPath for the header.")

        # Extract rows
        rows = tree.xpath(rows_xpath)
        data = []

        for row in rows:
            # Extract columns for each row
            columns = row.xpath('./td')
            row_data = [col.text_content().strip() for col in columns]
            if row_data:
                data.append(row_data)

        # Check if data extraction is successful
        if not data:
            raise ValueError("Data extraction failed, please check the XPath for the rows.")

        # Create DataFrame
        df = pd.DataFrame(data, columns=header)

        return df

    # Function to scrape data from multiple URLs and combine into a single DataFrame
    def scrape_full_data(urls):
        all_dataframes = []
        for url in urls:
            df = scrape_data_from_url(url)
            all_dataframes.append(df)
        
        # Concatenate all DataFrames into a single DataFrame
        nifty50_df = pd.concat(all_dataframes, ignore_index=True)
        
        return nifty50_df

    # Scrape full data from all URLs and combine into one DataFrame
    nifty50_df = scrape_full_data(urls)

    return nifty50_df


# Function 2: Scrape company names and links
def function_2():
    import requests
    from lxml import html
    import pandas as pd

    # URLs to scrape
    urls = [
        'https://www.screener.in/screens/261242/nifty-50/?limit=50&page=1',
        'https://www.screener.in/screens/261242/nifty-50/?limit=50&page=2'
    ]

    def scrape_data(url):
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Ensure we notice bad responses

        # Parse the content of the request with lxml
        tree = html.fromstring(response.content)

        # Define XPaths
        rows_xpath = '/html/body/main/div[2]/div[5]/table/tbody/tr[position()>1]'
        name_xpath = './td[2]/a/text()'
        link_xpath = './td[2]/a/@href'

        # Extract rows
        rows = tree.xpath(rows_xpath)
        data = []

        for row in rows:
            # Extract company name and link
            name = row.xpath(name_xpath)[0].strip() if row.xpath(name_xpath) else None
            link = row.xpath(link_xpath)[0].strip() if row.xpath(link_xpath) else None
            if name and link:
                data.append((name, link))

        return data

    # Aggregate data from all URLs
    all_data = []
    for url in urls:
        all_data.extend(scrape_data(url))

    # Create DataFrame for the company names and links
    df_links = pd.DataFrame(all_data, columns=['Company Name', 'Link'])

    return df_links


def get_company_link(company_name, df_links):
    match = df_links[df_links['Company Name'].str.lower() == company_name.lower()]
    return match['Link'].values[0] if not match.empty else "Company not found."
def scrape_quarterlypnl_sheet(url):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table element containing the P&L sheet data
        table = soup.find('table')
        if not table:
            print(f"Table not found for URL: {url}")
            return None

        # Find the header row and extract column names
        header_row = table.find('thead').find('tr')
        headers = [th.text.strip() for th in header_row.find_all('th')]

        # Find the data rows and extract data
        data_rows = table.find('tbody').find_all('tr')
        data = []
        for row in data_rows:
            data.append([td.text.strip() for td in row.find_all('td')])

        # Create a DataFrame from the extracted data
        df = pd.DataFrame(data, columns=headers)

        return df
    except Exception as e:
        print(f"Error scraping data for URL {url}: {e}")
        return None
def scrape_income_statement(url):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.select_one('section:nth-of-type(5) > div:nth-of-type(3) > table')
        if not table:
            print(f"Table not found for URL: {url}")
            return None

        header_row = table.select_one('thead > tr')
        headers = [th.text.strip() for th in header_row.find_all('th')]

        data_rows = table.select('tbody > tr')
        data = [[td.text.strip() for td in row.find_all('td')] for row in data_rows]

        df = pd.DataFrame(data, columns=headers)
        return df
    except Exception as e:
        print(f"Error scraping data for URL {url}: {e}")
        return None
def scrape_balance_sheet(url):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.select_one('section:nth-of-type(6) > div:nth-of-type(2) > table')
        if not table:
            print(f"Balance Sheet table not found for URL: {url}")
            return None

        header_row = table.select_one('thead > tr')
        headers = [th.text.strip() for th in header_row.find_all('th')]

        data_rows = table.select('tbody > tr')
        data = [[td.text.strip() for td in row.find_all('td')] for row in data_rows]

        return pd.DataFrame(data, columns=headers)
    except Exception as e:
        print(f"Error scraping Balance Sheet data for URL {url}: {e}")
        return None
def scrape_cash_flow_statement(url):
    import requests
    from lxml import html
    import pandas as pd

    try:
        response = requests.get(url)
        response.raise_for_status()
        tree = html.fromstring(response.content)

        header_xpath = '/html/body/main/section[7]/div[2]/table/thead/tr'
        body_xpath = '/html/body/main/section[7]/div[2]/table/tbody/tr'

        headers = tree.xpath(header_xpath + '/th/text()')
        rows = tree.xpath(body_xpath)

        data = []
        labels = []

        for row in rows:
            label = row.xpath('td[1]//text()')
            row_data = row.xpath('td[position()>1]/text()')

            if label:
                labels.append(label[0].strip())
            else:
                labels.append("")

            if len(row_data) < len(headers) - 1:
                row_data.extend([None] * (len(headers) - 1 - len(row_data)))
            elif len(row_data) > len(headers) - 1:
                row_data = row_data[:len(headers) - 1]

            data.append(row_data)

        cash_flow_df = pd.DataFrame(data, columns=headers[1:])
        cash_flow_df.insert(0, "Description", labels)

        return cash_flow_df
    except Exception as e:
        print(f"Error scraping Cash Flow Statement data for URL {url}: {e}")
        return None
def process_company_data(company_name, df_links):
    company_link = get_company_link(company_name, df_links)

    if company_link != "Company not found.":
        full_url = "https://www.screener.in" + company_link
        print(f"Full URL: {full_url}")  # Optional debug print

        # Get Income Statement
        income_statement_df = scrape_income_statement(full_url)
        if income_statement_df is not None:
            print(f"Company: {company_name} - Income Statement")
            print(income_statement_df)
        else:
            print(f"Failed to retrieve Income Statement data for {company_name}.")

        # Get Balance Sheet
        balance_sheet_df = scrape_balance_sheet(full_url)
        if balance_sheet_df is not None:
            print(f"Company: {company_name} - Balance Sheet")
            print(balance_sheet_df)
        else:
            print(f"Failed to retrieve Balance Sheet data for {company_name}.")

        # Get Cash Flow Statement
        cash_flow_df = scrape_cash_flow_statement(full_url)
        if not cash_flow_df.empty:
            print(f"Company: {company_name} - Cash Flow Statement")
            print(cash_flow_df)
        else:
            print(f"Failed to retrieve Cash Flow Statement data for {company_name}.")

        # Get Quarterly P&L Statement
        pnl_quarterly = scrape_quarterlypnl_sheet(full_url)
        if pnl_quarterly is not None:
            print(f"Company: {company_name} - Quarterly P&L Statement")
            print(pnl_quarterly)
        else:
            print(f"Failed to retrieve Quarterly P&L Statement data for {company_name}.")
    else:
        print("Company not found or invalid link.")
# 
# 
# 
# Function to scrape a table from a URL ## yha se theek kiya tha 
def scrape_table(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    driver.get(url)
    time.sleep(5)

    # Scrape table
    table_xpath = '/html/body/main/section[3]/div[2]/div[3]/table'
    tbody_xpath = table_xpath + '/tbody'
    header_row_xpath = tbody_xpath + '/tr[1]'
    data_row_xpath = tbody_xpath + '/tr'
    
    headers = driver.find_elements(By.XPATH, header_row_xpath + '/th')
    headers = [header.text.strip() for header in headers]
    
    rows = driver.find_elements(By.XPATH, data_row_xpath)[1:]
    table_data = [[cell.text.strip() for cell in row.find_elements(By.TAG_NAME, 'td')] for row in rows]
    
    driver.quit()

    df = pd.DataFrame(table_data, columns=headers)
    return df
# Function to scrape a table with links from a URL
def scrape_table_with_links(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    driver.get(url)
    time.sleep(5)

    # Scrape table
    table_xpath = '/html/body/main/section[3]/div[2]/div[3]/table'
    tbody_xpath = table_xpath + '/tbody'
    header_row_xpath = tbody_xpath + '/tr[1]'
    data_row_xpath = tbody_xpath + '/tr'
    
    headers = driver.find_elements(By.XPATH, header_row_xpath + '/th')
    headers = [header.text.strip() for header in headers]
    headers.append('Link')

    rows = driver.find_elements(By.XPATH, data_row_xpath)[1:]
    table_data = []
    
    for row in rows:
        row_data = [cell.text.strip() for cell in row.find_elements(By.TAG_NAME, 'td')]
        link_element = row.find_element(By.XPATH, './td[2]/a') if len(row.find_elements(By.XPATH, './td[2]/a')) > 0 else None
        row_data.append(link_element.get_attribute('href') if link_element else None)
        table_data.append(row_data)

    driver.quit()
    
    df_links_peers = pd.DataFrame(table_data, columns=headers)
    df_links_peers = df_links_peers[['S.No.', 'Name', 'Link']]
    
    return df_links_peers
def get_quarterly_income_statements(df_links_peers):
    quarterly_income_statements = {}
    for index, row in df_links_peers.iterrows():
        peer_name = row['Name'].replace(" ", "_")
        peer_link = row['Link']
        quarterly_income_statement = scrape_quarterlypnl_sheet(peer_link)

        if 'Raw PDF' in quarterly_income_statement.iloc[:, 0].values:
            quarterly_income_statement = quarterly_income_statement[quarterly_income_statement.iloc[:, 0] != 'Raw PDF']

        quarterly_income_statements[peer_name + "_quart"] = quarterly_income_statement
    return quarterly_income_statements
def calculate_number_of_shares(dfp):
    dfp['CMP Rs.'] = pd.to_numeric(dfp['CMP Rs.'], errors='coerce')
    dfp['Mar Cap Rs.Cr.'] = pd.to_numeric(dfp['Mar Cap Rs.Cr.'], errors='coerce')
    dfp['Number of Shares in Cr.'] = dfp['Mar Cap Rs.Cr.'] / dfp['CMP Rs.']
    df_shares = dfp[['Name', 'Number of Shares in Cr.']]
    return df_shares
def calculate_firm_metrics(ttm_sales_df, df_shares):
    TTM_Net_Profit_f1 = ttm_sales_df.iloc[0, 4]
    share_f1 = df_shares.iloc[0, 1]
    TTM_Sales_f1 = ttm_sales_df.iloc[0, 1]
    return TTM_Net_Profit_f1, share_f1, TTM_Sales_f1
def calculate_adjusted_statistics(dfp, column_name, TTM_Net_Profit_f1, share_f1):
    column_data = pd.to_numeric(dfp[column_name], errors='coerce').dropna()
    average = column_data.mean()
    percentile_25th = column_data.quantile(0.25)
    percentile_50th = column_data.median()
    percentile_75th = column_data.quantile(0.75)
    percentile_90th = column_data.quantile(0.90)

    statistics = {'Average': average, '25th Percentile': percentile_25th, '50th Percentile': percentile_50th, '75th Percentile': percentile_75th, '90th Percentile': percentile_90th}
    adjusted_statistics = {key: (value * TTM_Net_Profit_f1) / share_f1 for key, value in statistics.items() if np.issubdtype(type(value), np.number)}
    return adjusted_statistics
def calculate_combined_metrics(income_statement_df, cash_flow_df):
    operating_profit_row = income_statement_df[income_statement_df.iloc[:, 0] == "Operating Profit"]
    tax_rate_row = income_statement_df[income_statement_df.iloc[:, 0] == "Tax %"]
    depreciation_row = income_statement_df[income_statement_df.iloc[:, 0] == "Depreciation"]
    cash_flow_investing_row = cash_flow_df[cash_flow_df.iloc[:, 0] == "Cash Flow from investing"]

    if not operating_profit_row.empty and not tax_rate_row.empty and not cash_flow_investing_row.empty:
        operating_profit = clean_and_convert_to_float(operating_profit_row.iloc[0, 1:])
        tax_rate = tax_rate_row.iloc[0, 1:]  # No conversion for tax rate
        sales = clean_and_convert_to_float(income_statement_df.iloc[0, 1:])
        opm = income_statement_df[income_statement_df.iloc[:, 0] == "OPM %"].iloc[0, 1:].str.rstrip('%').astype(float)
        cash_flow_investing = clean_and_convert_to_float(cash_flow_investing_row.iloc[0, 1:])
        investment_rate = (cash_flow_investing / operating_profit) * 100
        depreciation = clean_and_convert_to_float(depreciation_row.iloc[0, 1:])
        depreciation_percentage = (depreciation / sales) * 100

        combined_df = pd.DataFrame({
            "Sales": sales,
            "Operating Profit": operating_profit,
            "OPM (%)": opm,
            "Tax Rate": tax_rate,
            "Investment Rate": investment_rate,
            "Depreciation as % of Revenue": depreciation_percentage
        }).T
        return combined_df
    else:
        return None
import pandas as pd

# Function to transpose and clean DataFrame
def transpose_and_clean_df(df):
    df = df.T
    df = df.dropna(axis=1)
    return df

# Function to clean and convert series to float
def clean_and_convert_to_float(series):
    return series.str.replace(',', '').astype(float)

# Function to calculate investment rate
def calculate_investment_rate(income_statement_df, cash_flow_df):
    # Extract the "Operating Profit" row from the income statement
    operating_profit_row = income_statement_df[income_statement_df.iloc[:, 0] == "Operating Profit"]

    # Extract the "Cash Flow from investing" row from the cash flow statement
    cash_flow_investing_row = cash_flow_df[cash_flow_df.iloc[:, 0] == "Cash Flow from investing"]

    # Ensure necessary rows exist in the dataframes
    if not cash_flow_investing_row.empty and not operating_profit_row.empty:
        # Extract the years (column names) from the income statement, excluding the first column
        years = income_statement_df.columns[1:]

        # Clean and convert the required rows to float
        cash_flow_investing = clean_and_convert_to_float(cash_flow_investing_row.iloc[0, 1:])
        operating_profit = clean_and_convert_to_float(operating_profit_row.iloc[0, 1:])

        # Calculate the investment rate for all periods
        investment_rate_all_periods = (cash_flow_investing / operating_profit) * 100

        # Create a new DataFrame with the investment rate and corresponding year
        investment_rate_df = pd.DataFrame({
            "Year": years,
            "Investment Rate (%)": investment_rate_all_periods
        })

        return investment_rate_df
    else:
        return "Required data rows not found."

# Example function for setting environment variables (if needed)
def set_api_key(api_key):
    import os
    os.environ['GEMINI_API_KEY'] = api_key

# Example function to configure Google Generative AI (if needed)
def configure_genai():
    import os
    import google.generativeai as genai

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    return model

# Example usage of the AI chat model (if needed)
def ask_genai_question(model, question):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [question],
            }
        ]
    )
    response = chat_session.send_message(question)
    return response.text
import numpy as np
import pandas as pd

# Function to handle company name input
def get_company_input():
    company_name = input("Enter the company name: ")
    return company_name

# Function to ask for company forecast
def get_forecast(company_name, chat_session):
    message = f"{company_name} sales GROWTH and operating margin forecast for next year, and for 5 years average, give just numbers not text and strictly no text"
    response = chat_session.send_message(message)
    return response.text

# Function to ask for WACC
def get_wacc(company_name, chat_session):
    message = f"{company_name} WACC"
    response = chat_session.send_message(message)
    return response.text

# Function to ask for EV/EBITDA ratio
def get_ev_ebitda(company_name, chat_session):
    message = f"{company_name} EV/EBITDA ratio"
    response = chat_session.send_message(message)
    return response.text

# Function to clean and convert WACC or EV/EBITDA values
def clean_percentage_value(value):
    clean_value = value.strip().rstrip('%')
    return float(clean_value) / 100

# Function to split and extract forecast values
def extract_forecast_values(x1):
    values = [v for v in x1.strip().split('\n') if v.strip()]
    if len(values) < 4:
        raise ValueError("x1 string does not contain enough forecast data.")
    
    next_year_sales_growth = float(values[0].strip().rstrip('%'))
    next_year_opm = float(values[1].strip().rstrip('%'))
    average_5yr_sales_growth = float(values[2].strip().rstrip('%'))
    average_5yr_opm = float(values[3].strip().rstrip('%'))

    return next_year_sales_growth, next_year_opm, average_5yr_sales_growth, average_5yr_opm

# Function to calculate forecasted sales and other metrics
def calculate_forecasted_sales(combined_df, next_year_sales_growth, next_year_opm, average_5yr_sales_growth, average_5yr_opm):
    last_year_sales = combined_df.loc["Sales"].iloc[-1]
    forecast_years = ["Mar 2025", "Mar 2026", "Mar 2027", "Mar 2028", "Mar 2029"]
    
    forecasted_sales = [last_year_sales * (1 + next_year_sales_growth / 100)]
    compounded_growth_factor = ((1 + average_5yr_sales_growth / 100) ** 5) / (1 + next_year_sales_growth / 100)

    for _ in range(1, len(forecast_years)):
        previous_sales = forecasted_sales[-1]
        next_sales = previous_sales * compounded_growth_factor**(1 / (len(forecast_years) - 1))
        forecasted_sales.append(next_sales)

    avg_depreciation_pct = np.mean(combined_df.loc["Depreciation as % of Revenue"])
    avg_tax_rate = np.mean(combined_df.loc["Tax Rate"].str.rstrip('%').astype(float)).astype(int)
    investment_rates = combined_df.loc["Investment Rate"]
    mean_investment_rate = np.mean(investment_rates)
    filtered_investment_rates = investment_rates[(investment_rates <= 0) | (investment_rates <= 3 * mean_investment_rate)]
    avg_investment_rate = np.mean(filtered_investment_rates)

    forecast_df = pd.DataFrame(index=forecast_years)
    forecast_df["Sales"] = forecasted_sales
    forecast_df["OPM (%)"] = [next_year_opm] + [average_5yr_opm] * (len(forecast_years) - 1)
    forecast_df["Operating Profit"] = forecast_df["Sales"] * forecast_df["OPM (%)"] / 100
    forecast_df["Tax Rate"] = f"{avg_tax_rate}%"
    forecast_df["Investment Rate"] = avg_investment_rate
    forecast_df["Depreciation as % of Revenue"] = avg_depreciation_pct

    predicted_combined_df = pd.concat([combined_df.T, forecast_df], axis=0).T
    return predicted_combined_df

# Function to calculate FCFF for each row
def calculate_fcff(row):
    op_profit = float(row["Operating Profit"])
    tax_rate = float(row["Tax Rate"].strip('%')) / 100
    investment_rate = float(row["Investment Rate"]) / 100
    depreciation_pct = float(row["Depreciation as % of Revenue"]) / 100

    fcff = op_profit * (1 - tax_rate) + (op_profit * investment_rate) + (row["Sales"] * depreciation_pct)
    return fcff

# Function to calculate terminal value using the Gordon Growth Model
def calculate_terminal_value(d1, growth_rate, discount_rate):
    terminal_value = d1 * (1 + growth_rate) / (discount_rate - growth_rate)
    return terminal_value

# Example to handle forecasts
def handle_forecast(company_name, combined_df, chat_session):
    x1 = get_forecast(company_name, chat_session)
    x3 = get_wacc(company_name, chat_session)
    x4 = get_ev_ebitda(company_name, chat_session)
    
    x3_float = clean_percentage_value(x3)
    x4_float = clean_percentage_value(x4)

    next_year_sales_growth, next_year_opm, average_5yr_sales_growth, average_5yr_opm = extract_forecast_values(x1)
    
    predicted_combined_df = calculate_forecasted_sales(combined_df, next_year_sales_growth, next_year_opm, average_5yr_sales_growth, average_5yr_opm)

    # Calculate FCFF
    dfx = predicted_combined_df.loc[:, "Mar 2025":"Mar 2029"].T
    dfx["FCFF"] = dfx.apply(calculate_fcff, axis=1)
    
    # Terminal Value Calculation
    d1 = dfx.iloc[-1, -1]
    growth_rate = 0.05
    terminal_value = calculate_terminal_value(d1, growth_rate, x3_float)

    return predicted_combined_df, terminal_value
import numpy as np
import pandas as pd

# Existing functions ...

# Function to calculate the present value of FCFF
def calculate_pv_of_fcff(dfx, discount_rate):
    fcff_pv = sum(dfx.loc["FCFF", year] / ((1 + discount_rate) ** i) for i, year in enumerate(dfx.columns, 1))
    return fcff_pv

# Function to calculate the present value (PV)
def calculate_pv(fcff_pv, terminal_value):
    return fcff_pv + terminal_value

# Function to calculate net value from the balance sheet
def calculate_net_value(balance_sheet_df, index_other_assets, index_borrowings):
    balance_sheet_df.columns = balance_sheet_df.columns.str.strip()
    balance_sheet_df.set_index(balance_sheet_df.columns[0], inplace=True)

    latest_year = balance_sheet_df.columns[-1]

    net = (
        float(balance_sheet_df.iloc[index_other_assets][latest_year].replace(',', ''))
        - float(balance_sheet_df.iloc[index_borrowings][latest_year].replace(',', ''))
    )
    return net

# Function to predict the share price
def predict_share_price(pv, net, share_f1):
    if pv < 0:
        share_price_pred = net / share_f1
    else:
        share_price_pred = (pv + net) / share_f1

    return np.round(share_price_pred, 2)

# Example function combining the logic of cells 30-33
def calculate_predicted_share_price(dfx, terminal_value, balance_sheet_df, share_f1, index_other_assets=8, index_borrowings=2):
    discount_rate = 0.15  # Example discount rate, adjust as needed

    # Calculate PV of FCFF
    fcff_pv = calculate_pv_of_fcff(dfx, discount_rate)
    
    # Calculate total present value
    pv = calculate_pv(fcff_pv, terminal_value)

    # Calculate net value from balance sheet
    net = calculate_net_value(balance_sheet_df, index_other_assets, index_borrowings)

    # Predict the share price
    share_price_pred = predict_share_price(pv, net, share_f1)

    return share_price_pred
