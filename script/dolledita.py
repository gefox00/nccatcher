import PySimpleGUI as Sg
from time import sleep

radio_dic = {
    '-1-': 'aaa',
    '-2-': 'bbb',
    '-3-': 'ccc',
}

layout = [[Sg.Input(), Sg.Input(), ],
          [Sg.Input(), Sg.Input(), Sg.Input()],
          [Sg.Text(), Sg.Text(), Sg.Text()],
          [Sg.Radio(item[1], key=item[0], group_id='radio') for item in radio_dic.items()],
          []]

window = Sg.Window(layout=layout, title='')

end_flag = True
while end_flag:
    sleep(0.1)
    event, value = window.read()
    print(event)
    try:
        if event == Sg.WIN_CLOSED:
            # ｘボタンはそのままプログラムの終了処理にする
            end_flag = False
            break
    except Sg.WIN_CLOSED:
        break
