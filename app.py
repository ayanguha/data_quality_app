import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import os

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime
from datetime import timedelta
import plotly.express as px
import random


app = dash.Dash(
    __name__,
    url_base_pathname='/dev/',
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Data Quality Framework"
#app.server.secret_key = os.environ.get('secret_key', 'secret')
server = app.server

domains = 10

# Dictionary of Domains
list_of_domains = [ "domain_" + str(d) for d in range(domains)]
list_of_dimensions = ['Completeness', 'Conformity', 'Consistency', 'Integrity', 'Timeliness', 'Uniqueness']

# Initialize data frame
def base_data():
    today = datetime.today()
    start = today - timedelta(days=30)
    end = today - timedelta(days=1)
    dt = start
    df = []

    while dt <= end:
        mld = model_level_data()
        for m in mld:
            m['run_date'] = dt.strftime('%Y-%m-%d')
            m['run_date_sort'] = dt.strftime('%Y%m%d')

            df.append(m)
        dt = dt + timedelta(days=1)
    print(m)
    return df

def model_level_data():

    models = 500
    df = []

    for m in range(models):
        domain = m%domains
        domain_name = "domain_" + str(domain)

        pass_val = random.randint(20,50)
        fail_val = random.randint(20,50)
        model_name = "model_" + str(m)

        dimension = random.choice(list_of_dimensions)
        df.append({'status': 'Pass','value': pass_val,'dimension': dimension,'domain': domain_name,'model': model_name})
        df.append({'status': 'Fail','value': fail_val,'dimension': dimension,'domain': domain_name,'model': model_name})

    return df

def domain_dimesion():

    domains = 10
    df = []
    for d in range(domains):
        domains_name = "domain_" + str(d)
        for dim in list_of_dimensions:
            pass_val = round(random.random(),2)
            fail_val = 1 - pass_val
            token = {'status': 'Pass', 'value': pass_val, 'dimension': dim, 'domain': domains_name}
            df.append(token)
            token = {'status': 'Fail', 'value': fail_val, 'dimension': dim, 'domain': domains_name}
            df.append(token)


    return df

data = domain_dimesion()
model_data = model_level_data()
base_data = base_data()


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
                                src=app.get_asset_url("slalom-logo.png"),
                            ),
                            href="https://plotly.com/dash/",
                        ),
                        html.H2("DQF"),

                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=datetime(2020, 1, 1),
                                    max_date_allowed=datetime(2044, 12, 12),
                                    initial_visible_month=datetime(2020, 1, 1),
                                    date=datetime(2020, 4, 1).date(),
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
                                        dcc.Graph(id="dimension-graph1" ),
                                        style={'display': 'inline-block'},
                                        className="four columns  bg-grey",
                                    ),
                                    html.Div(
                                        dcc.Graph(id="dimension-graph2" ),
                                        style={'display': 'inline-block'},
                                        className="four columns  bg-grey",
                                    ),
                                    html.Div(
                                        dcc.Graph(id="dimension-graph3" ),
                                        style={'display': 'inline-block'},
                                        className="four columns  bg-grey",
                                    )


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
      Output("test-trend", "figure")
    ],
    [Input("domain-dropdown", "value")]
    )
def update_pie_chart(domain):
    color_discrete_map={'Pass':'green', 'Fail':'red'}
    selected_data = [d for d in data if d['domain'] == domain]

    fig1 = px.line_polar(selected_data,
                   r="value", theta="dimension",
                   color="status",
                   template="plotly_dark",
                   line_close=True,
                   color_discrete_map=color_discrete_map,
                   title="Dimension-wise Quality Status")

    fig2 = px.bar_polar(selected_data,
                   r="value", theta="dimension",
                   color="status",
                   template="plotly_dark",
                   color_discrete_map=color_discrete_map,
                   title="Dimension-wise Quality Status")

    selected_model_data = [d for d in model_data if d['domain'] == domain]

    fig3 = px.bar(selected_model_data,
                  x='value', y='model',
                  color = 'status', color_discrete_map=color_discrete_map,
                  orientation = 'h',
                  template="plotly_dark",
                  title="Model-Level Quality Status")

    selected_base_data = [d for d in base_data if d['domain'] == domain]

    fig4 = px.bar(selected_base_data,
                  x='run_date', y='value',
                  color = 'status', color_discrete_map=color_discrete_map,
                  template="plotly_dark",
                  barmode='group',
                  title="Trend")


    return [fig1, fig2, fig3, fig4]





if __name__ == "__main__":
    app.run_server(debug=True)
