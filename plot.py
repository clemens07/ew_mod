import pandas as pd
import json
import plotly.express as px

with open('colors.json') as json_data:
    colors = json.load(json_data)

temperature = pd.read_csv('data_use/temperature_data_new.csv')
wind = pd.read_csv('data_use/wind_data_new.csv')
sun = pd.read_csv('data_use/sun_data_new.csv')

storage_level = pd.read_csv('results/storage_level.csv')
production = pd.read_csv('results/production.csv')


# capacity = pd.read_csv('new_res/capacity.csv')
# new_capacity = pd.read_csv('new_res/newcapacity.csv')

storage_level['colors'] = storage_level['Technology'].map(colors)
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
    ),
    html.H3("Storage Level"),
    
    # Dropdown to select a technology
    dcc.Dropdown(
        id='tech-dropdown',
        options=[{'label': tech, 'value': tech} for tech in storage_level['Technology'].unique()],
        value=storage_level['Technology'].unique(),
        multi=True  # Allow multiple selections
    ),
    
    # Plotly figure to display the data
    dcc.Graph(id='tech-plot'),

    html.H1("Production Dash Plot"),
    
    # Dropdown to select a technology
    dcc.Dropdown(
        id='production-dropdown',
        options=[{'label': tech, 'value': tech} for tech in production['Technology'].unique()],
        value=production['Technology'].unique(),
        multi=True  # Allow multiple selections
    ),
    
    # Plotly figure to display the data
    dcc.Graph(id='production-plot')
])

    # Define a callback to update the plot based on the selected technology
@app.callback(
    Output('tech-plot', 'figure'),
    Input('tech-dropdown', 'value')
)
def update_plot(selected_techs):
    filtered_df = storage_level[storage_level['Technology'].isin(selected_techs)]
    fig = px.bar(filtered_df, x='Hour', y='value', color='Technology', labels={'Hour': 'Hour', 'value': 'Sum of Value'}, title='Sum of Value by Technology')
    return fig

@app.callback(
    Output('production-plot', 'figure'),
    Input('production-dropdown', 'value')
)
def update_production_plot(selected_techs):
    filtered_df = production[production['Technology'].isin(selected_techs)]
    fig = px.bar(filtered_df, x='Hour', y='value', color='Technology', labels={'Hour': 'Hour', 'value': 'Production Value'}, title='Production Value by Technology')
    return fig


# @app.callback(
#     Output("graph", "figure"), 
#     Input("dropdown", "value"))
# def display_color(color):
#     fig = go.Figure(
#         data=go.Bar(y=[2, 3, 1], # replace with your own data source
#                     marker_color=color))
#     return fig




app.run_server(debug=True)