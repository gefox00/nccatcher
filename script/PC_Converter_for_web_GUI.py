import PySimpleGUI as Sg
import requests
from PC_Converter_for_web_class import Nccatcher
from time import sleep
import pyperclip

# ウィンドウに配置するコンポーネント設定
layout = [
            [Sg.Text('URLを張り付けてください'), Sg.Input(size=(53, 1), key='tb_open')],
            [Sg.Button('変換開始', size=33, key='bt_start'),
             Sg.Button('クリップボードにコピー', size=33, key='bt_copy')],
            [Sg.Output(size=(78, 20), key='log')]
         ]
window = Sg.Window('コンバーター', layout)
while True:
    event, values = window.read()
    load_data = {}
    # ×ボタン押下時の動作
    if event == Sg.WIN_CLOSED:
        break

    # 変換開始ボタン押下時の動作
    if event == 'bt_start':
        if len(window['tb_open'].get()) > 0 and 'charasheet.vampire-blood.net' in window['tb_open'].get():
            # APIを叩いてJson取得
            target = window['tb_open'].get() + '.js'
            data = requests.get(target)
            if data.status_code == requests.codes.ok:
                get = Nccatcher(data=data.json(), url=window['tb_open'].get()).ch_data
                pyperclip.copy(get)
                window['log'].update(get)
            sleep(1)
    if event == 'bt_copy':
        pyperclip.copy(window['log'].get())

exit()


# https://charasheet.vampire-blood.net/me58c7745269933f1080637f585dfa201
#                                       e58c7745269933f1080637f585dfa201
# https://charasheet.vampire-blood.net/m60c76858f87cacfa082381f315146a92
