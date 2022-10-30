from init import *

import dash
from dash import Dash, html, dcc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
#from datetime import datetime as date
#import pandas as pd
#import scipy.stats
#from colour import Color
from dash.dependencies import Input, Output, State
from time import sleep
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
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
    price_history = yf.Ticker(symbol).history(period=period,interval=interval,actions=False)
    progression = get_365_days(price_history)
    current_stock_view = go.Figure()
    current_stock_view.add_trace(go.Scatter(
        x=datelist,
        y=progression,
        line=dict(color='green')))
    current_stock_view.update_layout(font_size=15,hovermode='x',xaxis_title='Date',yaxis_title='Share Value (USD)',title={'text':stock_lookup[symbol],'x':0.5,'xanchor':'center'})
    return current_stock_view


current_stock_view = get_raw_stock_graph(SS.current_view)

current_view_dropdown = html.Div([
    dcc.Dropdown(
        id='current_view_dropdown',
        options=stock_symbols,
        value='AAPL',
        style={'font-size':'120%','height':'300%','overflowY':'2px'})])

vote_button = html.Div([html.Button('VOTE',id='vote',n_clicks=0)])



def get_cumulative(symbols,dic,period:str='1y',interval:str='1d',group:bool=True):
    progressions = []
    cumul = go.Figure()
    for i,symbol in enumerate(symbols):
        price_history = yf.Ticker(symbol).history(period=period,interval=interval,actions=False)
        progression = get_365_days(price_history)
        line = [round(dic[symbol][i] * e,2) for i,e in enumerate(progression)]
        cumul.add_trace(go.Scatter(
            x=datelist,
            y=line,
            name=symbol,
            stackgroup='one'))
    if group: title = 'Cumulative Value of Group Held Shares'
    else: title = 'Cumulative Value of Personal Held Shares (Share number clamps to possible values)'
    cumul.update_layout(font_size=15,hovermode='x',xaxis_title='Date',yaxis_title='Cumulative Share Value (USD)',title={'text':title,'x':0.5,'xanchor':'center'})
    return cumul

cumulative_view = get_cumulative([stock for stock in SS.heldstocks],SS.allstocks)
self_cumulative = get_cumulative([stock for stock in SS.selfshares],SS.selfshares,group=False)

flavor_text_1 = html.Div(id='flavortext1',children=f'You have {SS.allstocks[SS.current_view][-1]} shares of {SS.current_view}.')
flavor_text_2 = html.Div(id='flavortext2',children='')

voter_1 = html.Div(id='voter1',children='')
voter_3 = html.Div(id='voter3',children='')
voter_5 = html.Div(id='voter5',children='',style={'font-size':'20px'})

vote_button = html.Div(html.Button(id='votebutton',style={'font-size':'50px'},children='VOTE!'))

add_share = html.Div(html.Button(id = 'addshare',style={'font-size':'20px','display': 'inline-block'},children='▲'))
double_add = html.Div(html.Button(id='doubleadd',style={'font-size':'30px'},children='⯭'))
double_remove = html.Div(html.Button(id='doubleremove',style={'font-size':'30px'},children='⯯'))
remove_share = html.Div(html.Button(id='removeshare',style={'font-size':'20px','display': 'inline-block'},children='▼'))
share_count = html.Div(id = 'sharecount',style={'font-size':'50px','display': 'inline-block'},children=SS.sc)

@app.callback(
Output('sharecount','children'),
[Input('addshare','n_clicks'),Input('removeshare','n_clicks'),Input('doubleadd','n_clicks'),Input('doubleremove','n_clicks'),Input('current_view_dropdown','value')])
def update_share_count(up,down,up2,down2,reset):
    clicked = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'doubleadd' in clicked: SS.sc += 5
    elif 'addshare' in clicked: SS.sc += 1
    elif 'removeshare' in clicked: SS.sc -= 1
    elif 'doubleremove' in clicked: SS.sc -= 5
    elif 'current_view_dropdown' in clicked: SS.sc = 0
    price_history = yf.Ticker(SS.current_view).history(period='1mo',interval='1d',actions=False)
    L = list(round((price_history['High']+price_history['Low'])/2,2))
    price = L[-1]
    M = SS.budget // price
    SS.sc = min(M,SS.sc)
    shares = -1*SS.allstocks[SS.current_view][-1]
    SS.sc = max(shares,SS.sc)
    return f'{SS.sc} ({-(price*SS.sc):+,.2f})'

@app.callback(
Output('flavortext1','children'),
[Input('votebutton','n_clicks'),Input('sharecount','children'),Input('current_view_dropdown','value')])#,prevent_initial_call=True)
def hold_vote_1(clicks,value,sym):
    clicked = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'votebutton.n_clicks' in clicked and SS.symbolvotes[sym] == 0:
        SS.uivote(value)
        SS.symbolvotes[sym] = 1
        return f'Waiting for voters for {SS.current_view}...'
    elif 'current_view_dropdown' in clicked: return f'You have {SS.allstocks[SS.current_view][-1]} shares of {SS.current_view}.'
    elif 'sharecount.children' in clicked: return f'You have {SS.allstocks[SS.current_view][-1]} shares of {SS.current_view}.'
    elif SS.symbolvotes[sym] == 1: return 'You already voted on this stock today.'
        
