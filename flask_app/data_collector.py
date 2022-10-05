#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 20:41:43 2021

@author: rama
"""

import yfinance as yf

"""
DATA-COLLECTOR shall gather data for selected stocks from yahoo finance.
"""
def GetStockData(index="", duration="max"):
    # Query data
    idx = yf.Ticker(index)
    df = idx.history(period=duration)
    
    return df
