import PySimpleGUI as Sg
import API_Loader_method


key_data = {'タイトル': 'title', '名前': 'name'}

base_url = 'https://charasheet.vampire-blood.net/list_nechro.html'
API = API_Loader_method.ApiGetter(base_url=base_url, search_target={})
#          1行目
layout = [[Sg.Text('検索ワードを入力し検索データカテゴリを選択して実行ボタンを押してください')],
          # 2行目
          [Sg.Input(size=72, key='target')],
          # 3行目
          [Sg.Button(button_text='検索', size=62, key='bt_start')],
          # 4行目
          [Sg.Text(text='検索結果')],
          # 5行目
          [Sg.Text(text='ヒットしたデータ')],
          # 6行目
          [Sg.Combo([''], size=56, default_value='', key='select'),
           Sg.Button(button_text='データ確認', size=10, key='bt_start')],
          # 7行目
          [Sg.Text(text='データ内容')],
          # 8行目
          [Sg.MLine(size=(70, 10), key='tb_out')],
          # 9行目
          [Sg.Button(button_text='ココフォリア形式でデータを取得', size=30, key='bt_get_coco'),
           Sg.Button(button_text='保管所形式でデータを取得', size=30, key='bt_get_coco')]]
#
window = Sg.Window(layout=layout, title=' ')

end_window = True

while end_window:
    event, values = window.read()
    print(event, values)
    match event:
        case Sg.WIN_CLOSED:
            end_window = False
            break

        case 'bt_start':
            API.target = values['target']
            getlist = API.get_target_list()
            window['select'].Update(values=getlist)
        case 'select':
            print('select!!')
        case _:
            break
