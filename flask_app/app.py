import os
from unicodedata import name
from venv import create

from flask import Flask, render_template, redirect, request, url_for, jsonify

import plotly
import plotly.graph_objects as go

from pytickersymbols import PyTickerSymbols

import pandas as pd
import numpy as np
import json

import flask_app.data_collector as dc

app = Flask(__name__, static_folder="./static", template_folder="./static/templates")
app.config['SECRET_KEY'] = "SECRET_KEY_VALUE"

def create_graph(symbol):
    """
    The following script downloads and plots data from Stock market.
    """
    cols = [symbol]
    df = pd.DataFrame(data=None,columns=cols)

    # Get closing price
    tmp_df = dc.GetStockData(symbol)
    df[symbol] = tmp_df['Close'].copy()

    # drop na
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    # Calculate the rolling averages for 7 days and 30 days
    df['Weekly_average'] = df[symbol].rolling(7).mean()
    df['Monthly_average'] = df[symbol].rolling(30).mean()

    data = [
        go.Line(
            x=df.index, # assign x as the dataframe column 'x'
            y=df[symbol],
            name='Closing Price'
        ),
        go.Line(
            x=df.index, # assign x as the dataframe column 'x'
            y=df['Weekly_average'],
            name='Weekly Change'
        ),
        go.Line(
            x=df.index, # assign x as the dataframe column 'x'
            y=df['Monthly_average'],
            name='Monthly Change'
        )
    ]

    # JSON for plotting
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/')
def index():

    pys = PyTickerSymbols()
    countryList = pys.get_all_countries()
    indexList = pys.get_all_indices()

    graph = []

    return render_template("index.html", 
                plot=graph,
                countryList=countryList,
                indices=indexList,
                selectedStocks=[])

@app.route('/updateCountry', methods=['GET', 'POST'])
def updateCountry():
    value = request.get_json()
    pys = PyTickerSymbols()
    stocksList = pys.get_stocks_by_country(value)

    stocks = []
    for s in stocksList:
        stocks.append(s['name'])

    return jsonify(render_template('stockList.html',
             selectedStocks=stocks))

@app.route('/updateIndex', methods=['GET', 'POST'])
def updateIndex():
    value = request.get_json()
    pys = PyTickerSymbols()
    stocksList = pys.get_stocks_by_index(value)

    stocks = []
    for s in stocksList:
        stocks.append(s['name'])

    return jsonify(render_template('stockList.html',
             selectedStocks=stocks))

@app.route('/updateGraph', methods=['GET', 'POST'])
def updateGraph():

    index = request.get_json()
    df = pd.DataFrame(data=None,columns=[index])

    pys = PyTickerSymbols()
    stockList = pys.get_all_stocks()

    for stock in stockList:
        if stock['name'] == index:
            symbol = stock['symbol']
            break
    
    graphJSON = create_graph(symbol)

    return str(graphJSON)

if __name__ == '__main__':
    app.run(port=os.environ.get("PORT", 5000), host='0.0.0.0', debug=False, threaded=True)