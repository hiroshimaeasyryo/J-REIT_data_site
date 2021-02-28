import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
import statsmodels.api as sm


app = dash.Dash(__name__)

# Tokyo data
row_data = pd.read_csv('https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv')
by_day = row_data.groupby('公表_年月日')
dates = []
counts = []
for bd in by_day:
    dates.append(bd[0])
    counts.append(len(bd[1]))
daily_cases = pd.DataFrame({'counts':counts} ,index=dates)
datetimes = []
for d in daily_cases.index:
    datetimes.append(datetime.datetime.strptime(d, '%Y-%m-%d'))
daily_cases.index = datetimes
seasonal = sm.tsa.seasonal_decompose(daily_cases.counts, period=7)
daily_cases['trend'] = seasonal.trend

# Kanagawaデータ
kan_row = pd.read_csv('https://www.pref.kanagawa.jp/osirase/1369/data/csv/patient.csv', encoding="shift-jis")
kan_by_day = kan_row.groupby('発表日')
kan_dates = []
kan_counts = []
for bd in kan_by_day:
    kan_dates.append(bd[0])
    kan_counts.append(len(bd[1]))
kan_daily_cases = pd.DataFrame({'counts':kan_counts} ,index=kan_dates)
kan_datetimes = []
for d in kan_daily_cases.index:
    kan_datetimes.append(datetime.datetime.strptime(d, '%Y-%m-%d'))
kan_daily_cases.index = kan_datetimes
kan_seasonal = sm.tsa.seasonal_decompose(kan_daily_cases.counts, period=7)
kan_daily_cases['trend'] = kan_seasonal.trend

# 大阪府データ
osk_row = pd.read_csv('https://covid19-osaka.info/data/summary.csv', encoding="shift-jis")
osk_dates = []
osk_daily_cases = pd.DataFrame({'counts': osk_row['陽性人数']}, index=osk_row['日付'])
osk_daily_cases['counts'] = osk_row['陽性人数'].values
osk_datetimes = []
for d in osk_daily_cases.index:
    osk_datetimes.append(datetime.datetime.strptime(d, '%Y-%m-%d'))
osk_daily_cases.index = osk_datetimes
osk_seasonal = sm.tsa.seasonal_decompose(osk_daily_cases.counts, period=7)
osk_daily_cases['trend'] = osk_seasonal.trend

# Layout
app.layout = html.Div(
    children=[
        html.H1(children='COVID-19 Daily Cases in Japan'),
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
                ),
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
                )
            ]
)

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)