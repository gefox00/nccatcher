import sqlite3
import PySimpleGUI as Sg

dbname = 'data_file/my_char.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS character(name STRING, data STRING)')
cur.execute('CREATE TABLE IF NOT EXISTS maneuver(name STRING, equip STRING, '
            'timing STRING, cost STRING, range STRING, text STRING)')

layout = [[Sg.Input(size=70)],
          [Sg.Input(size=15), Sg.Input(size=15), Sg.Input(size=15), Sg.Input(size=15)],
          [Sg.MLine(size=(68, 15))],
          [Sg.Button(button_text='登録')]
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

