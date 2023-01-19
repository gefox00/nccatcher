import PySimpleGUI as Sg
import requests
from PC_Converter_for_web_class import Nccatcher
from time import sleep
import pyperclip

# ウィンドウに配置するコンポーネント設定
layout = [
            # URL入力用テキストボックスと文字列の配置
            [Sg.Text('URLを張り付けてください'), Sg.Input(size=(53, 1), key='tb_open')],
            # ボタンの配置1
            [Sg.Button('変換開始', size=33, key='bt_start'),
             # ボタンの配置
             Sg.Button('クリップボードにコピー', size=33, key='bt_copy')],
            # 変換結果表示用テキストボックスの配置
            [Sg.Output(size=(78, 20), key='log')]
         ]
# ウィンドウタイトル設定
window = Sg.Window('コンバーター', layout)
while True:
    # イベントハンドラ
    event, values = window.read()
    load_data = {}
    # ×ボタン押下時の動作
    if event == Sg.WIN_CLOSED:
        # ループを抜けるとGUIが終了する
        break

    # 変換開始ボタン押下時の動作
    if event == 'bt_start':
        window['log'].update(values)
        if len(window['tb_open'].get()) > 0 and 'charasheet.vampire-blood.net' in window['tb_open'].get():
            window['log'].update('')
            # APIを叩いてJson取得
            target = window['tb_open'].get() + '.js'
            data = requests.get(target)
            title = data.json()
            # レスポンスとシートタイトルを確認
            if data.status_code == requests.codes.ok and title['game'] == 'nechro':
                get_json = Nccatcher(data=data.json(), url=window['tb_open'].get()).ch_data
                pyperclip.copy(get_json)
                # 変換結果をGUIに反映
                window['log'].update(get_json)
                # クリップボードに結果をコピーしたことをポップアップ
                Sg.popup('変換結果をクリップボードにコピーしました', title='コピーしました', no_titlebar=True)
            else:
                Sg.popup_error('ネクロニカ以外のキャラシURLが入力されたか\n対応できないURLが指定されました', title='error')
            # ボタンを連打してサーバー攻撃しないように1秒待機
            sleep(1)
    # クリップボードにコピーボタン押下処理
    if event == 'bt_copy':
        # GUIのログボックスに表示してる内容をclipboardにコピーする
        pyperclip.copy(window['log'].get())
        # クリップボードにログボックスの中身をコピーしたことをポップアップ
        Sg.popup('クリップボードにコピーしました', title='コピーしました', no_titlebar=True)

# 何らかの理由でループが抜けたときにプログラムを確実に終了させる
exit()

# デバッグ用
# https://charasheet.vampire-blood.net/me58c7745269933f1080637f585dfa201
#                                       e58c7745269933f1080637f585dfa201

