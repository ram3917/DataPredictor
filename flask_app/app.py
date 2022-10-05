from flask import Flask, render_template, redirect, request, url_for, session

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
    # Get closing price
    tata_df = dc.GetStockData("TATAMOTORS.NS")
    df["Tata"] = tata_df['Close'].copy()

    # drop na
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    data = [
        go.Line(
            x=df.index, # assign x as the dataframe column 'x'
            y=df['Tata']
        )
    ]

    # JSON for plotting
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/')
def index():
    indexList = PyTickerSymbols()
    stockList = indexList.get_stocks_by_index('DAX')

    indices = []
    for stock in stockList:
        indices.append(stock['name'])

    graph = create_graph()

    return render_template("index.html", 
                plot=graph,
                indices=indices,
                selectedIndices=indices)

@app.route('/addIndexToList', methods=['POST'])
def addIndexToList():
    value = request.get_json()
    if len(selectedIndices)==0:
        selectedIndices = selectedIndices.append(value)
    else:
        selectedIndices = [value]

    return redirect(url_for("/index"))

@app.route('/updateGraph', methods=['GET', 'POST'])
def updateGraph():

    index = request.get_json()
    df = pd.DataFrame(data=None,columns=[index])

    indexList = PyTickerSymbols()
    stockList = indexList.get_stocks_by_index('DAX')

    indices = []
    for stock in stockList:
        indices.append(stock['name'])
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

    return render_template("index.html", 
                plot=graphJSON,
                indices=indices,
                selectedIndices=indices)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)