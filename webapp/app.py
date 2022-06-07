# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from pandas.core.arrays import categorical
import plotly.express as px
import pandas as pd
import pymongo
from pymongo import MongoClient
from dash.dependencies import Input, Output
import dash_table

app = dash.Dash(__name__)

# mongo connection details

uri = "mongodb+srv://aliu319:LO9UfXxBfDEPPfcQ@aliu319-gt.t7rt0.mongodb.net/test?retryWrites=true&w=majority"
db = "ofet-db"
collection = "devices"

def _connect_mongo(uri, db):
    """ A util for making a connection to mongo """

    conn = MongoClient(uri)
    return conn[db]

def read_mongo(uri, db, collection, query={}, proj={}):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(uri=uri, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query, proj)

    # Expand the cursor and construct the DataFrame
    docs =  list(cursor)
    df_flat = pd.json_normalize(docs)
    # Delete the _id
    # if no_id:
        # del df['_id']

    return df_flat


### QUERIES ###

q1 = {}
proj = {
    "_id": False, 
    "ofet.mobility_cm2_Vs": True, 
    "solution.concentration_mg_ml": True, 
    "solution.solvent.name": True,
    "substrate.surface_modification": True,
    "solution.polymer": True,
    "coating_process.deposition_method": True,
    "substrate.electrode_config": True
}   

df_1 = read_mongo(uri, db, collection, q1, proj)
# print(df_1)

continuous_vars = [
    'solution.polymer.Mn_kDa',
    'solution.polymer.Mw_kDa', 
    'solution.polymer.PDI', 
    'solution.concentration_mg_ml'
]
categorical_vars = [
    'solution.solvent.name', 
    'coating_process.deposition_method', 
    'substrate.surface_modification', 
    'solution.polymer.name', 
    'substrate.electrode_config'
]



# q4_vars = ['solvent_name', 'deposition_method', 'surface_treatment', 'electrode_config']
polymer_names = ['P3HT', 'DPP-DTT']

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
                    value='solution.polymer.Mw_kDa'
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
    Input('mobility-legend', 'value'))
def update_graph(xaxis_column_name, legend):

    fig = px.scatter(
        df_1,
        x=xaxis_column_name,
        y='ofet.mobility_cm2_Vs',
        color=legend
    )
    fig.update_yaxes(type='log')
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')


    return fig

if __name__ == '__main__':
    app.run_server(debug=True)