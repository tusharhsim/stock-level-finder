from collections import OrderedDict
from datetime import datetime
import mplfinance as mpf
import pandas as pd
import numpy as np
import requests
import json

enctoken = 'YVUrcPj58V3a9X7OX+IUi43A9de6+fFvb66Cq9X8hGVd05ZwAKL/m2GZPe95Q2H742CgQsmQpNoDMyRYJmkE8HgLXtGIVXd+Xas9Yug8RKdUoK4kTMf9xw=='
#enctoken = input('enctoken\t')

#params = (('from', datetime.today().strftime('%Y-%m-%d')),('to', datetime.today().strftime('%Y-%m-%d')))
params = (('from', '2022-02-03'),('to', '2022-04-20'))

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
df = pd.DataFrame(index= pd.to_datetime(date), data=candles, columns=['open','high','low','close'])

high = np.array(high)
low = np.array(low)

priceActionLH = high-low
#np.sqrt(np.mean(priceActionLH**2))

### variables###
baseline = 17200
min_line = baseline - 250
max_line = baseline + 250
nearest_level = 5  #np.std(priceActionLH**0.5)
down_pa = 20#np.sqrt(np.mean(priceActionLH**2))
up_pa = 20#np.sqrt(np.mean(priceActionLH**2))

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

def display_figure(dic):
        print(f'zone with max rejection\t{max(dic.values())} @ {[k for k,v in dic.items() if v == max(dic.values())]}')
'''        for i,j in dic.items():
                print("{:.1f}\t\t{}".format(i,j))
'''

def display_val_figure(dic):
        print(f'zone with max validation\t{max(dic.values())} @ {[k for k,v in dic.items() if v == max(dic.values())]}')
'''        for i,j in dic.items():
                print("\t{:.1f}\t\t{}".format(i,j))
'''

def display(lev, val):
        display_figure(lev)
        display_val_figure(val)

def plot(support, resistance):
        base = [baseline-0.05, baseline, baseline+0.05]
        all_levels = base + support + resistance
        colors = ['y']*3 + [i for i in 'r'*len(support)] + [j for j in 'g'*len(resistance)]
        mpf.plot(df, type = 'candle', style = 'binance', hlines = dict(hlines = all_levels, colors=colors, linewidths=(0.5)), tight_layout=True)

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
                                levels_r[high[touch]] = [round(up+down, 2), round(up, 2), round(down, 2)]
                                counter(high[touch])
                        touch = 0
                        down, up = 0,0
                        floor, ceil = 0,0
        except:
                if (i == len(high)-1) and touch:
                        if up >= up_par and down >= down_par:
                                levels_r[high[touch]] = [round(up+down, 2), round(up, 2), round(down, 2)]
                                counter(high[touch])
print('\nresistance:')
display(levels_r, validation_r)

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
                                levels_s[low[touch]] = [round(up+down, 2), round(down, 2), round(up, 2)]
                                counter(low[touch])
                        touch = 0
                        down, up = 0,0
                        floor, ceil = 0,0
        except:
                if (i == len(low)-1) and touch:
                        if up >= up_pas and down >= down_pas:
                                levels_s[low[touch]] = [round(up+down, 2), round(down, 2), (up, 2)]
                                counter(low[touch])
print('\nsupport:')
display(levels_s, validation_s)

def repeated(data, lst):
        if data in lst:
                repeated(data+0.05, lst)
        else:
                return float(data)

all_support = []
all_resistance = []
for i in levels_s:
        if i in all_support:
                all_support.append(i-0.05)
        else:
                all_support.append(i)
for i in levels_r:
        if i in all_resistance:
                last = repeated(i, all_support)
                if last != None and last > 0.05:
                        all_resistance.append(last)
                else:
                        all_resistance.append(i+0.05)
        else:
                all_resistance.append(i)

plot(all_support, all_resistance)

ranged_level_s = [i for i in all_support if i >= min_line and i <= max_line]
ranged_level_r = [i for i in all_resistance if i >= min_line and i <= max_line]

plot(ranged_level_s, ranged_level_r)

res_lev = {i:j for i,j in levels_r.items() if i >= min_line and i <= max_line}
sup_lev = {i:j for i,j in levels_s.items() if i >= min_line and i <= max_line}

res_val = {i:j for i,j in validation_r.items() if i >= min_line and i <= max_line}
sup_val = {i:j for i,j in validation_s.items() if i >= min_line and i <= max_line}

print('\nvalidation for ranged resistance:')
display(res_lev, res_val)
print('\nvalidation for ranged support:')
display(sup_lev, sup_val)

#df[df['ohlc'] == data]['ohlc']
