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

def get_raw_stock_graph(symbol:str,period:str='1y',interval:str='1d'):
    price_history = yf.Ticker(symbol).history(period=period,interval=interval,actions=False)
    o = list(price_history['Open'])
    h = list(price_history['High'])
    l = list(price_history['Low'])
    c = list(price_history['Close'])
    axis = [datetime.fromtimestamp(pendulum.parse(str(dt)).float_timestamp) for dt in list(price_history.index)]
    current_stock_view = go.Figure(data=go.Ohlc(
        x=axis,
        open=o,
        high=h,
        low=l,
        close=c))
    current_stock_view.update_layout(font_size=15,hovermode='x',xaxis_title='Time',yaxis_title='Share Value (USD)',title={'text':stock_lookup[symbol],'x':0.5,'xanchor':'center'})
    return current_stock_view

current_stock_view = get_raw_stock_graph(SS.current_view)

current_view_dropdown = html.Div([
    dcc.Dropdown(
        id='current_view_dropdown',
        #options=['AAPL','TSLA','NVDA'],
        options=stock_symbols,
        value='AAPL',
        style={'font-size':'120%','height':'300%','overflowY':'2px'})])

def get_cumulative(symbols,dict,period:str='1y',interval:str='1d',group:bool=True):
    progressions = []
    cumul = go.Figure()
    for i,symbol in enumerate(symbols):
        #print(symbol)
        price_history = yf.Ticker(symbol).history(period=period,interval=interval,actions=False)
        progression = list((price_history['High']+price_history['Low'])/2) # average of high and low
        print(len(progression))
        progression = [round(dict[symbol][e]*p,2) for e,p in enumerate(progression)]
        #print(progression)
        if i == 0: axis = [datetime.fromtimestamp(pendulum.parse(str(dt)).float_timestamp) for dt in list(price_history.index)]
        cumul.add_trace(go.Scatter(
            x=axis,
            y=progression,
            name=symbol,
            stackgroup='one'))
    if group: title = 'Cumulative Value of Group Held Shares'
    else: title = 'Cumulative Value of Personal Held Shares (Speculative)'
    cumul.update_layout(font_size=15,hovermode='x',xaxis_title='Time',yaxis_title='Cumulative Share Value (USD)',title={'text':title,'x':0.5,'xanchor':'center'})
    return cumul

cumulative_view = get_cumulative([stock for stock in SS.heldstocks],SS.heldstocks)
self_cumulative = get_cumulative([stock for stock in SS.selfshares],SS.selfshares,group=False)




@app.callback(
Output('current_view_div','children'),
[Input('current_view_dropdown','value')])
def update_current_view(symbol):
    SS.current_view = symbol
    #print(symbol)
    cv = get_raw_stock_graph(symbol)
    return dcc.Graph(id='current_view',figure=cv)


# main loop
if __name__ == '__main__':
    app.title = 'Stock Spectator'

    app.layout = html.Div(children=[
    #html.H1(children='Stock Spectator'),
    html.H1('Stock Spectator', style={'textAlign': 'center','font-family':'Gravitas One'}),
  
    html.Center(children=html.Div(children=current_view_dropdown,style={'width':'10%'})),
    
    html.Div(children=dcc.Graph(id='current_view',figure=current_stock_view),id='current_view_div'),
    html.Div(children=dcc.Graph(id='group',figure=cumulative_view),id='cumulative_view_div'),
    html.Div(children=dcc.Graph(id='self',figure=self_cumulative),id='self_cumulative_div')
    
    
    
    ])
    app.run_server(debug=True)