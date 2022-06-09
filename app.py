# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
from pandas.core.arrays import categorical
import plotly.express as px
import pandas as pd
import pymongo
from pymongo import MongoClient
from dash.dependencies import Input, Output
from dash import dash_table
from crud_functions import *
#
app = dash.Dash(__name__)

# mongo connection details

uri = "mongodb+srv://aliu319:LO9UfXxBfDEPPfcQ@aliu319-gt.t7rt0.mongodb.net/test?retryWrites=true&w=majority"
db = "ofet-db"
collection = "sandbox"


### QUERIES ###

q1 = {}
proj = {
    "_id": False
}   
docs = read_mongo_docs(uri, db, collection, q1, proj)
df = pd.json_normalize(docs)
# print(df_1)

continuous_vars = df[df.columns[df.dtypes == 'float64']]

categorical_vars = df[df.columns[df.dtypes == 'object']]



# q4_vars = ['solvent_name', 'deposition_method', 'surface_treatment', 'electrode_config']
polymer_names = ['P3HT']

app.layout = html.Div([

    # Query 1
    
    html.Div([
        html.Div([
            html.H2("Mobility Plot"),
            html.Div([
                html.Label('x-axis'),
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': i, 'value': i} for i in continuous_vars],
                    value='solution.polymer.semiconductor.Mw_kDa'
                ),
            ], style={'width': '45%', 'display': 'inline-block'}),
            html.Div([
                html.Label('y-axis'),
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in continuous_vars],
                    value='ofet.mobility_cm2_Vs'
                ),
            ], style={'width': '45%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Legend'),
                dcc.Dropdown(
                    id='mobility-legend',
                    options=[{'label': i, 'value': i} for i in categorical_vars],
                    value='solution.solvent.name'
                ),
            ], style={'width': '45%', 'display': 'inline-block'}),
            html.Div([
                html.Label('y-axis scale'),
                dcc.Dropdown(
                    id='yscale',
                    options=['linear', 'log'],
                    value='log'
                ),
            ], style={'width': '45%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(
                    id='mobility-graph',
                    # figure=fig
                ), 
            ])
        ], style={'width': '42%', 'display': 'inline-block'}),

        html.Div([], style={'width': '10%', 'display': 'inline-block'}), #spacer


    ]),
    html.Br(),


])

# Callback for Query 1
@app.callback(
    Output('mobility-graph', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('yscale', 'value'),
    Input('mobility-legend', 'value'))
def update_graph(xaxis_column_name, yaxis_column_name, yscale, legend):

    fig = px.scatter(
        df,
        x=xaxis_column_name,
        y=yaxis_column_name,
        color=legend
    )
    fig.update_yaxes(type=yscale)
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')


    return fig

if __name__ == '__main__':
    app.run_server(debug=True)