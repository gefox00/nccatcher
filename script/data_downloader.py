import requests
from requests import get
from bs4 import BeautifulSoup as Bs
from time import sleep
import  os
import json

class DataSearch:
    out_data = {}
    keyword = ''
    target = ''
    tag = 'https://charasheet.vampire-blood.net/list_nechro.html?order=id&tag='
    title = 'https://charasheet.vampire-blood.net/list_nechro.html?order=id&title='
    name = 'https://charasheet.vampire-blood.net/list_nechro.html?order=id&name='
    url = {'tag': tag, 'title': title, 'name': name}

    def __init__(self, target: str, keyword: str):
        self.keyword = keyword
        self.target = target

    def get_ch_list(self):
        urls = []
        get_target = self.url[self.target] + self.keyword
        data = get(get_target).text
        soup = Bs(data, 'html.parser')
        for result in soup.select('a[href]'):
            if '.pdf' in str(result.get("href")):
                urls.append(str(result.get("href")).replace('.pdf', '.js'))
        return urls


get_data = []

for g in get_data:
    try:
        data = DataSearch('name', g).get_ch_list()
        for i in data:
            print(i)
            with open('endata/'+os.path.basename(i)+'on', 'w', encoding='utf8')as w:
                res = requests.get(i).json()
                json.dump(res, w, indent=4)
            sleep(1)
    except KeyError:
        pass
