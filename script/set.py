import csv
import sqlite3
import db
import requests
db = db.NcDataBase()
res = requests.get("https://charasheet.vampire-blood.net/me58c7745269933f1080637f585dfa201.js").json()
data = str(res.keys()).replace('[', '(').replace(']', ' STRING)')[10:-1].replace("'","").replace(","," STRING,")
print(data)

db.conn.commit()


