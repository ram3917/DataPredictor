#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 20:41:43 2021

@author: rama
"""

import yfinance as yf
import pandas as pd

"""
DATA-COLLECTOR shall gather data for selected stocks from yahoo finance.
"""

# Query data
tata_motors = yf.Ticker("TATAMOTORS.NS")
tata_df = tata_motors.history(period="3y")

cols = ["Daily_Closing", "Weekly_average", "Monthly_average", "Weekly_var","Monthly_var"]
df = pd.DataFrame(data=None,columns=cols)

# Get closing price
df["Daily_Closing"] = tata_df['Close'].copy()

# drop na
df.dropna()

# Calculate the rolling averages for 7 days and 30 days
df['Weekly_average'] = df.rolling(7).mean()
df['Monthly_average'] = df.rolling(30).mean()

# Calculate the rolling variances for 7 days and 30 days
df['Weekly_var'] = df.rolling(30).var()
df['Monthly_var'] = df.rolling(30).var()

# Save data
df = df.round(2)
df.to_csv("data/tata_motors.csv")
df.to_json("data/tata_motors.json")