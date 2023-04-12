import PySimpleGUI as Sg

menu_items = [['ファイル', ['ファイルから開く', 'ファイルに保存']],
              ['Nscripter', ['実行', 'スクリプト書き出し']]
              ]
R_menu = ['&Right', ['選択行の内容を編集', ['キャラ名/コマンド', 'セリフ', '目', '眉', '口',
                                                '立ち位置', 'エフェクト', ['f']],
                     '&選択行を削除', ['None']
                     ]
          ]
main_layout = [[Sg.Menu(menu_items, key='file_menu')],
               [Sg.Table(headings=['キャラクター/コマンド', 'セリフ/コマンド引数',
                                   '文字数', '目',
                                   '眉', '口',
                                   '立ち位置', 'エフェクト',
                                   'エフェクトタイム', '声感情',
                                   'ボイスファイル名', 'キャスト'],
                         auto_size_columns=False,
                         col_widths=[20, 65, 7, 5, 5, 5, 8, 10, 14, 8, 16, 8],
                         values=[],
                         key='MN_table',
                         background_color='white',
                         text_color='black',
                         justification='center',
                         enable_events=True,
                         right_click_menu=R_menu,
                         alternating_row_color='skyblue')
                ]
               ]
window = Sg.Window(title='', layout=main_layout, size=(1600, 900))

while True:
    event, values = window.read()
    if event == Sg.WINDOW_CLOSED:
        break
