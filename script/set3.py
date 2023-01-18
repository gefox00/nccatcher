import json

with open('data.json', 'r', encoding='utf8')as r:
    data = json.load(r)
    for i in data:
        print(i, data[i])