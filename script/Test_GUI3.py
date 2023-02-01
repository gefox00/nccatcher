import PySimpleGUI as Sg
import json_file
import os
from time import sleep
import csv

data = ''
header = ['マニューバ名', '装備箇所', 'タイミング', 'コスト', '射程', 'テキスト', 'カテゴリ']
GUI = ['name', 'point', 'timing', 'cost', 'range', 'tb_txt2', 'category']
with open('database.json_file','r', encoding='utf8')as r:
    data = json_file.loads(r.read())

# ウィンドウに配置するコンポーネント設定
layout = [
            [Sg.Text('名前で検索')],
            [Sg.Input(size=80, key='bt_name')],
            [Sg.Button('検索', size=69, key='bt_search')],
            [Sg.Text('　名称　'), Sg.Input(size=40, key='name')],
            [
                Sg.Text('装備箇所'), Sg.Input(size=8, key='point'), Sg.Text('T'), Sg.Input(size=11, key='timing'),
                Sg.Text('C'), Sg.Input(size=11, key='cost'), Sg.Text('R'), Sg.Input(size=11, key='range'),
                Sg.Text('カテゴリ'), Sg.Input(size=11, key='category')
             ],
            [Sg.Text('適応効果'), Sg.Output(size=(80, 10), key='tb_txt2')],
            [Sg.Button('保存', size=69, key='bt_save')]
         ]
window = Sg.Window('エディタ', layout)
while True:
    event, values = window.read()
    load_data = {}
    if event == Sg.WIN_CLOSED:
        break

    if event == 'bt_search':
        with open('database.json_file', 'r', encoding='utf8') as r:
            data = json_file.loads(r.read())
        searchword = window['bt_name'].get()
        target = data.get(searchword)
        if not target == None:
            for g, d in zip(GUI, header):
                window[g].update(str(target.get(d)))
        else:
            for g, d in zip(GUI, header):
                window[g].update('')
    if event == 'bt_save':
        push_data = {}
        for h, g in zip(header, GUI):
            push_data[h] = window[g].get()
        data[window['name'].get()] = {}
        data[window['name'].get()] = push_data
        with open('database.json_file', 'w', encoding='utf8')as w:
            json_file.dump(data, w)


