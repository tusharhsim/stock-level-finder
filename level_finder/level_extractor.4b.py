from collections import OrderedDict
from datetime import datetime
import mplfinance as mpf
import pandas as pd
import numpy as np
import requests
import json

enctoken = 'RYkiSjCzMdSY5ygf0R3q8lVaWU57QgmuI+I3wXS814VA/gHrQwENt6CK1zvVHGx3K6dpMSSAwhrWr8zjwR/qf69mOL82kA=='
#enctoken = input('enctoken\t')

#params = (('from', datetime.today().strftime('%Y-%m-%d')),('to', datetime.today().strftime('%Y-%m-%d')))
params = (('from', '2021-05-06'),('to', '2021-05-07'))

headers = {'Authorization': 'enctoken '+str(enctoken),
           'Content-Type': 'application/x-www-form-urlencoded'}


#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/1minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/2minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/3minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/4minute', headers = headers, params = params)
response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/5minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/10minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/15minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/30minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/1hour', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/2hour', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/3hour', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/738561/day', headers = headers, params = params)

jsonData = response.json()
ohlc = jsonData['data']['candles']

candles = np.array([])
date = []
high = []
low = []
for i in ohlc[::][:]:
        date.append(i[0])
        candles = np.append(candles, np.array([i[1], i[2], i[3], i[4]]))
        high.append(int(i[2]))
        low.append(int(i[3]))
        #print(i)

date = np.array(date)
candles = candles.reshape(-1,4)
df = pd.DataFrame(data=candles, index= pd.to_datetime(date), columns=['open','high','low','close'])

high = np.array(high)
low = np.array(low)

levels_r = OrderedDict()
floor, ceil = 0,0
down, up = 0,0

for i in range(len(high)):
        try:
                if (high[i] <= high[i+1]) and not down:
                        if not floor:
                                floor = low[i]
                        up = high[i+1] - floor
                        touch = i+1
                elif (high[i] > high[i+1]) and up:
                        if not ceil:
                                ceil = high[i]
                        down = ceil - low[i+1]

                if down and (high[i] <= high[i+1]):
                        if up >= 18 and down >= 18:
                                levels_r[high[touch]] = [up+down, up, down]
                        touch = 0
                        down, up = 0,0
                        floor, ceil = 0,0
        except:
                if (i == len(high)-1) and touch:
                        if up >= 18 and down >= 18:
                                levels_r[high[touch]] = [up+down, up, down]

print('\nresistance:')
for i,j in levels_r.items():
        print(i,j)

levels_s = OrderedDict()
floor, ceil = 0,0
down, up = 0,0

for i in range(len(low)):
        try:
                if (low[i] >= low[i+1]) and not up:
                        if not ceil:
                                ceil = high[i]
                        down = ceil - low[i+1]
                        touch = i+1
                elif (low[i] < low[i+1]) and down:
                        if not floor:
                                floor = low[i]
                        up = high[i+1] - floor

                if up and (low[i] >= low[i+1]):
                        if up >= 18 and down >= 18:
                                levels_s[low[touch]] = [up+down, down, up]
                        touch = 0
                        down, up = 0,0
                        floor, ceil = 0,0
        except:
                if (i == len(low)-1) and touch:
                        if up >= 18 and down >= 18:
                                levels_s[low[touch]] = [up+down, down, up]

print('\nsupport:')
for i,j in levels_s.items():
        print(i,j)

support = []
resistance = []
for i in levels_s:
        support.append(int(i))
for i in levels_r:
        resistance.append(int(i))

levels = support + resistance
colors = [i for i in 'g'*len(support)] + [j for j in 'r'*len(resistance)]

mpf.plot(df, style = 'charles', type = 'candle', hlines = dict(hlines=levels, colors=colors, linewidths=(0.5)))
