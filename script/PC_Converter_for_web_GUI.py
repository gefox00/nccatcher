import PySimpleGUI as Sg
import requests
import pyperclip
from PC_Converter_for_web_class import Nccatcher
from time import sleep
import os
import json
import db

# コンフィグ？
config = {}
db_use = db.NcDataBase()
# 表示用ヘッダ
log_header = {'name': '名前', 'initiative': '最大行動値', 'externalUrl': '参照URL', 'memo': 'キャラクターメモ',
              'commands': 'チャットパレット', 'status': 'ステータス', 'params': 'パラメータ'}
clip_data = ''
if os.path.isfile('data_file/config.json'):
    with open('data_file/config.json', 'r', encoding='utf8') as r:
        config = json.load(r)
        # デバッグ用フラグ
        # このフラグは手動で切替て使うことにする
        debug_log = config['debug']

else:
    with open('data_file/config.json', 'w', encoding='utf8') as w:
        config['dbcheck'] = True
        config['lastchar'] = True
        config['URL'] = ''
        json.dump(config, w)
# 【メモ】 https: // charasheet.vampire - blood.net / list_nechro.html?name = % E3 % 81 % 82
# データベース操作追加
# コンバーターとコンバート履歴はGUIを分ける使いづらいと感じたら統合する
# ウィンドウに配置するコンポーネント設定
layout = [[Sg.Text('URLを張り付けてください'), Sg.Input(default_text=config['URL'], size=(64, 1), key='tb_open')],
          [Sg.Checkbox('データベースに記憶する', key='chb_dbc', default=bool(config['dbcheck'])),
           Sg.Checkbox('最後に変換したキャラを記憶する', key='chb_last', default=bool(config['lastchar']))],
          [Sg.Button('変換開始', size=38, key='bt_start'), Sg.Button('クリップボードにコピー', size=38, key='bt_copy')]]
if debug_log:
    # デバッグがオフの時はログをlayoutに追加
    layout.append([Sg.MLine(size=(88, 20), key='log')])
else:
    # gefoxの作ったキャラシ
    pyperclip.copy("https://charasheet.vampire-blood.net/me58c7745269933f1080637f585dfa201")

# ウィンドウタイトル設定
window = Sg.Window(title='コンバーター', layout=layout)
end_flag = True
while end_flag:
    # イベントハンドラ
    event, values = window.read()
    load_data = {}
    # ×ボタン押下時の動作
    match event:
        case Sg.WIN_CLOSED:
            # ｘボタンはそのままプログラムの終了処理にする
            end_flag = False
            break
        # ループを抜けるとGUIが終了する
        # 変換開始ボタン押下時の動作
        case 'bt_start':
            # ブランクとキャラシ保管所以外のURLは無視する
            if len(window['tb_open'].get()) > 0 and 'charasheet.vampire-blood.net' in window['tb_open'].get():
                if debug_log:
                    window['log'].update('')
                # APIを叩いてJson取得
                target = window['tb_open'].get() + '.js'
                data = requests.get(target)
                # 非対応チェック
                # 変換できないデータレスポンスを受け取ってないかチェックと対処法をポップアップ
                if '<!DOCTYPE html>' in str(data.content):
                    Sg.popup_error('対応できないURLが指定されました\n'
                                   'URL末尾に「#top」がついている場合は「#top」を消して変換を実行してください',
                                   title='error',
                                   no_titlebar=True)
                    continue
                # 処理可能なデータか中身を確認する
                # URLからなんのタイトルのキャラシか分からないためデータを取得して確かめる
                title = data.json()
                if data.status_code == requests.codes.ok and title['game'] == 'nechro':
                    # キャラシ変換オブジェクトをインスタンス化してデータを処理する
                    get_json = Nccatcher(data=data.json(), url=window['tb_open'].get())

                    str_title = str(title).replace("'", '')

                    db_use.original_data_insert({'md': title['phrase'], 'id': title['data_id'],
                                                 'name': title['data_title'], 'json': str_title})
                    upd = {'id': title['data_id'],
                           'md': title['phrase'],
                           'name': title['data_title'],
                           'json': str_title}
                    db_use.original_data_update(upd)
                    # 変換結果をクリップボードへコピーする
                    clip_data = get_json.ch_data
                    pyperclip.copy(clip_data)

                    # 変換結果をGUIに反映
                    if debug_log:
                        log_data = ""
                        for i in get_json.ch_data_js['data']:
                            log_data += f'{log_header[i]} : {get_json.ch_data_js["data"][i]}\n'
                        window['log'].update(log_data)
                    # クリップボードに結果をコピーしたことをポップアップ
                    Sg.popup('変換結果をクリップボードにコピーしました', title='コピーしました', no_titlebar=True)
                    # 変換したデータをデータベースにインサート
                    # ただし同一キャラ名のキャラはのぞく
                    # テーブルにインサートするデータを作成
                    push_data = [get_json.ch_data_js['data']['name'], get_json.ch_data]
                    # テーブルにインサートするデータと一致するデータがあるか検索して結果を格納
                    row_count = db_use.check_tbl_character_rows(push_data[0])
                    # GUIの情報とデータベースの情報から処理を分岐する
                    # データベースにデータを登録するかチェック
                    if window['chb_dbc'].get():
                        config['dbcheck'] = window['chb_dbc'].get()
                        if int(row_count) > 0:
                            # データベース保存にチェックが入っていて同一キャラ名があったら重複検知をポップアップする
                            value = Sg.popup_ok_cancel('同一名のデータが存在します\nデータを更新しますか？',
                                                       title='重複検知',
                                                       no_titlebar=True)
                            # データの更新意思を確認
                            if value == 'OK':
                                db_use.coco_ch_update(push_data)
                        else:
                            # 同一データが存在しないのでデータをインサートする
                            db_use.coco_ch_insert(push_data)
                else:
                    Sg.popup_error('対応できないURLが指定されました',
                                   title='error',
                                   no_titlebar=True)
                # ボタンを連打してサーバー攻撃しないように1秒待機
                # 一応API自体は平均1秒6リクエストくらい処理できるっぽい（実測）
                sleep(1)

        # クリップボードにコピーボタン押下処理
        case 'bt_copy':
            if not debug_log:
                continue
            if len(window['log'].get()) > 0:
                # 変換したキャラシをclipboardにコピーする
                if debug_log:
                    pyperclip.copy(clip_data)
                else:
                    pyperclip.copy('')
                # クリップボードにログボックスの中身をコピーしたことをポップアップ
                Sg.popup('変換結果をクリップボードにコピーしました', title='コピーしました', no_titlebar=True)
            else:
                # urlの入力なしにボタンを押下した場合は警告表示する
                # 他に処理はしない
                Sg.popup_error('コピーすべきデータがありません', title='error', no_titlebar=True)
# GUIの情報をJsonに保存
with open('data_file/config.json', 'w', encoding='utf8') as w:
    config['dbcheck'] = window['chb_dbc'].get()
    config['lastchar'] = window['chb_last'].get()
    if window['chb_last'].get():
        config['URL'] = window['tb_open'].get()
    else:
        config['URL'] = ''
    json.dump(config, w, indent=4)
# dbクラスを破棄
del db_use
