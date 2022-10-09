from init import *

from dash import Dash, html, dcc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime
#import pandas as pd
#import scipy.stats
#from colour import Color
from dash.dependencies import Input, Output
#import pandas_datareader as web
#import os

app = Dash('Stock Spectator')

# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

def get_raw_stock_graph(stock,period='1y',interval='1d'):
    price_history = yf.Ticker(stock).history(period=period,interval=interval,actions=False)
    o = list(price_history['Open'])
    h = list(price_history['High'])
    l = list(price_history['Low'])
    c = list(price_history['Close'])
    axis = [datetime.fromtimestamp(pendulum.parse(str(dt)).float_timestamp) for dt in list(price_history.index)]
    #time_series = list((price_history['High']+price_history['Low'])/2) # average of high and low
    #return o,h,l,c,axis

    #current_O, current_H, current_L, current_C, current_axis = get_raw_stock_graph(SS.current_view)

    current_stock_view = go.Figure(data=go.Ohlc(
        x=axis,
        open=o,
        high=h,
        low=l,
        close=c))
    current_stock_view.update_layout(hovermode='x',xaxis_title='Time',yaxis_title='Share Value (USD)')
    return current_stock_view

get_raw_stock_graph(SS.current_view)

current_view_dropdown = html.Div([
    dcc.Dropdown(
        id='current_view_dropdown',
        #options=['AAPL','TSLA','NVDA'],
        options=stock_symbols,
        value='AAPL')])

@app.callback(
Output('',''),
[Input('current_view_dropdown','value')])
def update_current_view(symbol):
    SS.current_view = symbol
    return get_raw_stock_graph(symbol)


# main loop
if __name__ == '__main__':
    app.title = 'Stock Spectator'

    app.layout = html.Div(children=[
    #html.H1(children='Stock Spectator'),
    html.H1('Stock Spectator', style={'textAlign': 'center'}),
  
    html.Center(children=html.Div(children=current_view_dropdown,style={'width':'10%'})),
    
    html.Div(children=dcc.Graph(id='current_view',figure=current_stock_view))
    
    
    
    ])
    app.run_server(debug=True)