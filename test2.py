#я нахожусь на дальнем востоке, поэтому ответы от ресурса у меня приходят дольше. По результатам первый проходит за 600 мс, последующие за 250 мс
#не совсем понял как вычисляется RPS, поэтому посчитал в двух вариантах: общее время выполнения всех 8 тестов ; суммирование 8 ответов сервера
#В одном случае RPS примерно 3, в другом примерно около 5

import time
from sys import getsizeof
import aiohttp
import asyncio
import datetime

import numpy as np


headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '68787bb9-bc11-401a-8dbf-a1970f199e80',
}
parameters = {
  'start':'1',
  'limit':'10',
  'convert':'USD',
  'sort':'volume_24h',
}

URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

#кол-во одновременных клиентов
MAX_CLIENTS = 8

#проверка скорость ответа ресурса
def ms_check(r_time):
    #print('time is',r_time)
    if r_time < 500:
        print ('site resp time is ok')
    else:
        print('site resp time is not ok')

#проверка на размер полученного пакета
def package_size_check(pckg):
    #ракомментить след. строку, чтобы увидеть размер пакета 
    #print('size:',(getsizeof(pckg)/1000), 'KB')
    if (getsizeof(pckg)/1000) < 10:
        print('package size is ok')
    else:
        print('package size is not ok')




#проверка на актуальность даты по каждой валюте
def date_check(r):
    #дата с клиента по UTC
    utctime = str(datetime.datetime.utcnow())
    utctime = utctime[0:10]
    tst_count = 0
    #print('utctime:',utctime)
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
    
    


#функция на выполнение get запроса 
async def fetch(client):
    print('Fetch process  started')
    #start = time.time()
    async with client.get(URL, params = parameters, headers = headers) as resp:
        #site_resp = (time.time() - start)*1000
        
        #print (site_resp)
        

        #print (ms_check(site_resp))

        #print (date_check(resp))
        #respaunvremya= resp.json()
        #print(respaunvremya)
        #print(package_size_check(resp))
        
        
        return await resp.json()
    
###
async def main():
    
    a=[]      #список для рассчета перцентиля 
    start_resp_timer = time.monotonic()   #начальная точка времени для подсчета rps
    async with aiohttp.ClientSession() as client:
         for i in range(1,MAX_CLIENTS+1):
            start_rps_timer = time.monotonic() #начальная точка отсчета response
            html = await fetch(client)
            end_rps_timer=(time.monotonic() - start_rps_timer)*1000 #конечная точка отсчета response
            print(package_size_check(html))      #тест на размер пакета
            a.append(end_rps_timer)           #добавление в список для рассчета перцентиля
            print(date_check(html))       #тест на актуальность каждого тикера
            print (ms_check(end_rps_timer))    #тест на ответ ресурса
            print('---------------------')
    
    print("Process took: {:.2f} seconds".format(time.monotonic() - start_resp_timer ))      #проверка, за сколько выполнился тест

            
#рассчет  и проверка персентеля
    #print(a)
    b=np.array(a)
    #print(b)
    p=np.percentile(b,80)
    if p<450:
        print('percentile is ok')
    else:
        print('percentile not ok')
    #print(p)
#рассчет и проверка rps
    resp_count = MAX_CLIENTS
    time_count = (time.monotonic()-start_resp_timer)
#первый вариант рассчета RPS    
    rps = resp_count/time_count
    print('rps1', rps)
#второй вариант рассчета RPS
    s=np.array(a)
    t=0
    for i in s:
        t = t+i
    t=t/1000
    rps2 = resp_count/t
    print ('rps2 is ',rps2)
    if rps > 5:
        print('rps is ok')
    else:
        print('rps not ok')

               
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
