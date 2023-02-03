import sqlite3
import PySimpleGUI as Sg

dbname = 'data_file/my_char.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS character(name STRING, data STRING)')
cur.execute('CREATE TABLE IF NOT EXISTS maneuver(name STRING, equip STRING, '
            'timing STRING, cost STRING, range STRING, text STRING)')

layout = [
            # URL入力用テキストボックスと文字列の配置
            [Sg.Text('Name'), Sg.Input(size=(62, 1), key='tb_open')],
            [Sg.Checkbox('データベースに記憶する', key='chb')],
            # ボタンの配置1
            [Sg.Button('変換開始', size=37, key='bt_start'),
             # ボタンの配置
             Sg.Button('クリップボードにコピー', size=37, key='bt_copy')]
            # 変換結果表示用テキストボックスの配置
         ]
window = Sg.Window(title='', layout=layout)

end_flag = True
while end_flag:
    event, value = window.read()
    match event:
        case Sg.WIN_CLOSED:
            end_flag = False
        case '':
            pass
        case _:
            break

