from collections import OrderedDict
from datetime import datetime
import mplfinance as mpf
import pandas as pd
import numpy as np
import requests
import json

enctoken = 'LyGfTNGHiHExN4B9EyvwdNiM/yGdWQchnFCD5Y95llbvcuc76OXx1amjCqJOoegFAexjOU+dNWjsmCDjjQIdMHmqlDIGiw=='
#enctoken = input('enctoken\t')

#params = (('from', datetime.today().strftime('%Y-%m-%d')),('to', datetime.today().strftime('%Y-%m-%d')))
params = (('from', '2021-02-01'),('to', '2021-05-10'))

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
        high.append(i[2])
        low.append(i[3])
        #print(i)

date = np.array(date)
candles = candles.reshape(-1,4)
df = pd.DataFrame(data=candles, index= pd.to_datetime(date), columns=['open','high','low','close'])

high = np.array(high)
low = np.array(low)

priceActionLH = high-low
#np.sqrt(np.mean(priceActionLH**2))

### variables###
baseline = 14942
min_line = baseline - 150
max_line = baseline + 150
nearest_level = 5  #np.std(priceActionLH**0.5)
down_pa = np.sqrt(np.mean(priceActionLH**2))
up_pa = np.sqrt(np.mean(priceActionLH**2))

print(f'upward PA\t {up_pa}')
print(f'downward PA\t {down_pa}')

down_par = down_pa
up_par = up_pa
down_pas = down_pa
up_pas= up_pa

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
        if data in levels_r:
                data += nearest_level - (data % nearest_level)
                if data in validation_r:
                        validation_r[data] += 1
                else:
                        validation_r[data] = 1

floor, ceil = 0,0
down, up = 0,0
touch = 0
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
                        if up >= up_par and down >= down_par:
                                levels_r[high[touch]] = [up+down, up, down]
                                counter(high[touch])
                        touch = 0
                        down, up = 0,0
                        floor, ceil = 0,0
        except:
                if (i == len(high)-1) and touch:
                        if up >= up_par and down >= down_par:
                                levels_r[high[touch]] = [up+down, up, down]
                                counter(high[touch])
'''print('\nresistance:')
for i,j in levels_r.items():
        print(i,j)
print('\nno of validation:')
for i,j in validation_r.items():
        print('\t',i,j)'''
print(f'supply zone with max validation {max(validation_r.values())} @ {[k for k,v in validation_r.items() if v == max(validation_r.values())]}')

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
                        if up >= up_pas and down >= down_pas:
                                levels_s[low[touch]] = [up+down, down, up]
                                counter(low[touch])
                        touch = 0
                        down, up = 0,0
                        floor, ceil = 0,0
        except:
                if (i == len(low)-1) and touch:
                        if up >= up_pas and down >= down_pas:
                                levels_s[low[touch]] = [up+down, down, up]
                                counter(low[touch])
'''print('\nsupport:')
for i,j in levels_s.items():
        print(i,j)
print('\nno of validation:')
for i,j in validation_s.items():
        print('\t',i,j)'''
print(f'demand zone with max validation {max(validation_s.values())} @ {[k for k,v in validation_s.items() if v == max(validation_s.values())]}')

support = []
resistance = []
for i in levels_s:
        support.append(i)
for i in levels_r:
        resistance.append(i)

levels = support + resistance
colors = [i for i in 'r'*len(support)] + [j for j in 'g'*len(resistance)]

mpf.plot(df, style = 'charles', type = 'candle', hlines = dict(hlines=levels, colors=colors, linewidths=(0.5)))

ranged_level_s = [i for i in support if i >= min_line and i <= max_line]
ranged_level_r = [i for i in resistance if i >= min_line and i <= max_line]

ranged_levels = ranged_level_s + ranged_level_r
colors = [i for i in 'r'*len(ranged_level_s)] + [j for j in 'g'*len(ranged_level_r)]
mpf.plot(df, style = 'charles', type = 'candle', hlines = dict(hlines=ranged_levels, colors=colors, linewidths=(0.5)))

res_range = {i:j for i,j in validation_r.items() if i >= min_line and i <= max_line}
sup_range = {i:j for i,j in validation_s.items() if i >= min_line and i <= max_line}
print('\nranged validation for support:')
for i,j in sup_range.items():
        print(i,j)
print('\nranged validation for resistance:')
for i,j in res_range.items():
        print(i,j)
print(f'\nranged demand zone with max validation {max(sup_range.values())} @ {[k for k,v in sup_range.items() if v == max(sup_range.values())]}')
print(f'ranged supply zone with max validation {max(res_range.values())} @ {[k for k,v in res_range.items() if v == max(res_range.values())]}')
