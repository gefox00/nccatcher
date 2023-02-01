import glob
import json_file
from PC_Converter_for_web_class import Nccatcher
from time import sleep


for i in glob.glob(fr'D:\Desktop\nccatcher\endata\*.json'):
    with open(i, 'r', encoding='utf8')as r:
        data = json_file.load(r)

        data = Nccatcher(data=data).ch_data_js
        print(data)
        name = ''
        print(data["data"]["name"])
        if len(data["data"]["name"]) > 0:
            name = data["data"]["name"]
        else:
            name = i
        with open(name, 'w', encoding='utf8')as w:
            json_file.dump(data, w, indent=4)
