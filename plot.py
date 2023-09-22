import pandas as pd
import json
import plotly.express as px

with open('colors.json') as json_data:
    colors = json.load(json_data)

temperature = pd.read_csv('data_use/temperature_data_new.csv')
wind = pd.read_csv('data_use/wind_data_new.csv')
sun = pd.read_csv('data_use/sun_data_new.csv')


# capacity = pd.read_csv('new_res/capacity.csv')
# new_capacity = pd.read_csv('new_res/newcapacity.csv')


# capacity['colors'] = capacity['Technology'].map(colors)
# new_capacity['colors'] = capacity['Technology'].map(colors)

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

app = Dash(__name__)


app.layout = html.Div([
    html.H1('EW MOD'),
#     html.P("Select color:"),
#     dcc.Dropdown(
#         id="dropdown",
#         options=['Gold', 'MediumTurquoise', 'LightGreen'],
#         value='Gold',
#         clearable=False,
#     ),
#     dcc.Graph(id="graph"),
#     html.H2('Installed Capacity'),
#     dcc.Graph(figure = go.Figure(
#         data=[go.Bar(x=capacity['Technology'], y=capacity['value'], marker_color = capacity['colors'])])
#     ),
#     html.H2('New Capacity'),
#     dcc.Graph(figure = go.Figure(
#         data=[go.Bar(x=new_capacity['Technology'], y=new_capacity['value'], marker_color = new_capacity['colors'])])
#     )
    dcc.Graph(
    id='temperature-line-plot',
    figure=px.line(temperature, x='hour', y='value', title='Temperature')
    ),
    dcc.Graph(
    id='wind-line-plot',
    figure=px.line(wind, x='hour', y='value', title='Wind')
    ),
    dcc.Graph(
    id='sun-line-plot',
    figure=px.line(sun, x='hour', y='value', title='Sun')
    )
])


# @app.callback(
#     Output("graph", "figure"), 
#     Input("dropdown", "value"))
# def display_color(color):
#     fig = go.Figure(
#         data=go.Bar(y=[2, 3, 1], # replace with your own data source
#                     marker_color=color))
#     return fig




app.run_server(debug=True)