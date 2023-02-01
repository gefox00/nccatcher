import json
import os
import requests
from bs4 import BeautifulSoup
from time import sleep
import json_file

class SheetLoader:
    target = ''
    sh_base_str = []

    category_data = {'タイトル': '?title=', 'タグ': '?tag=', '名前': '?name='}
    base_url = 'https://charasheet.vampire-blood.net/list_nechro.html'
    # targetには?tag=ホラーのような形のURLが渡されるのが前提
    def __init__(self, target):
        self.target = target
        self.target = 'https://charasheet.vampire-blood.net/list_nechro.html?tag=ホラー'

    def __del__(self):
        pass

    # 渡されたURLをサーバーに投げて帰ってきたHTMLをスクレイピングして片っ端から
    # キャラを入手する
    def ch_finder(self):
        cmd = self.target + '&page=1'
        res = requests.get(cmd).content
        soup = BeautifulSoup(res, 'html.parser')
        link = soup.find_all('a')
        # 検索結果頁数を探索
        max_page = 0
        for i in link:
            if '&page=' in i.get('href'):
                if int(str(i.get('href')).split('&page=')[1]) > max_page:
                    # 最大頁数をカウント
                    max_page = int(str(i.get('href')).split('&page=')[1])
        # スクレイピングに使用した変数を解放最大頁数は保持
        del res, soup, cmd, link
        catch_character = []
        for i in range(max_page):
            sleep(1)
            cmd = self.target + f'&page={i+1}'
            res = requests.get(cmd).content
            soup = BeautifulSoup(res, 'html.parser')
            link = soup.find_all('a')
            for li in link:

                if '.txt' in str(li.get('href')):
                    catch_character.append(str(li.get('href')).replace('.txt', ''))
        for i in catch_character:
            sleep(1)
            print(i+'.js')
            get_data = requests.get(i+'.js').json()
            with open(f'json_file/{os.path.basename(i)}.json', 'w', encoding='utf8')as w:
                json.dump(obj=get_data, fp=w, indent=4)



SheetLoader('').ch_finder()
