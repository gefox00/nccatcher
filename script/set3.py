import requests

# サーバーからデータを取得
url = 'https://charasheet.vampire-blood.net/4809281.js'
# データをJsonで確保
res = requests.get(url).json()
# データ組み立て用変数のセット
command = ''
param = []
out_data = {"kind": "character"}
cocost_data = {}
for cat, flv, name in zip(res['Powers_lv'], res['Powers_kouka'], res['Powers_name']):
    command += name + ' : {' + name + '}\n'
    param.append({'label': name, 'value': flv})
    pass

temp = {'name': res['pc_name'], 'initiative': 0,
        'externalUrl': str(url), 'memo': '', 'commands': command,
        'status': cocost_data, 'params': param}

print(command)



