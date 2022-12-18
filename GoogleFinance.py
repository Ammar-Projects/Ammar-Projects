# Webscraper to pull stock data from multiple Google Finance pages

# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# List the stock symbols you are interested in (these can be found on the company's page on Google Finance)
companies = ['DIS:NYSE','NFLX:NASDAQ','GOOGL:NASDAQ','AMZN:NASDAQ','META:NASDAQ']

# Initialize lists
current = []
names = []
previous = []

# Parse through each company's page and append values to lists
for x in companies:
    url = 'https://www.google.com/finance/quote/' + x
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    soup = BeautifulSoup(soup.prettify(),'html.parser')
    price = soup.find('div',{'class':'YMlKec fxKbKc'})
    name = soup.find('div',{'class':'zzDege'})
    prev = soup.find('div',{'class':'P6K39c'})
    current.append(price.text.strip())
    names.append(name.text.strip())
    previous.append(prev.text.strip())

# Create dataframe
data = {'Company':names,
        'CurrentPrice':current,
        'PreviousPrice':previous}
df = pd.DataFrame(data)

# Format dataframe
df[['CurrentPrice','PreviousPrice']] = df[['CurrentPrice','PreviousPrice']].replace('[\$,]', '', regex=True).astype(float)
df['PercentChg'] = (((df.CurrentPrice - df.PreviousPrice)/df.PreviousPrice)*100).round(2)

# View the dataframe
df