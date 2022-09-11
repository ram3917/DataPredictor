from flask import Flask, render_template

import plotly
import plotly.graph_objects as go

import pandas as pd
import numpy as np
import json

import flask_app.data_collector as dc

app = Flask(__name__, static_folder="./static", template_folder="./static/templates")


def create_graph():
    """
    The following script downloads and plots data from Stock market.
    """
    cols = ["Tata", "Reliance"]
    df = pd.DataFrame(data=None,columns=cols)

    # Get closing price
    # Get closing price
    tata_df = dc.GetStockData("TATAMOTORS.NS")
    df["Tata"] = tata_df['Close'].copy()

    reliance_df = dc.GetStockData("RELIANCE.NS")
    df["Reliance"] = reliance_df['Close'].copy()

    # drop na
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    data = [
        go.Line(
            x=df.index, # assign x as the dataframe column 'x'
            y=df['Tata']
        ),
        go.Line(
            x=df.index, # assign x as the dataframe column 'x'
            y=df['Reliance']
        )
    ]

    # JSON for plotting
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/')
def index():
    graph = create_graph()
    return render_template("index.html", plot=graph)


if __name__ == '__main__':
    app.run()