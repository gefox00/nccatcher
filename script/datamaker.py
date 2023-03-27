import json
from time import sleep
import requests

base_url = 'https://charasheet.vampire-blood.net/'

for i in range(4834574):
    js_data = requests.get(base_url + str(i + 1) + '.js')
    if js_data.status_code == requests.codes.ok and js_data.json()['game'] == 'nechro':
        print(js_data.json()['game'])
    sleep(1)
