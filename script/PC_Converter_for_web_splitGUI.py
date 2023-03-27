import PySimpleGUI as Sg
import requests
import pyperclip
from PC_Converter_for_web_class import Nccatcher
from time import sleep
import os
import json
import db

# コンフィグ読込用変数とDBオブジェクトをセット
config = {}
db_use = db.NcDataBase()
# 表示用ヘッダ
log_header = {'name': '名前', 'initiative': '最大行動値', 'externalUrl': '参照URL', 'memo': 'キャラクターメモ',
              'commands': 'チャットパレット', 'status': 'ステータス', 'params': 'パラメータ'}
clip_data = ''
layout = [[Sg.Text('PC1'), Sg.Input(key='PC1')],
          [Sg.Text('PC1'), Sg.Input(key='PC2')],
          [Sg.Text('PC1'), Sg.Input(key='PC3')],
          [Sg.Text('PC1'), Sg.Input(key='PC4')],
          [Sg.Button(button_text='開始')]
          ]

# ウィンドウタイトル設定
window = Sg.Window(title='コンバーター', layout=layout)
end_flag = True
while end_flag:
    # イベントハンドラ
    event, values = window.read()
    load_data = {}
    # ×ボタン押下時の動作
    match event:
        case Sg.WIN_CLOSED:
            # ｘボタンはそのままプログラムの終了処理にする
            end_flag = False
            break
del db_use
