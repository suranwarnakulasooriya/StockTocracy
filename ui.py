from init import *

from dash import Dash, html, dcc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
#from datetime import datetime as date
#import pandas as pd
#import scipy.stats
#from colour import Color
from dash.dependencies import Input, Output
#from pandas import date_range as dr
#import pandas_datareader as web
#import os

#today_y, today_m, today_d = datetime.today().year, datetime().today().month, datetime.today().day

#today_y = date.today().year
#today_m = date.today().month
#today_d = date.today().day

app = Dash('StockTocracy')

# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

def get_raw_stock_graph(symbol:str,period:str='1y',interval:str='1d'):
    '''
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
    current_stock_view.update_layout(font_size=15,hovermode='x',xaxis_title='Date',yaxis_title='Share Value (USD)',title={'text':stock_lookup[symbol],'x':0.5,'xanchor':'center'})
    return current_stock_view
    '''
    price_history = yf.Ticker(symbol).history(period=period,interval=interval,actions=False)
    #axis = [datetime.fromtimestamp(pendulum.parse(str(dt)).float_timestamp) for dt in list(price_history.index)]
    #axis = dr(date(today_y-1,today_m,today_d),date(today_y,today_m,today_d),freq='D')
    progression = get_365_days(price_history)
    current_stock_view = go.Figure()
    current_stock_view.add_trace(go.Scatter(
        x=datelist,
        y=progression,
        line=dict(color='green')
    ))
    current_stock_view.update_layout(font_size=15,hovermode='x',xaxis_title='Date',yaxis_title='Share Value (USD)',title={'text':stock_lookup[symbol],'x':0.5,'xanchor':'center'})
    return current_stock_view


current_stock_view = get_raw_stock_graph(SS.current_view)

current_view_dropdown = html.Div([
    dcc.Dropdown(
        id='current_view_dropdown',
        #options=['AAPL','TSLA','NVDA'],
        options=stock_symbols,
        value='AAPL',
        style={'font-size':'120%','height':'300%','overflowY':'2px'})])

vote_button = html.Div([
    html.Button('VOTE',id='vote',n_clicks=0)
])



def get_cumulative(symbols,dic,period:str='1y',interval:str='1d',group:bool=True):
    progressions = []
    cumul = go.Figure()
    for i,symbol in enumerate(symbols):
        #print(symbol)i sdfoisbandfoiabsdfoiabsd
        price_history = yf.Ticker(symbol).history(period=period,interval=interval,actions=False)
        #progression = list((price_history['High']+price_history['Low'])/2) # average of high and low
        #progression = [randint(140,190) for _ in range(364)]
        #print(len(progression))
        progression = get_365_days(price_history)
        #progression = [round(e*p,2) for e,p in enumerate(progression)]
        
        #line = []
        line = [round(dic[symbol][i] * e,2) for i,e in enumerate(progression)]
        #for i,e in enumerate(progression):
        #    print(dic[symbol][i],end = ' ')
        #    line.append(round(dic[symbol][i] * e,2))
        #print()
        
        #print(progression)
        #if i == 0: axis = [datetime.fromtimestamp(pendulum.parse(str(dt)).float_timestamp) for dt in list(price_history.index)]
        
        cumul.add_trace(go.Scatter(
            x=datelist,
            y=line,
            name=symbol,
            stackgroup='one'))
    if group: title = 'Cumulative Value of Group Held Shares'
    else: title = 'Cumulative Value of Personal Held Shares (Speculative)'
    cumul.update_layout(font_size=15,hovermode='x',xaxis_title='Date',yaxis_title='Cumulative Share Value (USD)',title={'text':title,'x':0.5,'xanchor':'center'})
    return cumul

cumulative_view = get_cumulative([stock for stock in SS.heldstocks],SS.allstocks)
self_cumulative = get_cumulative([stock for stock in SS.selfshares],SS.selfshares,group=False)

#vote_box = html.Div(
#    children='No Vote Held Yet',
#    id='votebox')

#cast_vote = html.Div([
#    dcc.Input(
#        id='vote',
#        placeholder='Enter how many shares you want to buy, insert a negative to sell.'
#    )])

flavor_text = html.Div(
    id='flavor_text',
    children='No Vote Held Yet'
)

vote_button = html.Div(
    html.Button(
        id='votebutton',
        #style={'width':'100%','height':'100%'},
        #type='VOTE!'
    )
)

#@app.callback(
#Output('votebox','children'),
#[Input('vote','value')])
#def hold_vote(vote):
#    return vote


@app.callback(
Output('current_view_div','children'),
[Input('current_view_dropdown','value')])
def update_current_view(symbol):
    SS.current_view = symbol
    #print(symbol)
    cv = get_raw_stock_graph(symbol)
    return dcc.Graph(id='current_view',figure=cv)

#@app.callback(
#Output('votebox','children'),
#[Input('vote','n_clicks')])
#def hold_vote(nc):
#    return SS.current_view


# main loop
if __name__ == '__main__':
    app.title = 'StockTocracy'

    app.layout = html.Div(children=[
    #html.H1(children='Stock Spectator'),
    html.H1('StockTocracy', style={'textAlign': 'center','font-family':'Gravitas One'}),

    html.H2(f'Budget: ${SS.budget:,.2f}',style={'textAlign': 'center','font-family':'Gravitas One'}),
  
    html.Center(children=html.Div(children=current_view_dropdown,style={'width':'10%'})),
    
    html.Div(children=dcc.Graph(id='current_view',figure=current_stock_view),id='current_view_div'),
    
    html.Center(children=flavor_text),
    html.Center(children=vote_button),
    #html.Center(children=vote_button),

    #html.Center(children=html.Div(children=comparitive_view_dropdown,style={'width':'10%'})),
    
    html.Div(children=dcc.Graph(id='group',figure=cumulative_view),id='cumulative_view_div'),
    html.Div(children=dcc.Graph(id='self',figure=self_cumulative),id='self_cumulative_div')
    
    
    
    ])
    app.run_server(debug=True)