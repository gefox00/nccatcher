import json


class Nccatcher:
    ch_data = ''
    ch_data_js = ''

    # 変換結果を格納
    def __init__(self, data: {}, url: str = ''):
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
        eq_h = sum(x == str(4) for x in data['Power_hantei'])
        eq_a = sum(x == str(5) for x in data['Power_hantei'])
        eq_b = sum(x == str(6) for x in data['Power_hantei'])
        eq_l = sum(x == str(7) for x in data['Power_hantei'])

        # メモ設定用変数定義
        sys_memo = '----カルマ----\n'

        # 挿入用データセット
        partdata = {0: 'None', 1: 'ポジション', 2: 'メインクラス', 3: 'サブクラス', 4: '頭', 5: '腕', 6: '胴', 7: '足'}
        timingdata = {0: 'Au', 1: 'Ac', 4: 'Ra', 2: 'Ju', 3: 'Da'}

        # チャットパレットの提携挿入コマンドを読込
        with open('data_file/cmdtxt.txt', 'r', encoding='utf8') as r:
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
        with open('data_file/data.json', 'r', encoding='utf8') as r:
            much = json.load(r)
            # マニューバデータの作成
            # Jsonからマニューバを読み込んでチャパレ用に成形する
            # 各部位のアイテム数をカウント

            for name, hantei, timing, cost, d_range, memo in zip(data['Power_name'], data['Power_hantei'],
                                                                 data['Power_timing'], data['Power_cost'],
                                                                 data['Power_range'], data['Power_memo']):
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
                                      f'{name}'
                                      f'《{timingdata[int(timing)]}:'
                                      f'{cost}:'
                                      f'{d_range}》'
                                      f'{insert}')
                    # この処理自体例外の出しようがないので下記のエグゼプトは実行されない気がする
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
        # ステータスデータを作成
        cocost_data = [{'label': '狂気減少上限', 'value': 0, 'max': len(data['kakera_name'])},
                       {'label': '頭残', 'value': eq_h, 'max': eq_h},
                       {'label': '腕残', 'value': eq_a, 'max': eq_a},
                       {'label': '胴残', 'value': eq_b, 'max': eq_b},
                       {'label': '脚残', 'value': eq_l, 'max': eq_l},
                       {'label': 'たからもの', 'value': 3, 'max': 4}]
        # キャラシの未練を読み込んでステータスに変換
        for i in range(4):
            cocost_data.append({'label': f'PL{i + 1}への未練', 'value': 3, 'max': 4})
        # 装備マニューバやセッション内で変わることがほぼないデータをパラメータに設定
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
        # パラメータにマニューバを設定
        for i in parts_sysdata:
            # print(i)
            cocopa_data.append({'label': i[0], 'value': '使用可能'})
        # マニューバをチャットパレットに挿入
        for i in parts_data:
            command += i + '\n'
        # クリップボードAPIで読込めるデータに整形
        temp = {'name': data['pc_name'], 'initiative': int(data['Act_Total']),
                'externalUrl': str(ch_url), 'memo': sys_memo, 'commands': command,
                'status': cocost_data, 'params': cocopa_data}
        # 最終形態
        out_data['data'] = temp
        # クリップボードAPIの仕様に合わせてここまでで作成したデータを辞書オブジェクトから文字列に変換
        self.ch_data = str(out_data).replace('\'', '"')
        # 他のプログラムでデータを再利用するため辞書型も別途保持
        self.ch_data_js = out_data
