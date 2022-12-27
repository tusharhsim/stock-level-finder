from selenium import webdriver
import pandas as pd

driver = webdriver.Chrome()
driver.implicitly_wait(4)

driver.get('https://www.investing.com/indices/major-indices')

for data in driver.find_elements_by_css_selector('#__next > div > div > div.grid-container.grid-container--fixed-desktop.general-layout_main__3tg3t > main > div.table-browser_table-browser-wrapper__2ynbE > table > tbody'):
	 world_indices = data.text.split('\n')

indices = world_indices[::2]
changes = []

for i in world_indices[1::2]:
	changes.append(float(i.split()[4][:-1]))

index = indices.index('Nifty 50')
indices.append(indices.pop(index))
changes.append(changes.pop(index))

relation = {}
for i in range(len(indices)):
	relation[indices[i]] = changes[i]

df = pd.DataFrame.from_dict(data=relation, orient='index').T
print(df.T)
df.to_csv('wi_noon.csv', mode='a', header=False)

input('\npress enter to exit webdriver\t')
driver.quit()

'''
'NA','DowJones','S&P500','Nasdaq','SmallCap2000','S&P500VIX','S&P/TSX','Bovespa','S&P/BMVIPC','DAX','FTSE100','CAC40','EuroStoxx50','AEX','IBEX35','FTSEMIB','SMI','PSI20','BEL20','ATX','OMXS30','OMXC25','MOEX','RTSI','WIG20','BudapestSE','BIST100','TA35','TadawulAllShare','Nikkei225','S&P/ASX200','DJNewZealand','Shanghai','SZSEComponent','ChinaA50','DJShanghai','HangSeng','TaiwanWeighted','SET','KOSPI','IDXComposite','BSESensex','PSEiComposite','Karachi100','HNX30','Nifty50'
'''