@app.callback(
Output('flavortext2','children'),
[Input('votebutton','n_clicks'),Input('current_view_dropdown','value')],prevent_initial_call=True)
def hold_vote_2(clicks,val):
    sleep(1)
    clicked = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'votebutton' in clicked: return 'Voters with Similar Budgets and Shares Found!'
    elif 'current_view_dropdown' in clicked: return ''

@app.callback(
Output('voter1','children'),
[Input('votebutton','n_clicks'),Input('current_view_dropdown','value')],prevent_initial_call=True)
def hold_vote_2(clicks,val):
    sleep(1)
    clicked = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'votebutton' in clicked: return f'{SS.votes[0][0]} voted {SS.votes[0][1]} : {SS.votes[1][0]} voted {SS.votes[1][1]} : {SS.votes[2][0]} voted {SS.votes[2][1]} : {SS.votes[3][0]} voted {SS.votes[3][1]} '
    elif 'current_view_dropdown' in clicked: return ''

@app.callback(
Output('voter3','children'),
[Input('votebutton','n_clicks'),Input('current_view_dropdown','value')],prevent_initial_call=True)
def hold_vote_2(clicks,val):
    sleep(1)
    clicked = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'votebutton' in clicked: return f'{SS.votes[4][0]} voted {SS.votes[4][1]} : {SS.votes[5][0]} voted {SS.votes[5][1]} : {SS.votes[6][0]} voted {SS.votes[6][1]} : {SS.votes[7][0]} voted {SS.votes[7][1]}'
    elif 'current_view_dropdown' in clicked: return ''

@app.callback(
Output('voter5','children'),
[Input('votebutton','n_clicks'),Input('current_view_dropdown','value')],prevent_initial_call=True)
def hold_vote_2(clicks,val):
    sleep(1)
    clicked = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'votebutton' in clicked: return f'You voted {SS.vote}. The Group voted {SS.toc}.'
    elif 'current_view_dropdown' in clicked: return ''

@app.callback(
Output('current_view_div','children'),
[Input('current_view_dropdown','value')])
def update_current_view(symbol):
    SS.current_view = symbol
    cv = get_raw_stock_graph(symbol)
    return dcc.Graph(id='current_view',figure=cv)

budgets = html.H2(id='budgets',children=f'Group Budget: ${SS.budget:,.2f} _______________ Self Budget: ${SS.sbudg:,.2f}')

@app.callback(
Output('budgets','children'),Output('hist','children'),
[Input('votebutton','n_clicks')])
def update_budgets(symbol):
    sleep(1)
    return f'Group Budget: ${SS.budget:,.2f} _______________ Self Budget: ${SS.sbudg:,.2f}', get_hist()

@app.callback(
Output('group','figure'),Output('self','figure'),
[Input('votebutton','n_clicks')])
def update_graphs(c):
    sleep(1)
    return get_cumulative([stock for stock in SS.heldstocks],SS.allstocks), get_cumulative([stock for stock in SS.selfshares],SS.selfshares,group=False)

def get_hist():
    fig = go.Figure()
    r = 1
    try: r = abs(max(SS.hist)-min(SS.hist))
    except: pass
    fig.add_histogram(x=SS.hist,nbinsx=int(2*r),histnorm='probability',hoverlabel=None,autobinx=True,hoverinfo=None)
    t0 = 0
    try: t0 = -abs(max(SS.hist))
    except: pass
    fig.update_layout(xaxis=dict(tickmode='linear',tick0=t0,dtick=1),xaxis_title='Shares Off From Group Vote',yaxis_title='Frequency',font_size=15,
    title={'text':"Your Vote vs The Group's Vote",'x':0.5,'xanchor':'center'},bargap=0.2)
    return html.Div(dcc.Graph(figure=fig))

hist = get_hist()

save_button = html.Div(children=html.Button(id='save',children='SAVE'))

@app.callback(Output('save','children'),
[Input('save','n_clicks')])
def save(c):
    SS.save('test.txt','test.txt','test.txt','test.txt','test.txt','test.txt')
    return 'SAVE'

# main loop
if __name__ == '__main__':
    print('\nreloaded\n')
    app.title = 'StockTocracy'
    app.layout = html.Div(children=[
    html.H1('StockTocracy', style={'textAlign': 'center','font-family':'Gravitas One','font-size':'70px'}),
    html.Center(children=budgets),
    html.Center(children=html.Div(children=current_view_dropdown,style={'width':'10%'})),
    html.Div(children=dcc.Graph(id='current_view',figure=current_stock_view),id='current_view_div'),
    html.Center(children=flavor_text_1), html.Center(children=flavor_text_2),
    html.Center(children=voter_1), html.Center(children=voter_3), html.Center(children=voter_5),
    html.Center(children=html.Div(children=[double_add,add_share,share_count,remove_share,double_remove],style={'display':'inline-block'})),
    html.Center(children=vote_button),
    html.Div(children=dcc.Graph(id='group',figure=cumulative_view),id='cumulative_view_div'),
    html.Div(children=dcc.Graph(id='self',figure=self_cumulative),id='self_cumulative_div'),
    html.Center(children=hist,id='hist'),
    html.Center(children=save_button)
    ])
    app.run_server(debug=True)