import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
from data_collector import *
import streamlit.components.v1 as components

# Set config
def set_page_config():
    st.set_page_config(
        page_title="Finance Dashboard",
        page_icon=":line_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)

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

    # Set title    
    st.header(select_name)
    # Line chart
    st.line_chart(df, x='Date', y=['Close', 'Weekly_average', 'Monthly_average'])
    
    # Add columns to show changes
    col1, col2, col3 = st.columns(3)
    # Show 3 months change
    maxVal, deltaChange = CalculateThreeMonthHigh(df, 3)
    col1.metric(label="Delta to 3 months max value", value="%.2f %" % (maxVal), delta="%.2f EUR" % (deltaChange))
    
    # Show 3 months change
    maxVal, deltaChange = CalculateThreeMonthHigh(df, 6)
    col2.metric(label="Delta to 6 months max value", value="%.2f %" % (maxVal), delta="%.2f EUR" % (deltaChange))

    # Show 3 months change
    maxVal, deltaChange = CalculateThreeMonthHigh(df, 12)
    col3.metric(label="Delta to 12 months max value", value="%.2f %" % (maxVal), delta="%.2f EUR" % (deltaChange))

    components.html('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9719516206957584" crossorigin="anonymous"></script>', height=300)