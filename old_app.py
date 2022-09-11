import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt
import plotly.express as px
import random


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Data Quality Framework"
server = app.server

domains = 10

# Dictionary of Domains
list_of_domains = [ "domain_" + str(d) for d in range(domains)]
list_of_dimensions = ['Completeness', 'Conformity', 'Consistency', 'Integrity', 'Timeliness', 'Uniqueness']

# Initialize data frame

def domain_dimesion():

    domains = 10
    df = []
    for d in range(domains):
        domains_name = "domain_" + str(d)
        for dim in list_of_dimensions:
            token = {'status': 'Pass', 'value': random.random(), 'dimension': dim, 'domain': domains_name}
            df.append(token)
            token = {'status': 'Fail', 'value': random.random(), 'dimension': dim, 'domain': domains_name}
            df.append(token)


    return df

data = domain_dimesion()


totalList = np.array(data)

card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Card title", className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),


            ]
        ),
    ],
    style={"width": "18rem"},
)

# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="three columns div-user-controls",
                    children=[
                        html.A(
                            html.Img(
                                className="logo",
                                src=app.get_asset_url("dash-logo-new.png"),
                            ),
                            href="https://plotly.com/dash/",
                        ),
                        html.H2("DQF"),

                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=dt(2020, 1, 1),
                                    max_date_allowed=dt(2044, 12, 12),
                                    initial_visible_month=dt(2020, 1, 1),
                                    date=dt(2020, 4, 1).date(),
                                    display_format="MMMM D, YYYY",
                                    style={"border": "0px solid black"},
                                )
                            ],
                        ),
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[

                                        dcc.Dropdown(
                                            id="domain-dropdown",
                                            options=
                                            [
                                                {"label": i, "value": i}
                                                for i in list_of_domains
                                            ],
                                             value = list_of_domains[0],
                                        )
                                    ],
                                ),

                            ],
                        ),
                        html.Div(
                            card
                        ),
                        html.P(id="total-tests"),


                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="nine columns div-for-charts bg-grey",
                    children=[
                        html.H2(
                            "Data Quality Dimension View"
                        ),
                        html.Div
                        (
                        children = [
                                    html.Div(
                                        dcc.Graph(id="dimension-graph1", ),
                                        style={'display': 'inline-block'},
                                        className="three columns  bg-grey",
                                    ),
                                   html.Div(
                                        dcc.Graph(id="dimension-graph2", ),
                                        style={'display': 'inline-block'},
                                        className="three columns  bg-grey",
                                    ),
                                    html.Div(
                                        dcc.Graph(id="dimension-graph3", ),
                                        style={'display': 'inline-block'},
                                        className="three columns  bg-grey",
                                    ),
                                    html.Div(
                                        dcc.Graph(id="dimension-graph4", ),
                                        className="three columns  bg-grey",
                                        style={'display': 'inline-block'},
                                    ),
                                    html.Div(
                                        dcc.Graph(id="dimension-graph5", ),
                                        className="three columns  bg-grey",
                                        style={'display': 'inline-block'},
                                    ),
                                    html.Div(
                                        dcc.Graph(id="dimension-graph6", ),
                                        className="three columns  bg-grey",
                                        style={'display': 'inline-block'},
                                    ),


                        ]),
                        html.Div(
                            className="text-padding",
                            children=[
                                "Data Quality Trends"
                            ],
                        ),
                        dcc.Graph(id="test-trend"),
                    ],
                ),
            ],
        )
    ]
)


@app.callback(
    [ Output("dimension-graph1", "figure"),
      Output("dimension-graph2", "figure"),
      Output("dimension-graph3", "figure"),
      Output("dimension-graph4", "figure"),
      Output("dimension-graph5", "figure"),
      Output("dimension-graph6", "figure")
    ],
    [Input("domain-dropdown", "value")]
    )
def update_pie_chart(domain):
    color_discrete_map={'Pass':'green', 'Fail':'red'}

    figs = []

    for dim in list_of_dimensions:
        selected_data = [d for d in data if d['domain'] == domain and d['dimension'] == dim]
        fig = px.pie(selected_data,names="status",
                     title=dim,
                     values="value",
                     template='plotly_dark',
                     height=350,
                     color='status',
                     color_discrete_map=color_discrete_map, hole=0.3
                     )
        figs.append(fig)


    return figs





if __name__ == "__main__":
    app.run_server(debug=True)
