from optparse import Values
import os
from unicodedata import name
from venv import create

from flask import Flask, render_template, redirect, request, url_for, jsonify, session

import plotly
import plotly.graph_objects as go

from pytickersymbols import PyTickerSymbols

import pandas as pd
import numpy as np
import json
import uuid 

import flask_app.data_collector as dc
from flask_app.data_collector import stockList

app = Flask(__name__, static_folder="./static", template_folder="./static/templates")
app.config['SECRET_KEY'] = str(uuid.uuid4())

def create_graph(symbol):
    """
    The following script downloads and plots data from Stock market.
    """
    # Get closing price
    df = dc.GetStockData(symbol)

    # drop na
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    # Calculate the rolling averages for 7 days and 30 days
    df['Weekly_average'] = df['Close'].rolling(7).mean()
    df['Monthly_average'] = df['Close'].rolling(30).mean()

    # Create figure
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df.index, y=df['Close'], mode='lines+markers', name='Closing Price'))

    fig.add_trace(
        go.Scatter(x=df.index, y=df['Weekly_average'], mode='lines+markers', name='Weekly Average'))

    fig.add_trace(
        go.Scatter(x=df.index, y=df['Monthly_average'], mode='lines+markers', name='Monthly Average'))


    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )


    # JSON for plotting
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/', methods = ['GET'])
def index():

    countryList = stockList['Country'].unique().tolist()
    exchangeList = []

    graph = []

    return render_template("index.html", 
                plot=graph,
                countryList=countryList,
                exchange=exchangeList,
                selectedStocks=[])

@app.route('/updateCountry', methods=['GET', 'POST'])
def updateCountry():
    value = request.get_json()
    countryList = stockList[stockList['Country'] == value]
   
    exchanges = countryList['Exchange'].unique().tolist()
    
    return jsonify(render_template('exchangeDropdown.html', exchange=exchanges))

@app.route('/updateExchange', methods=['GET', 'POST'])
def updateExchange():
    value = request.get_json()
    exchangeList = stockList[stockList['Exchange'] == value]
    stocks = exchangeList['Name'].tolist()

    return jsonify(render_template('stockList.html',
             selectedStocks=stocks))

@app.route('/updateGraph', methods=['GET', 'POST'])
def updateGraph():

    value = request.get_json()
    stock = stockList[stockList['Exchange']==value['exchange']]
    stock = stock[stock['Name']==value['stock']]
    symbol = stock['Ticker'].to_string().split(' ')[-1]

    graphJSON = create_graph(symbol)

    return str(graphJSON)

if __name__ == '__main__':
    app.run(port=os.environ.get("PORT", 5000), host='0.0.0.0', debug=False, threaded=True)