import json


class ClipApi:
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

    def set_name(self, name: str):
        self.data['data']['name'] = name

    def set_memo(self, memo: str):
        self.data['data']['memo'] = memo

    def set_initiative(self, inis: int):
        self.data['data']['initiative'] = inis

    def set_status(self, status: list):
        self.data['data']['status'] = status

    def set_params(self, params: list):
        self.data['data']['params'] = params

    def set_commands(self, commands: str):
        self.data['data']['commands'] = commands

    def set_secret(self, secret: bool):
        self.data['data']['secret'] = secret

    def set_invisible(self, invisible: bool):
        self.data['data']['invisible'] = invisible

    def set_hide_status(self, hide_status: bool):
        self.data['data']['hideStatus'] = hide_status

    def set_color(self, color: str):
        self.data['data']['color'] = color

    def txt_out(self):
        return json.dumps(self.data, indent=4)
