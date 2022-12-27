enctoken = 'pue/em1YrE6s8XSEzDO6AoOamMimlSPp845NFRqDW9P8LgwqE7dXPR2nAwqVRLOW0A8A7ZTzZfncfXqP9lLWbI5TO6xlrg=='
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import requests
import json

pd.set_option("display.max_rows", None, "display.max_columns", None)

ohlc = []
s_date = datetime.strptime('2019-01-01', "%Y-%m-%d").date()
e_date = datetime.strptime('2021-06-11', "%Y-%m-%d").date()

headers = {'Authorization': 'enctoken '+str(enctoken),
           'Content-Type': 'application/x-www-form-urlencoded'}

while s_date <= e_date:
        if e_date - s_date >= timedelta(days=60):
                params = (('from', s_date),('to', s_date+timedelta(days=60)), ('oi',0))
                s_date += timedelta(days=60)
        else:
                params = (('from', s_date),('to', e_date), ('oi',0))
                s_date = e_date + timedelta(days=1)
        response = requests.get('https://kite.zerodha.com/oms/instruments/historical/738561/hour', headers = headers, params = params)
        ohlc += response.json()['data']['candles']

#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/2minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/3minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/4minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/5minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/10minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/15minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/30minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/1hour', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/2hour', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/3hour', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/day', headers = headers, params = params)


candles = np.array([])
date = []

for i in ohlc[::][:]:
        date.append(i[0])
        candles = np.append(candles, np.array([i[1], i[2], i[3], i[4], i[5]]))
        #print(i)

date = np.array(date)
candles = candles.reshape(-1,5)
df = pd.DataFrame(index= pd.to_datetime(date), data=candles, columns=['open','high','low','close','volume'])
df.to_csv('ohlc.csv', index=False)
