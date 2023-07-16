#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 20:41:43 2021

@author: Rama Mallavarapu
"""
from forex_python.converter import CurrencyRates
import pandas as pd
from pandas.tseries.offsets import DateOffset
import yfinance as yf

"""
DATA-COLLECTOR shall gather data for selected stocks from yahoo finance.
"""

# '''
# Source : https://investexcel.net/all-yahoo-finance-stock-tickers/
# '''
# stockList = pd.read_excel(io="./streamlit_app/Yahoo Ticker Symbols - September 2017.xlsx",
#                 sheet_name= 'Stock', usecols='A:E', skiprows=3, index_col=None)

stockList = pd.read_csv("./streamlit_app/MyPortfolio.csv", sep=';')
stockList.reset_index(drop=True)

def GetStockData(index="", duration="max"):
    # Query data
    idx = yf.Ticker(index)
    df = idx.history(period=duration, interval="1d")

    # Convert the rates to Euros - I trade in EUROS
    c = CurrencyRates()
    exchange_value = c.get_rate('USD', 'EUR')

    # df['Open'] = df['Open'] * exchange_value
    # df['High'] = df['High'] * exchange_value
    # df['Low'] = df['Low'] * exchange_value
    df['Close'] = df['Close'] * exchange_value

    df = df['Close'].round(2)

    return df

def CalculateTimePeriodDelta(df, offsetMonths=3):
    currDate  = df['Date'].iloc[-1]
    startDate = currDate - DateOffset(months=offsetMonths)

    df = df[df['Date'].between(startDate, currDate)]

    maxVal = df['Close'].max()    
    currVal = df['Close'].iloc[-1]

    deltaChange = ((currVal - maxVal) / maxVal) * 100
    
    return maxVal, deltaChange

def CalculateChange(index=""):
    pass