import PySimpleGUI as Sg
import pyperclip
from yukoya import ykch_converter
import time

layout = [[Sg.Input(key='URL'), Sg.Button(button_text='変換', key='CONVERT')]]
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
