from selenium import webdriver
import keyboard
import time
import csv

driver = webdriver.Chrome()
driver.implicitly_wait(4)
changes = []
driver.get('https://www.investing.com/indices/indices-futures')

def data_scalper():
    n=1
    while True:
        for data in driver.find_elements_by_css_selector('#__next > div > div > div.grid-container.grid-container--fixed-desktop.general-layout_main__3tg3t > main > div:nth-child(3) > div.table-browser_table-browser-wrapper__2ynbE > table > tbody'):
            change = []
            for percent in (data.text.split('\n'))[1::2]:
                try:
                    change.append(float(percent.split()[6][:-1]))
                except:
                    change.append(float(percent.split()[4][:-1]))
            changes.append(change)
        print(f'data of {n} minutes saved')
        try:
            time.sleep(60)
        except KeyboardInterrupt:
            print('exiting...')
            driver.quit()
            break
        n+=1

data_scalper()
with open("indices_futures.csv", "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(changes)

'''
'NA','US30','US500','USTech100','SmallCap2000','S&P500VIX','DAX','CAC40','FTSE100','EuroStoxx50','FTSEMIB','SMI','IBEX35','ATX','WIG20','AEX','iBovespa','Nikkei225','TOPIX','HangSeng','ChinaH-Shares','CSI300','ChinaA50','S&P/ASX200','SingaporeMSCI','BankNIFTY','KOSPI200','SGXFTSETaiwanF','SouthAfrica40','TecDAX','Nifty50'
'''
