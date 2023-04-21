import sqlite3
from live.socket import LiveSocket

class MyLiveSocket(LiveSocket):
    def __init__(self, room_id=None, uid=None):
        super().__init__(room_id, uid)

        # 初始化數據庫
        self.db_path = './database/live.db'
        self.db_conn = sqlite3.connect(self.db_path)
        self.db_cursor = self.db_conn.cursor()
        self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS danmu
            (message varchar, uname varchar, uid int, is_admin bit, time varchar, `room id` int);
            """)
        self.db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS gift
        (gift varchar, count int, uname varchar, uid int, time varchar, `room id` int);
        """)
        self.db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS guard
        (level varchar, uname varchar, uid int, time varchar, `room id` int);
        """)
        # TODO
        # self.db_cursor.execute("""
        # CREATE TABLE IF NOT EXISTS 
        # """)
        self.db_conn.commit()

        self.start()
    
    def on_close(self, ws, *args):
        super().on_close(ws, *args)
        self.db_conn.close()

    # 覆寫收到對應指令碼時的動作
    def on_gift(self):
        self.db_cursor.execute("""INSERT INTO gift VALUES (?, ?, ?, ?, ?, ?);""", tuple(self.msg.values()) + (self.room_id,))
        self.db_conn.commit()

    def on_danmu(self):
        self.db_cursor.execute("""INSERT INTO danmu VALUES (?, ?, ?, ?, ?, ?);""", tuple(self.msg.values()) + (self.room_id,))
        self.db_conn.commit()

    def on_guard(self):
        self.db_cursor.execute("""INSERT INTO guard VALUES (?, ?, ?, ?, ?);""", tuple(self.msg.values()) + (self.room_id,))
        self.db_conn.commit()

    def on_interact(self):
        pass


MyLiveSocket(uid=128912828)