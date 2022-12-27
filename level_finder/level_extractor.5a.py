from collections import OrderedDict
from datetime import datetime
import mplfinance as mpf
import pandas as pd
import numpy as np
import requests
import json

enctoken = '8nh6pqX7GSOtirAGggMEaWYVP19YWMqn/ppRMLSc9HKQA9uUbHI0ua/su2cwMgoJuu/HzaCsaUzAoYBmPd4V2y1x5iVpSg=='
#enctoken = input('enctoken\t')

#params = (('from', datetime.today().strftime('%Y-%m-%d')),('to', datetime.today().strftime('%Y-%m-%d')))
params = (('from', '2021-05-07'),('to', '2021-05-07'))

headers = {'Authorization': 'enctoken '+str(enctoken),
           'Content-Type': 'application/x-www-form-urlencoded'}

#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/1minute', headers = headers, params = params)
response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/2minute', headers = headers, params = params)
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

priceActionLH = high-low
np.sqrt(np.mean(priceActionLH**2))

### variables###
nearest_level = 1  #np.std(priceActionLH**0.5)
down_pa = 0#np.sqrt(np.mean(priceActionLH**2))
up_pa = 0#np.sqrt(np.mean(priceActionLH**2))

levels_r = OrderedDict()
levels_s = OrderedDict()
validation_r = {}
validation_s = {}

def counter(data):
        if data in levels_s:
                data -= (data % nearest_level)
                if data in validation_s:
                        validation_s[data] += 1
                else:
                        validation_s[data] = 1
        elif data in levels_r:
                data += nearest_level - (data % nearest_level)
                if data in validation_r:
                        validation_r[data] += 1
                else:
                        validation_r[data] = 1

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
                        if up >= up_pa and down >= down_pa:
                                levels_r[high[touch]] = [up+down, up, down]
                                counter(high[touch])
                        touch = 0
                        down, up = 0,0
                        floor, ceil = 0,0
        except:
                if (i == len(high)-1) and touch:
                        if up >= up_pa and down >= down_pa:
                                levels_r[high[touch]] = [up+down, up, down]
                                counter(high[touch])
print('resistance:')
for i,j in levels_r.items():
        print(i,j)
print(f'supply zone with max validation {max(validation_r.values())} @ {[k for k,v in validation_r.items() if v == max(validation_r.values())]}')
'''print('\nno of validation:')
for i,j in validation_r.items():
        print('\t',i,j)
'''
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
                        if up >= up_pa and down >= down_pa:
                                levels_s[low[touch]] = [up+down, down, up]
                                counter(low[touch])
                        touch = 0
                        down, up = 0,0
                        floor, ceil = 0,0
        except:
                if (i == len(low)-1) and touch:
                        if up >= up_pa and down >= down_pa:
                                levels_s[low[touch]] = [up+down, down, up]
                                counter(low[touch])
print('\nsupport:')
for i,j in levels_s.items():
        print(i,j)
print(f'demand zone with max validation {max(validation_s.values())} @ {[k for k,v in validation_s.items() if v == max(validation_s.values())]}')
'''print('\nno of validation:')
for i,j in validation_s.items():
        print('\t',i,j)
'''
support = []
resistance = []
for i in levels_s:
        support.append(int(i))
for i in levels_r:
        resistance.append(int(i))

levels = support + resistance
colors = [i for i in 'g'*len(support)] + [j for j in 'r'*len(resistance)]

mpf.plot(df, style = 'charles', type = 'candle', hlines = dict(hlines=levels, colors=colors, linewidths=(0.5)))
