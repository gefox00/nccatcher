import requests
from bs4 import BeautifulSoup
import time
from PC_Converter_for_web_class import Nccatcher as Nc
import json
with open('name.txt', 'r', encoding='utf8')as r:
    for k in r.read().splitlines():
        print(k)
        try:
            base_url = 'https://charasheet.vampire-blood.net/list_nechro.html'
            res = requests.get(base_url, params={'name': k}).content
            soup = BeautifulSoup(res, "html.parser")
            for i in soup.find_all('a'):
                if '.txt' in i.get('href'):
                    url = str(i.get('href'))[:-4]
                    json_data = requests.get(url + '.js').json()

                    conv_data = Nc(json_data, url)
                    time.sleep(2)
                    with open(f'json_file/{conv_data.ch_data_js["data"]["name"].replace("/", "")}.json', 'w', encoding='utf8')as w:
                        json.dump(conv_data.ch_data_js, w, indent=4)
        except:
            continue


















