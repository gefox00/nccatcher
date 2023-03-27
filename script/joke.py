import PySimpleGUI as Sg
import pyperclip
import json
import os

M_timing = ['Au', 'Ac', 'Ra', 'Ju', 'Da']
M_range = [str(i) for i in range(5)]
M_range.append('自身')
M_range.append('効果参照')
Sg.theme('DarkBlue3')
menu_items = [['ファイル', ['ファイルから開く', 'ファイルに保存']]]
layout = [[Sg.Menu(menu_items, key='file_menu')],
          [Sg.Text('駒名称'), Sg.Input(key='main_name', size=57)],
          [Sg.Column(
              [
                  [Sg.Text('悪意'), Sg.Input(key='main_EXP', size=5),
                   Sg.Text('行動値'), Sg.Input(key='main_AP', size=5),
                   Sg.Text('ユニット数'), Sg.Input(key='main_unit', size=5)]
              ])
           ],
          [Sg.Text('マニューバ編集')],
          [Sg.Text('マニューバ名称'), Sg.Input(key='M_name', size=49)],
          [Sg.Text('タイミング'), Sg.Combo(values=M_timing, size=4, key='M_timing'),
           Sg.Text('コスト'), Sg.Input(key='M_cost', size=8),
           Sg.Text('射程'), Sg.Combo(values=M_range, key='M_range', size=8)],
          [Sg.Text('効\n果\n内\n容'), Sg.MLine(key='M_effect', size=(60, 10))],
          [Sg.Button(button_text='マニューバ登録', size=58, key='resist_data')],
          [Sg.Text('登録マニューバ')],
          [Sg.Table(headings=['名称', 'タイミング', 'コスト', '射程', '効果'],
                    auto_size_columns=False, values=[],
                    size=(48, 10),  justification='center',
                    key='MN_table', max_col_width=20, background_color='white', text_color='black',
                    alternating_row_color='skyblue'
                    )],

          [Sg.Button(button_text='駒出力', size=58, key='output')]
          ]

window = Sg.Window('Rエディタ', layout)
end_bol = True
while end_bol:

    event, values = window.read()
    match event:
        case Sg.WINDOW_CLOSED:
            end_bol = False
            break
        case 'resist_data':
            mn_data = {'name': window['M_name'].get(),
                       'timing': window['M_timing'].get(),
                       'cost': window['M_cost'].get(),
                       'range': window['M_range'].get(),
                       'effect': window['M_effect'].get()}
            tables = window['MN_table'].get()
            tables.append([mn_data['name'],
                           mn_data['timing'],
                           mn_data['cost'],
                           mn_data['range'],
                           mn_data['effect']
                           ])
            window['MN_table'].update(tables)
            print(window['MN_table'].get())
        case 'output':
            clip_data = {"kind": "character", "data": {"name": window['main_name'].get()}}
            clip_data["data"]['initiative'] = window['main_AP'].get()

        case 'ファイルから開く':
            open_file = Sg.popup_get_file('このツールで作成したレギオンのJsonを指定してください',
                                          file_types=(("Json", "*.json"),))
            with open(open_file, 'r', encoding='utf8')as r:
                data = json.load(r)
        case 'ファイルに保存':
            save_file = Sg.popup_get_file("保存するファイル名を入力してください",
                                          save_as=True,
                                          file_types=(("Json", "*.json"),))

        case _:
            end_bol = False
            break


window.close()
