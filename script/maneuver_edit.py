import PySimpleGUI as Sg
import pprint
import db


db_use = db.NcDataBase()
eq_text = ['任意', '頭', '腕', '胴', '足', 'ポジションスキル', 'クラススキル']
tm_text = ['オート', 'アクション', 'ジャッジ', 'ダメージ', 'ラピッド']

layout = [[Sg.Input(size=70, key='mn_name')],
          [Sg.DropDown(eq_text, key='mn_equip'),
           Sg.DropDown(tm_text, key='mn_timing')],
          [Sg.Input(size=15, key='mn_cost'), Sg.Input(size=15, key='mn_range')],
          [Sg.MLine(size=(68, 15), key='mn_text')],
          [Sg.Button(button_text='登録', key='-REGIST-')]
          ]
window = Sg.Window(title='', layout=layout)

end_flag = True
while end_flag:
    event, value = window.read()
    match event:
        case Sg.WIN_CLOSED:
            end_flag = False
            del db_use
        case '-REGIST-':
            pprint.pprint(dir(window))
            pass
        case _:
            break

