import glob
import json
from PC_Converter_for_web_class import Nccatcher


for i in glob.glob(fr'D:\Desktop\nccatcher\endata\*.json'):
    with open(i, 'r', encoding='utf8')as r:
        data = json.load(r)
        print(Nccatcher(data=data).ch_data)

