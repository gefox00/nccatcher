import PySimpleGUI as Sg
import pyperclip
from yukoya import ykch_converter
import time

layout = [[Sg.Input(key='URL'), Sg.Button(button_text='変換', key='CONVERT')],
          [Sg.Text('PL1'), Sg.Input(key='PL1_NAME'), Sg.Text('感情'), Sg.Input(key='PL1_EMO')],
          [Sg.Text('PL2'), Sg.Input(key='PL2_NAME'), Sg.Text('感情'), Sg.Input(key='PL2_EMO')],
          [Sg.Text('PL3'), Sg.Input(key='PL3_NAME'), Sg.Text('感情'), Sg.Input(key='PL3_EMO')],
          [Sg.Text('PL4'), Sg.Input(key='PL4_NAME'), Sg.Text('感情'), Sg.Input(key='PL4_EMO')]]
window = Sg.Window(title='', layout=layout)
end_flag = True
while end_flag:
    event, value = window.read()
    match event:
        case 'CONVERT':
            conv_data = ykch_converter(window['URL'].get()).cocoforia()
            pyperclip.copy(conv_data)
            time.sleep(3)
        case Sg.WIN_CLOSED:
            end_flag = False
            break
        case _:
            end_flag = False
            break
