import requests
import time
from sys import getsizeof
import datetime


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'10',
  'convert':'USD',
  'sort':'volume_24h',
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '68787bb9-bc11-401a-8dbf-a1970f199e80',
}

#проверка скорость ответа ресурса
def ms_check(r_time):
    #print('time is',r_time)
    if r_time < 500:
        print ('site resp time is ok')
    else:
        print('site resp time is not ok')
    return
        
#проверка на размер полученного пакета        
def package_size_check(pckg):
    #ракомментить след. строку, чтобы увидеть размер пакета 
    #print('size:',(getsizeof(pckg)/1000), 'KB')
    if (getsizeof(pckg)/1000) < 10:
        print('package size is ok')
    else:
        print('package size is not ok')
    return
        
#проверка на актуальность даты по каждой валюте
def date_check(r):
    #дата с клиента по UTC
    utctime = str(datetime.datetime.utcnow())
    utctime = utctime[0:10]
    #print('utctime:',utctime)
    tst_count = 0
    for i in range(len(r['data'])):
        ticker_date = r['data'][i]['last_updated']
        ticker_date = ticker_date[0:10]
        #print('ticker_date:',ticker_date)
        if ticker_date == utctime:
            tst_count = tst_count+1
    if tst_count == len(r['data']):
        print ('date of tickers is ok')
    else:
        print ('date of tickers is not ok')
    return 


start=time.monotonic()
r = requests.get( 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest', params = parameters, headers = headers )
end = time.monotonic()
dataLL = r.json()
end_timer=(end - start)*1000

print('---------------------')
print(package_size_check(r))
print('---------------------')
print(date_check(dataLL))
print('---------------------')
print (ms_check(end_timer))
print('---------------------')
