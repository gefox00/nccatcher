import requests
import json_file
from bs4 import BeautifulSoup as bs
from time import sleep

base_url='https://charasheet.vampire-blood.net/list_nechro.html?name='
# Titleでひっかけてるみたい
target = ''

data = requests.get(base_url+target).text

soup = bs(data, 'html.parser')
ch_data_tx = []
ch_data_js = []
for l in soup.select('a[href]'):
    if '.pdf' in str(l.get("href")):
        temp = l.get("href")[:-4] + '.js'
        ch_data_tx.append(requests.get(temp).text)
        sleep(1)
for i in ch_data_tx:
    ch_data_js.append(json_file.loads(i))
for i in ch_data_js:
    for j in i:
        print(j)