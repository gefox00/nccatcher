from bs4 import BeautifulSoup as Bs
import requests as rq
import re


class ApiGetter:
    url = ''
    target = ''
    keys = ''

    def __init__(self, base_url, search_target):
        self.url = base_url
        self.target = search_target

    def get_target_list(self):
        rtn = []
        res = rq.get(url=self.url, data={self.keys: self.target}).content
        print({self.keys: self.target})
        soup = Bs(res, "html.parser")
        for i in soup.find_all('a'):
            link = i.get("href")
            name = i.get_text()

            if self.target in name:# and 'charasheet.vampire-blood.net' in name:
                rtn.append(link)
                print(link, "\t", name)
            if '&order=&page=' in link:
                print(link, name)
            #'<div class="methodcount">'
        result = soup.find('p', class_='text-sm text-gray-700 leading-5')#.get_text()
        print(Bs(result, "html.parser").find('span', class_='font-medium').get_text())
        # print(re.findall(r"\d+", s))
        # print(soup.find('span', class_='font-medium').get_text())
        print(result)
        return rtn
        
