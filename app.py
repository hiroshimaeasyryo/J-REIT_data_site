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

# Layout
app.layout = html.Div(
    children=[
        html.H1(children='COVID-19 Daily Cases in Japan'),
        dcc.Graph(
            id='graph1',
            figure={
                'data': [
                    {'x': daily_cases.index,
                    'y': daily_cases['counts'],
                    'type': 'bar',
                    'name': '新規感染者数'},
                    {'x': daily_cases.index,
                    'y': daily_cases['trend'],
                    'type': 'line',
                    'name': '7日移動平均'}
            ],
            'layout': {
                'title': '東京都内新規感染者数'
            }
        }
    )
])

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)