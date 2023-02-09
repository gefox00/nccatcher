import requests




base_url = 'https://charasheet.vampire-blood.net/list_nechro.html'
res = requests.get(base_url, data={'name': 'ドール', 'tag': 'ドール'})
print(res.text)
