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
    #routes_pathname_prefix="/dash/",
    #requests_pathname_prefix="/dev/dash/",
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Data Quality Framework"
#app.server.secret_key = os.environ.get('secret_key', 'secret')
server = app.server

data = pd.read_csv('data.csv',sep='|')
list_of_domains = data['domain'].unique().tolist()



card1 = dbc.Card(
            [dbc.CardBody(
                         [
                         html.Div([html.H6("Total Number of Tests"),html.H4("Card Data 1", id="card_data11")], style={"border-style": "solid"}),
                         html.Div(html.P()),
                         html.Div([html.H6("Passed"), html.H4("Card Data 2", id="card_data12")], style={"border-style": "solid"}),
                         html.Div(html.P()),
                         html.Div([html.H6("Failed"),html.H4("Card Data 2", id="card_data13")], style={"border-style": "solid"})
                         ]
                     )] ,style={"width": "18rem"}
            )
card2 = dbc.Card(
            [dbc.CardBody(
                         [
                         html.Div([html.H6("Total Execution Time"), html.H4("Card Data 1", id="card_data21")], style={"border-style": "solid"}),
                         html.Div(html.P()),
                         html.Div([html.H6("Domain"),html.H4("Domain", id="card_data22")], style={"border-style": "solid"})
                         ]
                     ),
            ] ,style={"width": "18rem"}
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
                                        card1,
                                        style={'display': 'inline-block'},
                                        className="two columns  bg-grey",
                                    ),
                                    html.Div(
                                        card2,
                                        style={'display': 'inline-block'},
                                        className="two columns  bg-grey",
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
    [ Output("card_data11", "children"),
      Output("card_data12", "children"),
      Output("card_data13", "children"),
      Output("card_data21", "children"),
      Output("card_data22", "children"),
      Output("dimension-graph2", "figure"),
      Output("dimension-graph3", "figure"),
      Output("test-trend", "figure")
    ],
    [Input("domain-dropdown", "value")]
    )
def update_chart(domain):
    color_discrete_map={'Pass':'#50C878', 'Fail':'#C11B17'}
    latest_date = data.run_date_time.max()
    selected_base_data = data[data.domain == domain]
    latest_data = selected_base_data[selected_base_data.run_date_time == latest_date]

    totals = latest_data.groupby(['run_date_time','dimension'])[['test_case_no']].count().reset_index().rename(columns={'test_case_no':'total_test_case_no'})
    status_totals = latest_data.groupby(['run_date_time','dimension','status'])[['test_case_no']].count().reset_index()

    dimension_view = status_totals.merge(totals, how='inner', on=['run_date_time','dimension'])
    dimension_view['pct'] = round(dimension_view.test_case_no/dimension_view.total_test_case_no * 100,2)


    fig2 = px.bar(dimension_view,
                   x="pct", y="dimension",
                   color="status",
                   orientation = 'h',
                   barmode = 'group',
                   template="plotly_dark",
                   color_discrete_map=color_discrete_map,
                   title="Dimension-wise Quality Status")

    model_view = latest_data.groupby(['model', 'status'])[['test_case_no']].count().reset_index()
    fig3 = px.bar(model_view,
                  x='test_case_no', y='model',
                  color = 'status', color_discrete_map=color_discrete_map,
                  orientation = 'h',
                  template="plotly_dark",
                  title="Model-Level Quality Status")

    trend_view = selected_base_data.groupby(['run_date_time', 'status'])[['test_case_no']].count().reset_index()

    fig4 = px.area(trend_view,
                  x='run_date_time', y='test_case_no',
                  color = 'status', color_discrete_map=color_discrete_map,
                  template="plotly_dark",
                  title="Trend")

    tdf = latest_data.groupby(['status'])[['test_case_no']].count().reset_index().rename(columns={'test_case_no':'total_test_case_no'})
    failed = tdf[tdf.status == 'Fail'].reset_index().total_test_case_no[0]
    passed = tdf[tdf.status == 'Pass'].reset_index().total_test_case_no[0]
    total_tests = passed + failed

    latest_exec_time = latest_data.execution_time_in_seconds.sum()

    card_data11 = html.H4(f"{total_tests}", className="card-text")
    card_data12 = html.H4(f"{passed}", className="card-text")
    card_data13 = html.H4(f"{failed}", className="card-text")
    card_data21 = html.H4(f"{latest_exec_time}", className="card-text")
    card_data22 = html.H4(f"{domain}", className="card-text")


    return [card_data11,
            card_data12,
            card_data13,
            card_data21,
            card_data22,
            fig2, fig3, fig4]





if __name__ == "__main__":
    app.run_server(debug=True)
