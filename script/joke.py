import PySimpleGUI as Sg
import pyperclip
import json
import cocofolia_clip_api
a = "" \
    ""

# ファイルメニューの挙動制御
def top_menu(menu_event: str, target_data=None):
    match event:
        # ファイルから読込
        case 'load':
            pass

        # ファイルに保存
        case 'save':
            pass
    pass


def get_selected_row(table: Sg.Table, mode: str):
    match mode:
        case 'del':
            if len(table.SelectedRows) == 0:
                return None
            del table.get()[table.SelectedRows[0]]
            table.update(table.get())
        case _:
            return None

def make_region():
    # チャパレ初期化と組み立て
    command_sauce = '-----ダイス-----\nchoice[PC1, PC2, PC3, PC4]\n:ユニット数+\n:ユニット数-\n:悪意\n'
    for i in range(3):
        command_sauce += f'NA+{i + 1}\n'
    for i in range(3):
        command_sauce += f'NA-{i + 1}\n'
    command_sauce += '-----マニューバ-----\n'
    # 入力したマニューバをチャパレ用文字列に組み換え
    for i in window['MN_table'].get():
        command_sauce += f'{i[0]}《{i[1]}:{i[2]}:{i[3]}》{i[4]}\n'
    # GUIで入力したココフォリア上で値の操作が必要な項目をステータスに変換
    status = [{'label': 'ユニット数', 'value': int(window['main_unit'].get()),
               'max': int(window['main_unit'].get())}
              ]
    # GUIで入力した固定値をパラメータに変換
    params = [{'label': '悪意', 'value': int(window['main_EXP'].get())}]
    clip_data.set_commands(command_sauce)
    clip_data.set_params(params)
    clip_data.set_status(status)
    clip_data.set_name(window['main_name'].get())
    clip_data.set_initiative(int(window['main_AP'].get()))


clip_data = cocofolia_clip_api.ClipApi()
M_timing = ['', 'Au', 'Ac', 'Ra', 'Ju', 'Da']
M_range = [str(i) for i in range(5)]
M_range.insert(0, '')
for i in [f"{i}-{j}" for i in range(4) for j in range(i+1, 5)]:
    M_range.append(i)
M_range.append('自身')
M_range.append('効果参照')
Sg.theme('DarkBlue3')
menu_items = [['ファイル', ['ファイルから開く', 'ファイルに保存']]]
layout = [[Sg.Menu(menu_items, key='file_menu')],
          [Sg.Text('駒名称'), Sg.Input(key='main_name', size=57)],
          [Sg.Text('悪意'), Sg.Input(key='main_EXP', size=5),
           Sg.Text('行動値'), Sg.Input(key='main_AP', size=5),
           Sg.Text('ユニット数'), Sg.Input(key='main_unit', size=5)],
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
                    size=(48, 10), key='MN_table',
                    background_color='white', text_color='black',
                    justification='center', enable_events=True,
                    right_click_menu=['&Right', ['選択行の内容を編集',
                                                 ['名称', 'タイミング', 'コスト', '射程', '効果内容'],
                                                 '&選択行を削除']],
                    alternating_row_color='skyblue')
           ],
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
            window['MN_table'].update(enable_events=True)
        case 'output':
            make_region()
            pyperclip.copy(clip_data.txt_out())

        case 'ファイルから開く':
            make_data = 0
            target = ['main_name', 'main_EXP', 'main_AP', 'main_unit',
                      'M_name', 'M_timing', 'M_cost', 'M_range', 'M_effect', 'MN_table']
            for i in target:
                make_data += len(window[i].get())
            if make_data > 0:
                if Sg.popup_ok_cancel('編集中のデータを上書きしますがファイルを開きますか？') == 'Cancel':
                    print('get')
                    continue

            open_file = Sg.popup_get_file('このツールで作成したレギオンのJsonを指定してください',
                                          file_types=(("Json", "*.json"),))
            with open(open_file, 'r', encoding='utf8')as r:
                data = json.load(r)

        case 'ファイルに保存':
            save_file = Sg.popup_get_file("保存するファイル名を入力してください",
                                          save_as=True,
                                          file_types=(("Json", "*.json"),))
            with open(save_file, 'w', encoding='utf8')as w:
                make_region()
                w.write(clip_data.txt_out())
        case '選択行を削除':
            get_selected_row(table=window['MN_table'], mode='del')
        case 'MN_table':
            if values['MN_table']:  # テーブルが選択されている場合
                selected_row_index = values['-TABLE-'][0]
        case _:
            print(values, event)
            # print(event, values)
            end_bol = False
            break
window.close()
