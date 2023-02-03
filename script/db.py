import sqlite3


# このクラスではデータベースのクエリと一定操作をまとめて記述する
class NcDataBase:
    dbname = 'data_file/my_char.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    # DBがオープンされていることを通知
    print('db open')

    def __init__(self):
        self.table_set()

    def __del__(self):
        # デストラクタでコネクションとカーソルを破棄とvacuumを実行してDBの最適化をする
        print('DB closing')
        self.cur.execute('VACUUM')
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        print('DB close complete')

    def mn_inserter(self, data: [[]]):
        for i in data:
            sql = f'INSERT INTO maneuver(name, equip, timing, cost, range, text, category)' \
                  f'VALUES("{i[0]}","{i[1]}","{i[2]}","{i[3]}","{i[4]}","{i[5]}","{i[6]}")'
            self.conn.execute(sql)
            self.conn.commit()

    def mnn_data_get(self, target):
        sql = fr'SELECT * FROM maneuver ' \
              fr'WHERE name like "%{target}%"'
        print(sql)
        return self.cur.execute(sql).fetchall()

    def table_set(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS '
                         'character(name STRING, data STRING)')
        self.cur.execute('CREATE TABLE IF NOT EXISTS '
                         'base_character(title STRING, tag STRING, name STRING, data STRING)')
        self.cur.execute('CREATE TABLE IF NOT EXISTS '
                         'maneuver(name STRING, equip STRING, timing STRING, '
                         'cost STRING, range STRING, text STRING, category STRING)')
        self.cur.execute('CREATE TABLE IF NOT EXISTS '
                         'original_sheet(md STRING, id STRING, name STRING, json STRING)')
        self.conn.commit()

    def check_tbl_original_sheet_rows(self, data: []):
        back = self.cur.execute(f'SELECT COUNT(*) '
                                f'FROM original_sheet '
                                f'WHERE md = "{data[0]}" AND '
                                f'id "{data[1]}" AND '
                                f'name = {data[0]}').fetchone()
        return int(back[0])

    def original_data_update(self, push_data: {}):
        self.cur.execute(f'UPDATE original_sheet '
                         f"SET name = '{push_data['name']}' , json = '{push_data['json']}'"
                         f"WHERE md = '{push_data['md']}' AND id = '{push_data['id']}'")
        self.conn.commit()

    def original_data_insert(self, push_data: {}):
        self.cur.execute(f"INSERT INTO original_sheet(md, id, name, json) "
                         f"VALUES('{push_data['md']}', '{push_data['id']}', "
                         f"'{push_data['name']}', '{str(push_data['json'])}')")
        self.conn.commit()

    def check_tbl_character_rows(self, data_name: ''):
        back = self.cur.execute(f'SELECT COUNT(*) FROM character WHERE name = "{data_name}"').fetchone()
        return int(back[0])

    def coco_ch_update(self, push_data: []):
        self.cur.execute(f'UPDATE character '
                         f'SET data = \'{str(push_data[1])}\''
                         f'WHERE character.name = "{push_data[0]}"')
        self.conn.commit()

    def coco_ch_insert(self, push_data: []):
        self.cur.execute(f'INSERT INTO character(name, data) '
                         f'VALUES("{push_data[0]}", \'{str(push_data[1])}\')')
        self.conn.commit()

    def base_ch_insert(self, insert_data: []):
        self.cur.execute(f'INSERT INTO character(name, data) '
                         f'VALUES("{insert_data[0]}", \'{str(insert_data[1])}\')')
        self.conn.commit()
