import PySimpleGUI as sg
import requests
from PC_Converter_for_web_class import nccatcher
from time import sleep
import pyperclip
import psd_tools


tag = 'https://charasheet.vampire-blood.net/list_nechro.html?order=id&tag='
title = 'https://charasheet.vampire-blood.net/list_nechro.html?order=id&title='
name = 'https://charasheet.vampire-blood.net/list_nechro.html?order=id&name='
choices = ("タグ", "タイトル", "名前")

# ウィンドウに配置するコンポーネント設定
layout = [[sg.Text('キーワード')],
          [sg.Input(size=(80, 1), key='tb_open')],
          [sg.Listbox(choices, size=30, key='lb_target')],
          [sg.Button('検索', key='bt_start'),
           sg.Button('クリップボードにコピー', key='bt_copy'),
           sg.Button('update', key='bt_st')]]
window = sg.Window('データ検索', layout)
while True:
    event, values = window.read()

    # ×ボタン押下時の動作
    if event == sg.WIN_CLOSED:
        break

    # 変換開始ボタン押下時の動作
    if event == 'bt_start':
        print(window['lb_target'])
    if event == 'bt_copy':
        print(event)
    if event == 'bt_st':
        print(event)

    # https://charasheet.vampire-blood.net/me58c7745269933f1080637f585dfa201