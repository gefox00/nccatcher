import sqlite3
import requests

data = requests.get('https://charasheet.vampire-blood.net/4745469#top.js')
print(data.content)
