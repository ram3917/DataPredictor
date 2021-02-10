#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 22:12:42 2021

@author: rama
"""

import DataCollector as dc
import pandas as pd
import matplotlib.pyplot as plt

"""
The following script downloads and plots data from Stock market.
"""
cols = ["Tata", "Reliance"]
df = pd.DataFrame(data=None,columns=cols)

# Get closing price
tata_df = dc.GetStockData("TATAMOTORS.NS")
df["Tata"] = tata_df['Close'].copy()

reliance_df = dc.GetStockData("RELIANCE.NS")
df["Reliance"] = reliance_df['Close'].copy()

# drop na
df.fillna(method='ffill', inplace=True)
df.fillna(method='bfill', inplace=True)

# # Calculate the rolling averages for 7 days and 30 days
# df['Weekly_average'] = df.rolling(7).mean()
# df['Monthly_average'] = df.rolling(30).mean()

# # Calculate the rolling variances for 7 days and 30 days
# df['Weekly_var'] = df.rolling(30).var()
# df['Monthly_var'] = df.rolling(30).var()

# Save data
df = df.round(2)
df.to_csv("data/test_data.csv")
df.to_json("data/test_data.json")

daily_returns = df.copy()
daily_returns = ( daily_returns[1:] / daily_returns[:-1].values ) - 1
daily_returns.iloc[0, :] = 0

'Plot for analysis'
fig, ax = plt.subplots(1, 2)
daily_returns.plot(ax=ax[0])

daily_returns['Tata'].plot.hist(label='Tata', bins=20,alpha=0.8, ax=ax[1])
daily_returns['Reliance'].plot.hist(label='Reliance', bins=20,alpha=0.8, ax=ax[1])

plt.show()


