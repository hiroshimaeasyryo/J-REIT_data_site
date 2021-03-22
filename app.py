import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from bs4 import BeautifulSoup
import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
import itertools
from sklearn import linear_model
import statsmodels.api as sm
import requests
from rq import Queue
from redis import Redis
from worker import conn
from utils import load_tky_data, load_kan_data, load_osk_data, load_hkd_data
import time


app = dash.Dash(__name__)


redis_conn = Redis()
q = Queue(connection=redis_conn)

# Tokyo data
tky_job = q.enqueue(load_tky_data, 'https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv')
# Kanagawa data
kan_job = q.enqueue(load_kan_data, 'https://www.pref.kanagawa.jp/osirase/1369/data/csv/patient.csv')
# Osaka data
osk_job = q.enqueue(load_osk_data, 'https://covid19-osaka.info/data/summary.csv')
# Hokkaido data
hkd_job = q.enqueue(load_hkd_data, 'https://www.harp.lg.jp/opendata/dataset/1369/resource/2853/covid19_data.csv')


time.sleep(25)
daily_cases = tky_job.result
kan_daily_cases = kan_job.result
osk_daily_cases = osk_job.result
hkd_daily_cases = hkd_job.result


# Layout
app.layout = html.Div(
                children=[
                    html.H2(children='COVID-19 Daily Cases in Japan'),
                    html.Div(
                        children=[
                            dcc.Graph(
                                id='graph1',
                                figure={
                                    'data':[
                                        {'x': daily_cases.index,
                                        'y': daily_cases['counts'],
                                        'type': 'bar',
                                        'name': '新規感染者数'},
                                        {'x': daily_cases.index,
                                        'y': daily_cases['trend'],
                                        'type': 'line',
                                        'name': '7日移動平均'}
                                            ],
                                    'layout': {'title': '東京都内新規感染者数'}
                                        }
                            ),
                            dcc.Graph(
                                id = "graph2",
                                figure = {
                                    'data':[
                                        {'x': kan_daily_cases.index,
                                        'y': kan_daily_cases['counts'],
                                        'type': 'bar',
                                        'name': '新規感染者数'},
                                        {'x': kan_daily_cases.index,
                                        'y': kan_daily_cases['trend'],
                                        'type': 'line',
                                        'name': '7日移動平均'}
                                    ],
                                    'layout': {'title': '神奈川県内新規感染者数'}
                                }
                            )
                        ],
                        style = {'display': 'flex'}
                    ),
                    html.Div(
                        children=[
                            dcc.Graph(
                                id = "graph3",
                                figure = {
                                    'data':[
                                        {'x': osk_daily_cases.index,
                                        'y': osk_daily_cases['counts'],
                                        'type': 'bar',
                                        'name': '新規感染者数'},
                                        {'x': osk_daily_cases.index,
                                        'y': osk_daily_cases['trend'],
                                        'type': 'line',
                                        'name': '7日移動平均'}
                                            ],
                                    'layout': {'title': '大阪府内新規感染者数'}
                                        }
                                    ),
                            dcc.Graph(
                                id = "graph4",
                                figure = {
                                    'data':[
                                        {'x': hkd_daily_cases.index,
                                        'y': hkd_daily_cases['日陽性数'],
                                        'type': 'bar',
                                        'name': '新規感染者数'},
                                        {'x': hkd_daily_cases.index,
                                        'y': hkd_daily_cases['trend'],
                                        'type': 'line',
                                        'name': '7日移動平均'}
                                            ],
                                    'layout': {'title': '北海道内新規感染者数'}
                                        }
                                    ),
                        ],
                        style = {'display': 'flex'}
                    )
                ]
            )


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)