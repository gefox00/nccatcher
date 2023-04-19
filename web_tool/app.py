import streamlit as st
import json
import requests
import pyperclip
from PC_Converter_for_web_class import Nccatcher

st.title('ココネクフォーマット')

st.text_input(label='変換したいキャラシのURLを入力', key='-input-')
st.write('このツールはキャラクター保管所（下記URLのサイト）の')
st.write('ネクロニカのキャラクターをココフォリアの駒に変換するためのツールです')
st.write('https://charasheet.vampire-blood.net/')
# セッションのコンポーネントのアクセスを簡略化
asset = st.session_state

get_button = st.button(label='変換結果をコピー', key='-convert-')
# イベント処理
if get_button and len(asset['-input-']) > 0:
    target = asset['-input-'] + '.js'
    target_json = requests.get(target).json()
    print('https://charasheet.vampire-blood.net' in target)
    if 'https://charasheet.vampire-blood.net' in target and target_json['game'] == 'nechro':
        convert = Nccatcher(target_json)
        print(convert.ch_data_js)
        pyperclip.copy(str(convert.ch_data_js).replace("'", '"'))



