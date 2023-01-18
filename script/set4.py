import glob
import json
import csv

enmn = []
for i in glob.glob('endata/*'):
    with open(i, 'r', encoding='utf8')as r:
        data = json.load(r)
        mn_data = {}
        if data.get('data_title') == 'バブルヘッド':
            for pn, ph, pt, pc, pr, pm in zip(data['Power_name'], data['Power_hantei'], data['Power_timing'],
                                              data['Power_cost'], data['Power_range'], data['Power_memo']):
                enmn.append([pn, ph, pt, pc, pr, pm])
# enmn = set(enmn)

with open('BH.csv', 'w', newline='\n', encoding='utf8')as w:
    csv.writer(w).writerows(enmn)
