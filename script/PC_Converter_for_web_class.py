import json
import sqlite3


class Nccatcher:
    # 変換結果を格納
    ch_data = ""
    ch_data_js = {}

    dbname = 'data_file/my_char.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    def __del__(self):
        self.dispose(self.conn, self.cur)

    def dispose(self, del_conn, del_cur):
        del_conn.commit()
        del_cur.execute('VACUUM')
        del_conn.close()

    def __init__(self, data: {}, url: str, db_dir: str = 'data_file/my_char.db'):
        self.conv(data, url)

    # 処理本体
    def conv(self, jsdata: {}, ch_url):
        # GUIから受け取ったJsonを格納
        data = jsdata

        # clipboardAPIの決まり文句
        out_data = {"kind": "character"}

        # チャットパレット設定用変数定義
        parts_data = []
        command = ''

        # パラメータ設定用変数定義
        parts_sysdata = []

        # 部位のアイテムカウント用変数定義
        eq_h = 0
        eq_a = 0
        eq_b = 0
        eq_l = 0

        # メモ設定用変数定義
        sys_memo = '----カルマ----\n'

        # 挿入用データセット
        partdata = {0: 'None', 1: 'ポジション', 2: 'メインクラス', 3: 'サブクラス', 4: '頭', 5: '腕', 6: '胴', 7: '足'}
        timingdata = {0: 'オート', 1: 'アクション', 4: 'ラピッド', 2: 'ジャッジ', 3: 'ダメージ'}

        # チャットパレットの提携挿入コマンドを読込
        with open('data_file/cmdtxt.txt', 'r', encoding='utf8')as r:
            for i in r.read().splitlines():
                command += i + '\n'

        # Jsonからカルマを取得してメモに挿入
        for i in data['carma_name']:
            sys_memo += i + '\n'

        # Jsonからきおくのかけらを取得してメモに挿入
        sys_memo += '----きおくのかけら----\n'
        for i in data['kakera_name']:
            sys_memo += i + '\n'

        # マニューバデータベースの読込と出力データ作成
        with open('data_file/data.json', 'r', encoding='utf8')as r:
            much = json.load(r)
            # マニューバデータの作成
            # Jsonからマニューバを読み込んでチャパレ用に成形する
            for name, hantei, timing, cost, d_range, memo in zip(data['Power_name'], data['Power_hantei'],
                                                                 data['Power_timing'], data['Power_cost'],
                                                                 data['Power_range'], data['Power_memo']):
                # 各部位のアイテム数をカウント
                match int(hantei):
                    case 4:
                        eq_h += 1
                    case 5:
                        eq_a += 1
                    case 6:
                        eq_b += 1
                    case 7:
                        eq_l += 1
                # 辞書型の仕様を利用してマニューバの名前でdata.jsonから検索してテキストをマッチング
                try:


                    # 例外のおきようなくね？
                    # 今後修正検討箇所
                    insert = ''
                    # キャラシのマニューバをデータべースからキーワード検索
                    # あいまいな検索方法なため似たような名前の物がヒットしてしまうため正確性はない
                    for m in much:
                        if m in name:
                            insert = much[m]
                    # マッチした場合はマニューバデータにテキストを差し込み
                    parts_data.append(f'[{partdata[int(hantei)]}] '
                                      f'{name}:'
                                      f'{timingdata[int(timing)]}:'
                                      f'{cost}:'
                                      f'{d_range}:'
                                      f'{insert}')
                    # この処理自体例外の出しようがないので下記のエグゼプトは実行されない気がする
                    #
                except KeyError:
                    # マッチしなければ大元のデータを引用する
                    # 例外のおきようがない気がするのでこの処理は必要ない気がする
                    parts_data.append(f'[{partdata[int(hantei)]}] '
                                      f'{name}:{timingdata[int(timing)]}:{cost}:{d_range}:{memo}')
                finally:
                    parts_sysdata.append([name, hantei, timing, cost, d_range])

        temp = []
        for i in partdata:
            for j in parts_sysdata:
                if str(i) == str(j[1]):
                    temp.append(j)
        parts_sysdata = temp
        temp = []
        for i in partdata:
            for j in parts_data:
                if partdata[i] in j:
                    temp.append(j)
        parts_data = temp
        cocost_data = [{'label': '狂気減少上限', 'value': 0, 'max': len(data['kakera_name'])},
                       {'label': '頭残', 'value': eq_h, 'max': eq_h},
                       {'label': '腕残', 'value': eq_a, 'max': eq_a},
                       {'label': '胴残', 'value': eq_b, 'max': eq_b},
                       {'label': '脚残', 'value': eq_l, 'max': eq_l}]
        for i in range(4):
            cocost_data.append({'label': f'PL{i+1}への未練', 'value': 3, 'max': 4})
        cocopa_data = [{'label': 'ポジション', 'value': data['Position_Name']},
                       {'label': 'メインクラス', 'value': data['MCLS_Name']},
                       {'label': 'サブクラス', 'value': data['SCLS_Name']},
                       {'label': '武装', 'value': f'{data["NP1"]}/9'},
                       {'label': '変異', 'value': f'{data["NP2"]}/9'},
                       {'label': '改造', 'value': f'{data["NP3"]}/9'},
                       {'label': '寵愛', 'value': f'{data["exp_his_sum"]}'},
                       {'label': '享年', 'value': data['age']},
                       {'label': '暗示', 'value': data['pc_carma']}
                       ]
        for i in parts_sysdata:
            # print(i)
            cocopa_data.append({'label': i[0], 'value': '使用可能'})
        for i in parts_data:
            command += i + '\n'

        temp = {'name': data['pc_name'], 'initiative': int(data['Act_Total']),
                'externalUrl': str(ch_url), 'memo': sys_memo, 'commands': command,
                'status': cocost_data, 'params': cocopa_data}
        out_data['data'] = temp
        # 変換したデータをオブジェクトで保持
        self.ch_data = str(out_data).replace('\'', '"')
        self.ch_data_js = out_data
