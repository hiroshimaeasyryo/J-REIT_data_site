import requests
import pandas as pd
import datetime
from sklearn import linear_model
import statsmodels.api as sm
import csv
import io


def load_tky_data(url):
    get_url = requests.get(url)
    tky_row = pd.read_csv(io.BytesIO(get_url.content),sep=",")
    tky_by_day = tky_row.groupby('公表_年月日')
    tky_dates = []
    tky_counts = []
    for bd in tky_by_day:
        tky_dates.append(bd[0])
        tky_counts.append(len(bd[1]))
    tky_datetimes = []
    for d in tky_dates:
        tky_datetimes.append(datetime.datetime.strptime(d, '%Y-%m-%d'))
    tky_daily_cases = pd.DataFrame({'counts':tky_counts} ,index=tky_dates)
    tky_seasonal = sm.tsa.seasonal_decompose(tky_daily_cases.counts, period=7)
    tky_daily_cases['trend'] = tky_seasonal.trend
    return tky_daily_cases

def load_kan_data(url):
    get_url = requests.get(url)
    kan_row = pd.read_csv(io.BytesIO(get_url.content), sep=",", encoding="shift-jis")
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
    return kan_daily_cases

def load_osk_data(url):
    get_url = requests.get(url)
    osk_row = pd.read_csv(io.BytesIO(get_url.content), sep=",", encoding="shift-jis")
    osk_dates = []
    osk_daily_cases = pd.DataFrame({'counts': osk_row['陽性人数']}, index=osk_row['日付'])
    osk_daily_cases['counts'] = osk_row['陽性人数'].values
    osk_datetimes = []
    for d in osk_daily_cases.index:
        osk_datetimes.append(datetime.datetime.strptime(d, '%Y-%m-%d'))
    osk_daily_cases.index = osk_datetimes
    osk_seasonal = sm.tsa.seasonal_decompose(osk_daily_cases.counts, period=7)
    osk_daily_cases['trend'] = osk_seasonal.trend
    return osk_daily_cases

def load_hkd_data(url):
    get_url = requests.get(url)
    hkd_row = pd.read_csv(io.BytesIO(get_url.content), sep=",", encoding="shift-jis")
    hkd_str_date = hkd_row['年'].astype(str) + '/' + hkd_row['月'].astype(str) + '/' + hkd_row['日'].astype(str)
    hkd_date = pd.to_datetime(hkd_str_date)
    hkd_daily_cases = hkd_row.drop(['グラフ非表示', '年', '月', '日', '日検査数', '検査累計', '陽性累計', '日患者数', '患者累計',
        '日軽症中等症数', '軽症中等症累計', '日重症数', '重症累計', '日死亡数', '死亡累計', '日治療終了数',
        '治療終了累計', '新規検査人数計', '陽性率％', '濃厚接触者', '濃厚接触者以外', '備考'], axis=1)
    hkd_daily_cases.index = hkd_date
    hkd_seasonal = sm.tsa.seasonal_decompose(hkd_daily_cases['日陽性数'], period=7)
    hkd_daily_cases['trend'] = hkd_seasonal.trend
    return hkd_daily_cases