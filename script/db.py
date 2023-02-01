import sqlite3


class NcDataBase:
    dbname = 'data_file/my_char.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    print('db open')

    def __init__(self):
        self.table_set()

    def __del__(self):
        print('DB closing')
        self.cur.execute('VACUUM')
        self.cur.close()
        self.conn.close()
        print('DB close complete')

    def table_set(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS '
                         'character(name STRING, data STRING)')
        self.cur.execute('CREATE TABLE IF NOT EXISTS '
                         'base_character(title STRING, tag STRING, name STRING, data STRING)')
        self.cur.execute('CREATE TABLE IF NOT EXISTS '
                         'maneuver(name STRING, equip INTEGER, timing INTEGER, '
                         'cost INTEGER, range STRING, text STRING)')
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

