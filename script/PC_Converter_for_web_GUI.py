import PySimpleGUI as Sg
import requests
import pyperclip
from PC_Converter_for_web_class import Nccatcher
from time import sleep
import sqlite3
# デバッグ用フラグ
# ログボックスフラグ
debug_log = False

# https: // charasheet.vampire - blood.net / list_nechro.html?name = % E3 % 81 % 82
# データベース操作追加
# コンバーターとコンバート履歴はGUIを分ける使いづらいと感じたら統合する
# データベースをオープンしてテーブルをセットする
dbname = 'data_file/my_char.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()
# テーブルの存在をチェックしてテーブルが存在しないときは作成する
cur.execute('CREATE TABLE IF NOT EXISTS character(name STRING, data STRING)')
cur.execute('CREATE TABLE IF NOT EXISTS maneuver(name STRING, equip INTEGER, '
            'timing INTEGER, cost INTEGER, range INTEGER, text STRING)')

conn.commit()
# デバッグ用
#
# ウィンドウに配置するコンポーネント設定
layout = [
            # URL入力用テキストボックスと文字列の配置
            [Sg.Text('URLを張り付けてください'), Sg.Input(size=(62, 1), key='tb_open')],
            [Sg.Checkbox('データベースに記憶する', key='chb')],
            # ボタンの配置1
            [Sg.Button('変換開始', size=37, key='bt_start'),
             # ボタンの配置
             Sg.Button('クリップボードにコピー', size=37, key='bt_copy')]
            # 変換結果表示用テキストボックスの配置
         ]
if debug_log:
    layout.append([Sg.Output(size=(78, 20), key='log')])
else:
    pyperclip.copy("https://charasheet.vampire-blood.net/me58c7745269933f1080637f585dfa201")

# ウィンドウタイトル設定
window = Sg.Window(title='コンバーター', layout=layout)
while True:
    # イベントハンドラ
    event, values = window.read()
    load_data = {}
    # ×ボタン押下時の動作
    if event == Sg.WIN_CLOSED:
        # ｘボタンはそのままプログラムの終了処理にする
        break
        # ループを抜けるとGUIが終了する
    # 変換開始ボタン押下時の動作
    if event == 'bt_start':
        # ブランクとキャラシ保管所以外のURLは無視する
        if len(window['tb_open'].get()) > 0 and 'charasheet.vampire-blood.net' in window['tb_open'].get():
            if debug_log:
                window['log'].update('')
            # APIを叩いてJson取得
            target = window['tb_open'].get() + '.js'
            data = requests.get(target)
            # 非対応チェック
            # 変換できないデータレスポンスを受け取ってないかチェックと対処法をポップアップ
            if '<!DOCTYPE html>' in str(data.content):
                Sg.popup_error('対応できないURLが指定されました\n'
                               'URL末尾に「#top」がついている場合は「#top」を消して変換を実行してください',
                               title='error',
                               no_titlebar=True)
                continue
            # 処理可能なデータか中身を確認する
            # URLからなんのタイトルのキャラシか分からないためデータを取得して確かめる
            title = data.json()
            if data.status_code == requests.codes.ok and title['game'] == 'nechro':
                # キャラシ変換オブジェクトをインスタンス化してデータを処理する
                get_json = Nccatcher(data=data.json(), url=window['tb_open'].get())
                # 変換結果をクリップボードへコピーする
                pyperclip.copy(get_json.ch_data)
                # 変換結果をGUIに反映
                if debug_log:
                    window['log'].update(get_json.ch_data)
                # クリップボードに結果をコピーしたことをポップアップ
                Sg.popup('変換結果をクリップボードにコピーしました', title='コピーしました', no_titlebar=True)
                # 変換したデータをデータベースにインサート
                # ただし同一キャラ名のキャラはのぞく
                push_data = [get_json.ch_data_js['data']['name'], get_json.ch_data]
                cur.execute(f'SELECT COUNT(*) FROM character WHERE name = "{push_data[0]}"')
                row_count = cur.execute(f'SELECT COUNT(*) FROM character WHERE name = "{push_data[0]}"').fetchone()[0]
                if int(row_count) > 0 and window['chb'].get():
                    value = Sg.popup_ok_cancel('同一名のデータが存在します\nデータを更新しますか？',
                                               title='重複検知',
                                               no_titlebar=True)
                    if value == 'OK':
                        cur.execute(f'UPDATE character '
                                    f'SET name = "{push_data[0]}" AND data = \'{str(push_data[1])}\''
                                    f'WHERE name = "{push_data[0]}"')
                        conn.commit()
                else:
                    # 同一データが存在しないのでデータをインサートする
                    cur.execute(f'INSERT INTO character(name, data) VALUES("{push_data[0]}", \'{str(push_data[1])}\')')
                    conn.commit()
            else:
                Sg.popup_error('対応できないURLが指定されました',
                               title='error',
                               no_titlebar=True)
            # ボタンを連打してサーバー攻撃しないように1秒待機
            sleep(1)

    # クリップボードにコピーボタン押下処理
    if event == 'bt_copy':
        if not debug_log:
            continue
        if len(window['log'].get()) > 0:
            # GUIのログボックスに表示してる内容をclipboardにコピーする
            if debug_log:
                pyperclip.copy(window['log'].get())
            else:
                pyperclip.copy('')
            # クリップボードにログボックスの中身をコピーしたことをポップアップ
            Sg.popup('クリップボードにコピーしました', title='コピーしました', no_titlebar=True)
        else:
            # urlの入力なしにボタンを押下した場合は警告表示する
            # 他に処理はしない
            Sg.popup_error('コピーすべきデータがありません', title='error', no_titlebar=True)
# データベースの最終コミットと領域開放した後にデータベースを閉じる
conn.commit()
cur.execute('VACUUM')
conn.close()
