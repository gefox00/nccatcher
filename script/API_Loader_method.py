from bs4 import BeautifulSoup as Bs
import requests as rq
import re
import math


class ApiGetter:
    url = ''
    target = ''
    keys = ''

    def __init__(self, base_url, search_target):
        self.url = base_url
        self.target = search_target

    def get_target_list(self):
        rtn = []
        print(self.target)
        res = rq.get(url=self.url, data={'name': str(self.target)}).content
        # res = rq.get(url=f'{self.url}?{self.keys}={self.target}').content
        soup = Bs(res, "html.parser")
        for i in soup.find_all('a'):
            link = i.get("href")
            name = i.get_text()

            if self.target in name and 'https://' in link:
                rtn.append(link)
                print(link, "\t", name)
        try:
            result = soup.find('p', class_='text-sm text-gray-700 leading-5').get_text().replace(' ', '')
            last_page = math.ceil(int(re.findall(r"\d+", result)[2]) / 50)
            if int(last_page) > 1:
                for count in range(int(last_page-1)):
                    pass


        except AttributeError:
            pass
        return rtn
        
