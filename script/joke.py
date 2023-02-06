import requests
from PIL import Image
import io
import PySimpleGUI as sg
import os


def get_pic():
    get_fox = requests.get("https://randomfox.ca/floof/").json()
    a_img = Image.open(io.BytesIO(requests.get(get_fox['image']).content))
    bio = io.BytesIO()
    a_img.save(fp=bio, format='png')
    return {'pic_io': bio.getvalue(), 'pic_url': get_fox['image']}


sg.theme('DarkAmber')
layout = [[sg.Button('show_pic', key='bush'), sg.Button('get_this_pic', key='buge', visible=False)],
          [sg.Image(key='pic', size=(500, 500))]]

window = sg.Window('サンプルプログラム', layout)
urls = ''
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'bush':
        get_data = get_pic()
        window['pic'].update(get_data['pic_io'])
        window['buge'].update(visible=True)
        urls = get_data['pic_url']
    if event == 'buge':
        getpic = requests.get(urls)
        result = sg.popup_get_file("ファイルを選択してください", file_types=(("jpeg画像", ".jpg"),))


window.close()
