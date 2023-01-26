import sqlite3
import PySimpleGUI as Sg
import pyperclip
dbname = 'data_file/my_char.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS character(name STRING, data STRING)')
data = cur.execute('SELECT * FROM character')
database_data = {}
combo_init = []

for i in data:
    database_data[i[0]] = i[1]
    combo_init.append(i[0])

layout = [
            # URL入力用テキストボックスと文字列の配置
            [Sg.Text('データを選び各操作を実行してください')],
            [Sg.Combo(combo_init, default_value=combo_init[0], size=76, key='cb')],
            # ボタンの配置1
            [Sg.Button('クリップボードにコピー', size=33, key='bt_start'),
             Sg.Button('選択データを削除', size=33, key='bt_delete')]
         ]
# ウィンドウタイトル設定
window = Sg.Window(title='コンバーター', layout=layout)
while True:
    # イベントハンドラ
    event, values = window.read()
    if event == Sg.WIN_CLOSED:
        # ループを抜けるとGUIが終了する
        conn.close()
        break

    # 変換開始ボタン押下時の動作
    if event == 'bt_start':
        if len(window['cb'].get()) > 0:
            pyperclip.copy(database_data[window['cb'].get()])
        else:
            Sg.popup_error('コピーできるデータがありません', title='error', no_titlebar=True)

    if event == 'bt_delete':
        a = f'DELETE FROM character WHERE name = {database_data[window["cb"].get()]}'
        conn.commit()
        pass

conn.close()
