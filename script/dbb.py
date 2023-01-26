import sqlite3


dbname = 'data_file/my_char.db'
# DBを作成する（既に作成されていたらこのDBに接続する）
conn = sqlite3.connect(dbname)
cur = conn.cursor()
data = cur.execute('SELECT * FROM character')

for i in data:
    print(i)


# DBとの接続を閉じる(必須)
conn.close()
