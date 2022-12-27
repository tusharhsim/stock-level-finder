from selenium import webdriver
import pandas as pd

driver = webdriver.Chrome()
driver.implicitly_wait(4)

driver.get('https://www.investing.com/indices/indices-futures')

for data in driver.find_elements_by_css_selector('#__next > div > div > div.grid-container.grid-container--fixed-desktop.general-layout_main__3tg3t > main > div:nth-child(3) > div.table-browser_table-browser-wrapper__2ynbE > table > tbody'):
	 indices_fut = data.text.split('\n')

indices = indices_fut[::2]
changes = []

for i in indices_fut[1::2]:
    try:
        changes.append(float(i.split()[6][:-1]))
    except Exception:
        changes.append(float(i.split()[4][:-1]))

index = indices.index('Nifty 50')
indices.append(indices.pop(index))
changes.append(changes.pop(index))

relation = {}
for i in range(len(indices)):
	relation[indices[i]] = changes[i]

df = pd.DataFrame.from_dict(data=relation, orient='index').T
print(df.T)
df.to_csv('indices_futures.csv', mode='a', header=False)

input('\npress enter to exit webdriver\t')
driver.quit()

'''
'NA','US30','US500','USTech100','SmallCap2000','S&P500VIX','DAX','CAC40','FTSE100','EuroStoxx50','FTSEMIB','SMI','IBEX35','ATX','WIG20','AEX','iBovespa','Nikkei225','TOPIX','HangSeng','ChinaH-Shares','CSI300','ChinaA50','S&P/ASX200','SingaporeMSCI','BankNIFTY','KOSPI200','SGXFTSETaiwanF','SouthAfrica40','TecDAX','Nifty50'
'''
