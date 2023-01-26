import PySimpleGUI as Sg
import requests
import pyperclip
from PC_Converter_for_web_class import Nccatcher
from time import sleep
import sqlite3

# データベース操作追加
# コンバーターとコンバート履歴はGUIを分ける使いづらいと感じたら統合する
dbname = 'data_file/my_char.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()
# テーブルの存在をチェックしてテーブルが存在しないときは作成する
cur.execute('CREATE TABLE IF NOT EXISTS character(name STRING, data STRING)')

pyperclip.copy("https://charasheet.vampire-blood.net/me58c7745269933f1080637f585dfa201")
# ウィンドウに配置するコンポーネント設定
layout = [
            # URL入力用テキストボックスと文字列の配置
            [Sg.Text('URLを張り付けてください'), Sg.Input(size=(53, 1), key='tb_open')],
            # ボタンの配置1
            [Sg.Button('変換開始', size=33, key='bt_start'),
             # ボタンの配置
             Sg.Button('クリップボードにコピー', size=33, key='bt_copy')]
            # 変換結果表示用テキストボックスの配置
            # ,[Sg.Output(size=(78, 20), key='log')]
         ]
# ウィンドウタイトル設定
window = Sg.Window(title='コンバーター', layout=layout)
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
        # ブランクとキャラシ保管所以外のURLは無視する
        if len(window['tb_open'].get()) > 0 and 'charasheet.vampire-blood.net' in window['tb_open'].get():
            # window['log'].update('')
            # APIを叩いてJson取得
            target = window['tb_open'].get() + '.js'
            data = requests.get(target)
            # 処理可能なデータか中身を確認する
            # URLからなんのタイトルのキャラシか分からないためデータを取得して確かめる
            title = data.json()
            if data.status_code == requests.codes.ok and title['game'] == 'nechro':
                # キャラシ変換オブジェクトをインスタンス化してデータを処理する
                get_json = Nccatcher(data=data.json(), url=window['tb_open'].get())
                # 変換結果をクリップボードへコピーする
                pyperclip.copy(get_json.ch_data)
                # 変換結果をGUIに反映
                # window['log'].update(get_json.ch_data)
                # クリップボードに結果をコピーしたことをポップアップ
                Sg.popup('変換結果をクリップボードにコピーしました', title='コピーしました', no_titlebar=True)
                # 変換したデータをデータベースにインサート
                # ただし同一キャラ名のキャラはのぞく
                push_data = {get_json.ch_data_js['data']['name']: get_json.ch_data}
                if cur.execute(f'SELECT COUNT(*) FROM character WHERE name = "{push_data.keys()}"').rowcount > 0:
                    value = Sg.popup_ok_cancel('同一名のデータが存在します\nデータを更新しますか？',
                                               title='重複検知',
                                               no_titlebar=True)
                    if value == 'OK':
                        pass

                else:
                    # 同一データが存在しないのでデータをインサートする
                    cur.execute(f'INSERT INTO character(name, data) VALUES({push_data.keys()}, {push_data.values()})')


            else:
                Sg.popup_error('ネクロニカ以外のキャラシURLが入力されたか\n対応できないURLが指定されました',
                               title='error',
                               no_titlebar=True)
            # ボタンを連打してサーバー攻撃しないように1秒待機
            sleep(1)
    # クリップボードにコピーボタン押下処理
    if event == 'bt_copy':
        if len(window['log'].get()) > 0:
            # GUIのログボックスに表示してる内容をclipboardにコピーする
            pyperclip.copy(window['log'].get())
            # クリップボードにログボックスの中身をコピーしたことをポップアップ
            Sg.popup('クリップボードにコピーしました', title='コピーしました', no_titlebar=True)
        else:
            # urlの入力なしにボタンを押下した場合は警告表示する
            # 他に処理はしない
            Sg.popup_error('コピーすべきデータがありません', title='error', no_titlebar=True)
conn.close()
