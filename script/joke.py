import requests
from PIL import Image
import PySimpleGUI as sg


get_fox = requests.get("https://randomfox.ca/floof/").json()
get_fox_pic = requests.get(get_fox['image']).content

fox = Image.frombytes(mode='RGBA', size=(100, 100), data=get_fox_pic)
fox.show()


if False:
    # ウィンドウのテーマ
    sg.theme('DarkRed')

    # ウィンドウのレイアウト
    layout = [
            [sg.Image(source=get_fox_pic)]
        ]

    # ウィンドウオブジェクトの作成
    window = sg.Window('title', layout, size=(300, 300))

    # イベントのループ
    while True:
        # イベントの読み込み
        event, values = window.read()
        # ウィンドウの×ボタンクリックで終了
        if event == sg.WIN_CLOSED:
            break

    # ウィンドウ終了処理
    window.close()