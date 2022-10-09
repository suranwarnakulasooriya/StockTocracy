# internal imports

# 3rd party libraries
from dash import Dash, html, dcc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import scipy.stats
from colour import Color
from dash.dependencies import Input, Output
import pandas_datareader as web
import os
app = Dash('Kromer Tracker')

os.environ["ALPHAVANTAGE_API_KEY"] = "pk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
'''stock.py
stock = web.DataReader("AAPL", "av-daily", start='09/25/22',
#start=datetime(today_y-1,today_m,today_d),
#end=datetime(today_y,today_m,today_d),
end=today_str,
api_key=os.getenv('ALPHAVANTAGE_API_KEY'))'''


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
fig = go.Figure(data=go.Ohlc(x=df['Date'],
                    open=df['AAPL.Open'],
                    high=df['AAPL.High'],
                    low=df['AAPL.Low'],
                    close=df['AAPL.Close']))

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
fig = go.Figure(data=go.Ohlc(x=df['Date'],
                    open=df['AAPL.Open'],
                    high=df['AAPL.High'],
                    low=df['AAPL.Low'],
                    close=df['AAPL.Close']))




# main loop
if __name__ == '__main__':
    #app = Dash('Kromer Tracker')
    app.title = 'Kromer Tracker'

    app.layout = html.Div(children=[
    html.H1(children='Kromer Tracker'),
    dcc.Graph(id='stonk',figure=fig)    
    ])
    app.run_server(debug=True)