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










# main loop
if __name__ == '__main__':
    app = Dash('Kromer Tracker')
    app.title = 'Kromer Tracker'

    app.layout = html.Div(children=[
    html.H1(children='Kromer Tracker'),
    
    ])
    app.run_server(debug=True)