from datetime import datetime
import numpy as np
import requests
import json

#enctoken = input('enctoken\t')
enctoken = 'unmhddkh46OIzdzWDmDv8f9sGJXVAQC+nGMjRDkfevDuev3qfRN+bdmeKjid3bG/hhd6MBsq6o2iNUWY1LErbu1B0ximKA=='

headers = {'Authorization': 'enctoken '+str(enctoken),
           'Content-Type': 'application/x-www-form-urlencoded'}

date = datetime.today().strftime('%Y-%m-%d')
#params = (('from', date),('to', date))
params = (('from', '2021-05-07'),('to', '2021-05-07'))

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
priceActionLH =  []
priceAction = []

for i in ohlc[::][:]:
        priceAction.append(int(i[4]-i[1]))
        priceActionLH.append(int(i[2]-i[3]))
#        print(i)

priceAction = np.array(priceAction)
priceActionLH = np.array(priceActionLH)
print('no of candles candles\t\t%s' %len(priceAction))

print('\nfor OC:\ntotal movement\t\t%s' %abs(sum(priceAction)))
print('movement per candle\t%s' %(abs(sum(priceAction))/len(priceAction)))

pa = np.sqrt(np.mean(priceAction**2))
print('price action rms\t%s' %(pa))
print('std\t\t\t%s' %(np.std(priceAction)))

print('\nfor HL:\ntotal movement\t\t%s' %abs(sum(priceActionLH)))
print('movement per candle\t%s' %(abs(sum(priceActionLH))/len(priceActionLH)))

pa = np.sqrt(np.mean(priceActionLH**2))
print('price action rms\t%s' %(pa))
print('std\t\t\t%s' %(np.std(priceActionLH)))
