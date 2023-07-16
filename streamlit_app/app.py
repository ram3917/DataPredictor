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

def plot_chart(exchange, stock):
    symbol = stockList.loc[(stockList['Exchange']==exchange) & (stockList['Name']==stock)]
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

    plot_chart(select_exchange, select_name)    
    
    # Add columns to show changes
    col1, col2, col3 = st.columns(3)

    n_Cols = 1
    for iter in st.columns(4):
        # Get 3, 6, 12 month changes
        n_months = n_Cols * 3
        n_Cols = n_Cols + 1
        # Show changes months change
        maxVal, deltaChange = CalculateTimePeriodDelta(df, n_months)
        iter.metric(label="Delta to {0} months High".format(n_months),
                     value="{:.2f} EUR".format(maxVal), delta="{0:.2f} %".format(deltaChange))   

components.html('<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="ramashwinkX" data-color="#FF5F5F" data-emoji="☕"  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-position="Right" data-font-color="#ffffff" data-coffee-color="#FFDD00" ></script>')