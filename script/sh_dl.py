import PySimpleGUI as Sg


category_data = {'タイトル': '?title=', 'タグ': '?tag=', '名前': '?name='}

base_url = 'https://charasheet.vampire-blood.net/list_nechro.html'
#          1行目
layout = [[Sg.Text('検索ワードを入力し検索データカテゴリを選択して実行ボタンを押してください')],
          # 2行目
          [Sg.Input(size=60),
           Sg.Combo(list(category_data.keys()), size=8, default_value='名前', key='category')],
          # 3行目
          [Sg.Button(button_text='実行', size=62, key='bt_start')],
          # 4行目
          [Sg.Text(text='検索結果')],
          # 5行目
          [Sg.Text(text='ヒットしたデータ')],
          # 6行目
          [Sg.Combo(values=['a', 'b'], size=70, default_value='', key='select')],
          # 7行目
          [Sg.Text(text='データ内容')],
          # 8行目
          [Sg.MLine(size=(70, 10), key='tb_out')]]
#
window = Sg.Window(layout=layout, title=' ')

end_window = True
while end_window:
    event, values = window.read()

    match event:
        case Sg.WIN_CLOSED:
            end_window = False
            break

        case 'bt_start':
            window['select'].Update(values=['c', 'd'])
            window['select'].Update(value='d')
            print('get')

for i in range(10):
    break
    data = requests.get("https://charasheet.vampire-blood.net/me58c7745269933f1080637f585dfa201.js")
    print(i, data.json())
    sleep(0.4)
