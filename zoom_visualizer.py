#tracks zoom's stock price over a span of a year 

from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import matplotlib.pyplot as pyplot
import pandas as pd
import numpy as np 
from datetime import datetime 
from matplotlib import pyplot as plt

START_DATE = '2019-10-01'
END_DATE = str(datetime.now().strftime('%Y-%m-%d'))

#UK_STOCK = 'UU.L'
USA_STOCK = 'ZM'

def get_stats(stock_data):
    return {
        'last':np.mean(stock_data.tail(1)),
        'short_mean': np.mean(stock_data.tail(20)),
        'long_mean': np.mean(stock_data.tail(200)),
        'short_rolling': stock_data.rolling(window=20).mean(),
        'long_rolling': stock_data.rolling(window=200).mean()
    }

def clean_data(stock_data, col):
    weekdays = pd.date_range(start=START_DATE, end=END_DATE)
    clean_data = stock_data[col].reindex(weekdays)
    return clean_data.fillna(method='ffill')

def create_plot(stock_data, ticker):
    stats = get_stats(stock_data)
    #plt.style.use('dark_background')
    plt.subplots(figsize=(12,8))
    plt.plot(stock_data, label=ticker)
    plt.plot(stats['short_rolling'], label='20 day rolling mean')
    plt.plot(stats['long_rolling'], label='200 day rolling mean')
    plt.xlabel('Days since OCT 1 2019')
    plt.ylabel('Adj Close(p)')
    plt.legend()
    plt.title("Stock Price from 2019-2020")
    plt.show()

def get_data(ticker):
    try:
        stock_data = data.DataReader(ticker,
                                      'yahoo',
                                      START_DATE,
                                      END_DATE)
        adj_close = clean_data(stock_data, 'Adj Close')
        create_plot(adj_close, ticker)

    except RemoteDataError:
        print("No data found for {t}'.format(t=ticker")

get_data(USA_STOCK)
