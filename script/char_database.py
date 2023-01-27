import sqlite3
import PySimpleGUI as Sg
import pyperclip


dbname = 'data_file/my_char.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS character(name STRING, data STRING)')
data = cur.execute('SELECT * FROM character')
database_data = {}
combo_init = ['']
try:
    for i in data:
        database_data[i[0]] = i[1]
        combo_init.append(i[0])
except IndexError:
    combo_init.append('データが1件も登録されていません')


layout = [
            # URL入力用テキストボックスと文字列の配置
            [Sg.Text('データを選び各操作を実行してください')],
            [Sg.Combo(combo_init, default_value=combo_init[0], size=76, key='cb')],
            # ボタンの配置1
            [Sg.Button('クリップボードにコピー', size=20, key='bt_start'),
             Sg.Button('選択データを削除', size=20, key='bt_delete'),
             Sg.Button('データベースをリロード', size=20, key='bt_reload')]
         ]
# ウィンドウタイトル設定
window = Sg.Window(title='cocoホリック', layout=layout)
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
            Sg.Ok('クリップにデータをコピーしました')
        else:
            Sg.popup_error('コピーできるデータがありません', title='error', no_titlebar=True)

    if event == 'bt_delete':
        try:
            pass
        except KeyError:
            pass
    if event == 'bt_reload':
        data = cur.execute('SELECT * FROM character').fetchall()
        combo_init = []
        for i in data:
            combo_init.append(i[0])
        window['cb'].update(combo_init)
        Sg.Ok('データ再読み込み完了')
conn.close()
