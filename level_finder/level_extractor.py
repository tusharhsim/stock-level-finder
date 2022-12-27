from collections import OrderedDict
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import requests
import json

enctoken = 'r/oj9E1iXaSG35qAn/+4eJy4+3tS5hmWMRw0VercVv/JvkzfzXTNa9dXyZWn4hFk7/0QD5jd2In2AXDTK0EAuEVLT4QGUQ=='
#enctoken = input('enctoken\t')

#params = (('from', datetime.today().strftime('%Y-%m-%d')),('to', datetime.today().strftime('%Y-%m-%d')))
params = (('from', '2021-03-01'),('to', '2021-05-01'))

headers = {'Authorization': 'enctoken '+str(enctoken),
           'Content-Type': 'application/x-www-form-urlencoded'}


#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/1minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/2minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/3minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/4minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/5minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/10minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/15minute', headers = headers, params = params)
response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/30minute', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/1hour', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/2hour', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/256265/3hour', headers = headers, params = params)
#response = requests.get('https://kite.zerodha.com/oms/instruments/historical/738561/day', headers = headers, params = params)

jsonData = response.json()
ohlc = jsonData['data']['candles']

support =  []
resistance = []

for i in ohlc[::][:]:
        data = np.array([i[1], i[2], i[3], i[4]])
        resistance.append(int(np.sqrt(np.mean(data**2))))
        support.append(int(np.square(np.mean(data**0.5))))
        #print(i)

resistance = np.array(resistance)
support = np.array(support)

levels_s = OrderedDict()
up = 0
down = 0

for i in range(len(support)):
        try:
                if support[i] >= support[i+1] and not up:
                        down += support[i] - support[i+1]
                        touch = i+1
                elif support[i] < support[i+1] and down:
                        up += support[i+1] - support[i]

                if up and support[i+1] < support[i]:
                        par_str = up + down
                        if par_str >= 50 and up >= 20:
                                levels_s[support[touch]] = [par_str, down, up]
                        down, up = 0,0
        except:
                pass

print('support')
for i,j in levels_s.items():
        #print(i,j)
        pass

levels_r = OrderedDict()
up = 0
down = 0

for i in range(len(resistance)):
        try:
                if resistance[i] < resistance[i+1] and not down:
                        up += resistance[i+1] - resistance[i]
                        touch = i+1
                elif resistance[i] >= resistance[i+1] and up:
                        down += resistance[i] - resistance[i+1]

                if down and resistance[i+1] < resistance[i]:
                        par_str = up + down
                        if par_str >= 50 and down >= 20:
                                levels_r[resistance[touch]] = [par_str, up, down]
                        down, up = 0,0
        except:
                pass

print('\nresistance')
for i,j in levels_r.items():
        #print(i,j)
        pass


# plotting
plt.xlabel("Time") 
plt.ylabel("LTP") 
plt.plot(np.arange(len(support)), support, color ="b")
plt.plot(np.arange(len(resistance)), resistance, color ="b")
for i in levels_s:
        plt.axhline(y=i, color='g', linestyle='-')
for i in levels_r:
        plt.axhline(y=i, color='r', linestyle='-')
plt.show()
