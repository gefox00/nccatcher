import csv
import json


outjson = {}
dataline = {}
header = ['マニューバ名', '装備箇所', 'タイミング', 'コスト', '射程', 'テキスト', 'カテゴリ']

with open('data.csv', 'r', encoding='utf8')as r:
    data = csv.reader(r)
    for i in data:
        if len(i[1]) == 0:
            temp = i
            temp[1] = 'スキル'
            for na, da in zip(header, temp):
                dataline[na] = da
            # 0-6
        else:
            for na, da in zip(header, i):
                dataline[na] = da
        outjson[i[0]] = dataline
        dataline = {}
for i in outjson:
    print(i, outjson[i])
with open('database.json', 'w', encoding='utf8')as w:
    json.dump(outjson, w, indent=4)
