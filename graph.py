from house import *

from dash import Dash, html, dcc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import scipy.stats
from colour import Color
from dash.dependencies import Input, Output

def make_cumulative(t):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t[::-1],y=E,name='Electricity',stackgroup='one'))
    fig.add_trace(go.Scatter(x=t[::-1],y=F,name='Food',stackgroup='one'))
    fig.add_trace(go.Scatter(x=t[::-1],y=W,name='Waste',stackgroup='one'))
    fig.add_trace(go.Scatter(x=t[::-1],y=P,name='Purchases',stackgroup='one'))
    fig.add_trace(go.Scatter(x=t[::-1],y=La,name='Lawn',stackgroup='one'))
    for i,car in enumerate(house.cars):
        fig.add_trace(go.Scatter(x=t[::-1],y=[round(point/1e3,2) for point in car.datapoints],name=f'Car {i+1}',stackgroup='one'))
    if house.has_stove:
        fig.add_trace(go.Scatter(x=t[::-1],y=St,name='Stove',stackgroup='one'))
    if house.has_water:
        fig.add_trace(go.Scatter(x=t[::-1],y=Wt,name='Water Heating',stackgroup='one'))
    fig.update_layout(hovermode='x',title_text='Cumulative Emissions',xaxis_title='Day',yaxis_title='CO₂e (kg)')
    return fig

def make_pie(t):
    datalists = [E[-t:],F[-t:],W[-t:],P[-t:],La[-t:]]
    labels = ['Electricity','Food','Waste','Purchases','Lawn']
    if house.has_stove:
        datalists.append(St[-t:])
        labels.append('Stove')
    if house.has_water:
        datalists.append(Wt[-t:])
        labels.append('Water Heating')
    for i,car in enumerate(house.cars):
        labels.append(f'Car {i+1}')
        data = [point/1e3 for point in car.datapoints[-t:]]
        datalists.append(data)
    totals = []
    for l in datalists:
        totals.append(sum(l))
    totals = [round(total/1e3,2) for total in totals]
    fig = go.Figure(data=[go.Pie(labels=labels, values=totals, title='Factors in GHG Emissions')])
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return fig

def name_to_figure(ty:str,name:str):
    if ty == 'cum':
        return make_cumulative(listdays(ts(name)))
    elif ty == 'pie':
        return make_pie(ts(name))

timeframe = 'y'
timeframe = ts(timeframe)
time = listdays(timeframe)

house = House(cars=2,people=3,gas_stove=True,water_heating=True)
house.gen_data(timeframe)

app = Dash('GreenHouse')
app.title = 'GreenHouse'

# color scale
colors = list(Color('red').range_to(Color('green'),100))[::-1]
colors = [color.hex_l for color in colors]

# house total
gross_frame = pd.DataFrame({
    "Day": time,
    "CO₂e (Tonnes)": [house.daily(day) for day in range(timeframe)]})
gross_fig = px.scatter(gross_frame, x="Day", y="CO₂e (Tonnes)",color="CO₂e (Tonnes)",color_continuous_scale=colors,title='Daily Emissions of the House',hover_name='CO₂e (Tonnes)',hover_data=['Day'])
gross_fig.update_coloraxes(showscale=False)
gross_fig.update_layout(hovermode='x')

# electricity
E = [0 for _ in range(timeframe)]
for light in house.lights:
    for i,val in enumerate(light.datapoints[-timeframe:]): E[i] += val/1e3
E = [round(_,2) for _ in E]

# food
F = [0 for _ in range(timeframe)]
for mouth in house.mouths:
    for i,val in enumerate(mouth.datapoints[-timeframe:]): F[i] += val/1e3
F = [round(_,2) for _ in F]

# waste
W = [0 for _ in range(timeframe)]
for trash in house.trash:
    for i,val in enumerate(trash.datapoints[-timeframe:]): W[i] += val/1e3
W = [round(_,2) for _ in W]

# purchases
P = [0 for _ in range(timeframe)]
for wallet in house.wallets:
    for i,val in enumerate(wallet.datapoints[-timeframe:]): P[i] += val/1e3
P = [round(_,2) for _ in P]

# stove + water + lawn
St = [0 for _ in range(timeframe)]
Wt = [0 for _ in range(timeframe)]
La = [0 for _ in range(timeframe)]
if house.has_stove:
    for i,val in enumerate(house.stove.datapoints[-timeframe:]): St[i] += round(val/1e3,2)
if house.has_water:
    for i,val in enumerate(house.water.datapoints[-timeframe:]): Wt[i] += round(val/1e3,2)
for i,val in enumerate(house.lawn.datapoints[-timeframe:]): La[i] += round(val/1e3,2)

# dropdowns
cum_dropdown = html.Div([
    dcc.Dropdown(
        id='cum_dropdown',
        options=['1y','6m','3m','1m'],
        value='1y')])
pie_dropdown = html.Div([
    dcc.Dropdown(
        id='pie_dropdown',
        options=['1y','6m','3m','1m'],
        value='1y')])

# plots
cum_plot = html.Div(dcc.Graph(figure=name_to_figure('cum','1y')),id='cum_plot')
pie_plot = html.Div(dcc.Graph(figure=name_to_figure('pie','1y')),id='pie_plot')

@app.callback(
Output('cum_plot', 'children'),
[Input('cum_dropdown', 'value')])
def update_cum(fig_name):
    return dcc.Graph(figure=name_to_figure('cum',fig_name))

@app.callback(
Output('pie_plot', 'children'),
[Input('pie_dropdown', 'value')])
def update_pie(fig_name):
    return dcc.Graph(figure=name_to_figure('pie',fig_name))

app.layout = html.Div(children=[
    html.H1(children='GreenHouse'),
    dcc.Graph(id='house',figure=gross_fig),
    cum_dropdown, cum_plot,
    pie_dropdown, pie_plot])

if __name__ == '__main__':
    app.run_server(debug=True)