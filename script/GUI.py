import PySimpleGUI as sg
import requests
from PC_Converter_for_web_class import Nccatcher
sg.theme('Default1')

# ウィンドウに配置するコンポーネント設定
layout = [
            [sg.Text('キャラシのURLを張り付けてください')],
            [sg.Input(size=(80,1),key='tb_open')],
            [sg.Button('変換開始',key='bt_start')]
            ,[sg.Output(size=(78,20),key='log')]
         ]
window = sg.Window('キャラシコンバーター', layout)
while True:
    event, values = window.read()
    loaddata = {}

    # ×ボタン押下時の動作
    if event == sg.WIN_CLOSED or event == 'キャンセル':
        break

    # 変換開始ボタン押下時の動作
    elif event == 'bt_start':
        if len(window['tb_open'].get()) > 0:
            target = window['tb_open'].get() + '.js'

            data = requests.get(target)
            get = Nccatcher(data=data.json(), URL=window['tb_open'].get()).ch_data
            print(get)



# https://charasheet.vampire-blood.net/me58c7745269933f1080637f585dfa201
