#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 20:41:43 2021

@author: rama
"""
import os
import pandas as pd
import yfinance as yf

"""
DATA-COLLECTOR shall gather data for selected stocks from yahoo finance.
"""

'''
Source : https://investexcel.net/all-yahoo-finance-stock-tickers/
'''
stockList = pd.read_excel(io= os.getcwd() + "\\flask_app\\static\\Yahoo Ticker Symbols - September 2017.xlsx",
                sheet_name= 'Stock', usecols='A:E', skiprows=3, index_col=None)

stockList.reset_index(drop=True)

def GetStockData(index="", duration="max"):
    # Query data
    idx = yf.Ticker(index)
    df = idx.history(period=duration)
    
    return df


def CalculateAverageReturns(index=""):
    pass

def CalculateChange(index=""):
    pass