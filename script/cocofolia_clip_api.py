import json


class ClipApi:
    # ココフォリアClipboard APIのテンプレートをインスタンス化
    def __init__(self):
        self.data = {
            "kind": "character",
            "data": {
                "name": "no-name",
                "memo": "",
                "initiative": 0,
                "status": [],
                "params": [],
                "active": True,
                "secret": False,
                "invisible": False,
                "hideStatus": False,
                "color": "#ffffff",
                "commands": "",
            }
        }

    # キャラクター名
    def set_name(self, name: str):
        self.data['data']['name'] = name

    # メモ（改行がそのまま反映されるので文字列でデータを用意する）
    def set_memo(self, memo: str):
        self.data['data']['memo'] = memo

    # イニシアティブ（整数型でないとデータが反映されないので注意する）
    def set_initiative(self, inis: int):
        self.data['data']['initiative'] = inis

    # ステータス（次の形の配列を用意するキーは固定なのでほかのキーは使用しない
    #   {'label': 'ラベル名', 'value': '現在値', 'max': '最大値'})
    def set_append_status(self, status_dict: dict):
        self.data['data']['status'] = status_dict

    # パラメータ（次の形の配列を用意するキーは固定なのでほかのキーは使用しない
    #   {'label': 'ラベル名', 'value': '値'})
    def set_append_params(self, params_dict: dict):
        self.data['data']['params'] = params_dict

    # チャットパレット（改行込みの文字列でデータを用意する。１行ごとにコマンドとして認識されるので改行文字列でOK）
    def set_commands(self, commands_line: str):
        self.data['data']['commands'] = commands_line

    # ステータスを非公開にする
    def set_secret(self, secret: bool):
        self.data['data']['secret'] = secret

    # 発言時キャラクターを表示しない
    def set_invisible(self, invisible: bool):
        self.data['data']['invisible'] = invisible

    # 盤面キャラクター一覧に表示しない
    def set_hide_status(self, hide_status: bool):
        self.data['data']['hideStatus'] = hide_status

    # キャラクター表示文字色の設定
    def set_color(self, color: str):
        self.data['data']['color'] = color

    # 入力されたデータをClipBoardAPIの対応書式で文字列出力
    def txt_out(self):
        return json.dumps(self.data, indent=4)

    # ネクロニカのダイステンプレートをチャットパレットに挿入する
    def set_nechro_dice(self, type_flag: str):
        commands = 'choice[1,2,3,4]\n'
        if type_flag == 'pc':
            commands += 'NM\nNMN\nNME'
        commands += [f'NA+{i+1}\n' for i in range(3)]
        commands += [f'NA-{i+1}\n' for i in range(3)]

    # チャットパレットに追記する
    def set_append_command(self, append_line: str):
        self.data['data']['commands'] += append_line
