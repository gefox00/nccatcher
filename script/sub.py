import json
with open('ashb.json', 'r', encoding='utf8')as r:
    data = json.loads(r.read())
    for i in data:
        print(i, data[i])


