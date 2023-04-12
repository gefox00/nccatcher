import json_file
import pyperclip


class nccatcher:
    # 変換結果を外部から取得するために設置
    ch_data = ""

    def __init__(self, data: {}, URL: str):
        self.conv(data, URL)

    # 処理本体
    def conv(self, jsdata: {}, ch_URL, clip: bool = True):
        data = jsdata
        # デバッグ用に残しておく
        # with open('testdata.json_file','r',encoding='utf8')as r:
        #     data = json_file.load(r)
        # clipboardAPIの決まり文句
        out_data = {"kind": "character"}
        parts_data = []
        parts_sysdata = []
        eq_h = 0
        eq_a = 0
        eq_b = 0
        eq_l = 0
        memo = '----カルマ----\n'
        command = 'NM 未練判定\n1NC 行動判定\n1NC+1 行動判定\n1NC+2 行動判定\n1NC+3 行動判定\n' \
                  '1NC 狂気・対話判定\n1NC+1 狂気・対話判定\n1NC+2 狂気・対話判定\n1NC+3 狂気・対話判定\n' \
                  ':狂気減少上限+1\n:狂気減少上限=0\n'
        partdata = {1: 'ポジション', 2: 'メインクラス', 3: 'サブクラス', 4: '頭', 5: '腕', 6: '胴', 7: '足'}
        timingdata = {0: 'オート', 1: 'アクション', 2: 'ラピッド', 3: 'ジャッジ', 4: 'ダメージ'}

        for i in data['carma_name']:
            memo += i + '\n'
        memo += '----きおくのかけら----\n'
        for i in data['kakera_name']:
            memo += i + '\n'

        with open('data.json_file', 'r', encoding='utf8') as r:
            much = json_file.load(r)
            for name, hantei, timing, cost, d_range in zip(data['Power_name'], data['Power_hantei'],
                                                           data['Power_timing'], data['Power_cost'],
                                                           data['Power_range']):
                if int(hantei) == 4:
                    eq_h += 1
                if int(hantei) == 5:
                    eq_a += 1
                if int(hantei) == 6:
                    eq_b += 1
                if int(hantei) == 7:
                    eq_l += 1
                try:
                    insert = ""
                    for z in much:
                        if z in name:
                            insert = much[z]
                    parts_data.append(
                        f'[{partdata[int(hantei)]}] {name}: {timingdata[int(timing)]} : {cost} : {d_range} : {insert}')
                except:
                    parts_data.append(
                        f'[{partdata[int(hantei)]}] {name}: {timingdata[int(timing)]} : {cost} : {d_range} : nodata')
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
            cocost_data.append({'label': f'PL{i + 1}への未練', 'value': 3, 'max': 4})
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
            cocopa_data.append({'label': i[0], 'value': 'ALIVE'})
        for i in parts_data:
            command += i + '\n'
        temp = {'name': data['pc_name'], 'initiative': int(data['Act_Total']),
                'externalUrl': str(ch_URL),
                'memo': memo, 'commands': command,
                'status': cocost_data, 'params': cocopa_data}
        out_data['data'] = temp
        # クリップボード変換したデータを書き込みインスタンスしたときにオンオフ切替
        self.ch_data = str(out_data).replace('\'', '"')
        if clip:
            pyperclip.copy(self.ch_data)
