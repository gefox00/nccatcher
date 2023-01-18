import requests
import json
import pyperclip
import PySimpleGUI as Sg


class DC_Dolls:
    chs_url = ''
    name = ''
    position = ''
    main_class = ''
    sub_class = ''
    bp = 0
    act_point = 0
    piece = {}
    carma = []
    parts = {}
    party = {}
    levels = {}
    palet = []


class Tools:
    json = ''
    txt = ''
    pdf = []
    urls = {}

    def __init__(self, target):
        self.dataset(target)
    def get_param(self):
        pass

    def get_binary(self):
        self.json = requests.get(self.urls['js_url'])
        self.txt = requests.get(self.urls['txt_url'])
        self.pdf = requests.get(self.urls['txt_pdf'])

    def dataset(self, data):
        org_data = data
        self.urls['org_url'] = org_data
        self.urls['js_url'] = data + '.js'
        self.urls['txt_pdf'] = data + '.pdf'
        self.urls['txt_url'] = data + '.txt'

    def get_basedata(self, url):
        target = url + '.js'
        res = requests.get(target)
        data = res.content
        chdata = json.loads(data)
        return chdata


if __name__ == '__main__':
    print(__name__)
    tgurl = 'https://charasheet.vampire-blood.net/me58c7745269933f1080637f585dfa201'
    mn_timing = {0: 'オート', 1: 'アクション', 2: 'ラピッド', 3: 'ジャッジ', 4: 'ダメージ'}
    mn_equip = {1: 'ポジション', 2: 'メインクラス', 3: 'サブクラス', 4: '頭', 5: '腕', 6: '胴', 7: '足'}
    DC_level = {1:'武装',2:'変異',3:'改造'}
    # 'Power_hantei'
    # 'Power_name'
    # 'V_Power_timing'
    # 'Power_range'
    # 'kakera_name'
    # 'MC1'
    # 'MC2'
    # 'MC3'
    # 'SC1'
    # 'SC2'
    # 'SC3'
    # 'ST_Bonus'
    # 'Act_Total'
    # 'roice_name'
    # 'data_title'
    # 'pc_name'
    # 'age'

    if True:
        partmake = []
        create_doll = DC_Dolls()
        data = Tools(tgurl).get_basedata(tgurl)

        create_doll.name = data['pc_name']
        create_doll.position = data['Position_Name']
        create_doll.main_class = data['MCLS_Name']
        create_doll.sub_class = data['SCLS_Name']
        create_doll.act_point = int(data['Act_Total'])
        create_doll.levels['武装'] = int(data['MC1'])
        create_doll.levels['変異'] = int(data['MC2'])
        create_doll.levels['改造'] = int(data['MC3'])
        create_doll.levels['武装'] += int(data['SC1'])
        create_doll.levels['変異'] += int(data['SC2'])
        create_doll.levels['改造'] += int(data['SC3'])
        create_doll.levels[DC_level[int(data['ST_Bonus'])]] += 1
        for pos, name, time, cost, mrange, memo, shozoku in zip(data['Power_hantei'],
                                                                data['Power_name'],
                                                                data['Power_timing'],
                                                                data['Power_cost'],
                                                                data['Power_range'],
                                                                data['Power_memo'],
                                                                data['Power_shozoku']):
            create_doll.parts[name] = [mn_equip[int(pos)], mn_timing[int(time)], cost, mrange, memo, shozoku]

        for name, txt in zip(data['kakera_name'],data['kakera_memo']):
            create_doll.piece[name] = txt

    for i in data:
        print(i,data[i])
    for i in create_doll.parts:
        print(i, create_doll.parts[i])
    for i in create_doll.piece:
        print(i,create_doll.piece[i])
