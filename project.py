!pip install yfinance
!pip install bs4
!pip install nbformat

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

    # Create a ticker object for Tesla (TSLA)
tesla_ticker = yf.Ticker("TSLA")

# Get historical market data
tesla_stock_data = tesla_ticker.history(period="max")

# You can display the first few rows to check the data
print(tesla_stock_data.head())
# You would typically get this from another source or have it in a separate file
tesla_revenue_data = pd.DataFrame({
    "Date": ["2020-12-31", "2021-03-31", "2021-06-30", "2021-09-30"],
    "Revenue": [10744, 10389, 11958, 13757]
})
# Convert Date to datetime format
tesla_revenue_data['Date'] = pd.to_datetime(tesla_revenue_data['Date'])

print(tesla_revenue_data)

# Get historical market data for Tesla with the maximum period
tesla_data = tesla_ticker.history(period="max")

# Display the first few rows to check the data
print(tesla_data.head())

# Reset the index
tesla_data.reset_index(inplace=True)

# Display the first few rows to check the data
print(tesla_data.head())


# Download the webpage containing the Tesla revenue data
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
response = requests.get(url)
html_data = response.text

# Parse the HTML data using BeautifulSoup
soup = BeautifulSoup(html_data, "html.parser")
# Extract the table with Tesla revenue data
tables = soup.find_all('table')
tesla_revenue = pd.read_html(str(tables))[1] 

# Rename the columns for clarity
tesla_revenue.columns = ["Date", "Revenue"]

# Clean the Revenue column
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace(",|\$", "", regex=True)

# Remove any null or empty strings in the Revenue column
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue["Revenue"] != ""]

# Display the last 5 rows of the tesla_revenue dataframe
print(tesla_revenue.tail())

# Create a ticker object for GameStop (GME)
gme_ticker = yf.Ticker("GME")

# Get historical market data for GameStop with the maximum period
gme_data = gme_ticker.history(period="max")

# Reset the index
gme_data.reset_index(inplace=True)

print(gme_data.head())




# Extract the table with GameStop revenue data
tables_gme = soup_gme.find_all('table')
gme_revenue = pd.read_html(str(tables_gme))[1]  # Assuming the second table contains the revenue data

# Rename the columns for clarity
gme_revenue.columns = ["Date", "Revenue"]

# Clean the Revenue column
gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace(",|\$", "", regex=True)

# Remove any null or empty strings in the Revenue column
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue["Revenue"] != ""]

# Display the last 5 rows of the gme_revenue dataframe
print(gme_revenue.tail())


make_graph(tesla_data, tesla_revenue, "Tesla (TSLA) Stock Data up to June 2021")


# Step 1: Plot the GameStop stock graph using make_graph function
make_graph(gme_data, gme_revenue, 'GameStop')
