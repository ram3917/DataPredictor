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

def create_graph():
    """
    The following script downloads and plots data from Stock market.
    """
    cols = ["Tata"]
    df = pd.DataFrame(data=None,columns=cols)

    # Get closing price
    tata_df = dc.GetStockData("TATAMOTORS.NS")
    df["Tata"] = tata_df['Close'].copy()

    # drop na
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    data = [
        go.Line(
            x=df.index, # assign x as the dataframe column 'x'
            y=[]
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

    graph = create_graph()

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
            idx_df = dc.GetStockData(symbol)
            df[index] = idx_df['Close'].copy()
            break

    # drop na
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    data = [
        go.Line(
            x=df.index, # assign x as the dataframe column 'x'
            y=df[index]
        )
    ]

    # JSON for plotting
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return str(graphJSON)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)