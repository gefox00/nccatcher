import json_file

with open('data.json_file', 'r', encoding='utf8')as r:
    data = json_file.load(r)
    for i in data:
        print(i, data[i])