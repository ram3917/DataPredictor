import streamlit as st
import pandas as pd
from data_collector import *

st.title('Stock Price for the Last Year')

# Using object notation
select_exchange = st.sidebar.selectbox(
    "Which Exchange are we looking at?",
    (stockList['Exchange'].unique())
)

if select_exchange:
    # Using object notation
    select_name = st.sidebar.selectbox(
        "Which Stock do you want to look at?",
        (stockList[stockList['Exchange']==select_exchange]['Name'].to_list())
    )
else:
    # Using object notation
    select_name = st.sidebar.selectbox(
        "Which Stock do you want to predict?",
        (stockList['Name'].to_list())
    )

if select_exchange and select_name:
    
    symbol = stockList.loc[(stockList['Exchange']==select_exchange) & (stockList['Name']==select_name)]
    symbol = symbol.reset_index()
        
    # Get closing price
    df = GetStockData(symbol['Ticker'][0], '5y')
    df = df.reset_index()
    # drop na
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    # Calculate the rolling averages for 7 days and 30 days
    df['Weekly_average'] = df['Close'].rolling(7).mean()
    df['Monthly_average'] = df['Close'].rolling(30).mean()

    plot_df = df[['Date','Close', 'Weekly_average','Monthly_average']].copy()

    st.header(select_name)
    st.line_chart(plot_df, x='Date', y=['Close', 'Monthly_average'])