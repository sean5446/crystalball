
import sqlite3

from datetime import datetime


class Db:
    def __init__(self, db_name):
        self.db_name = db_name

        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("create table if not exists status(id, awake)")
            cur.execute("create table if not exists stocks(id, symbol, date)")
            con.commit()

    def set_stock(self, symbol):
        with sqlite3.connect(self.db_name) as con:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                cur = con.cursor()
                if not self.get_stock():
                    raise RuntimeError
                cur.execute(f"update stocks set symbol='{symbol}', date='{now}' where id=1")
                con.commit()
            except Exception as ex:
                cur = con.cursor()
                print(f"inserting symbol {symbol}")
                cur.execute(f"insert into stocks values (1, '{symbol}', '{now}')")
                con.commit()

    def get_stock(self):
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            res = cur.execute(f"select * from stocks where id=1")
            stock = res.fetchall()
            db_symbol = stock[0][1]
            db_date = stock[0][2]
            return db_symbol, db_date


    def set_awake_status(self, status: int):
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            print(f"setting status {status}")
            cur.execute(f"update status set awake={status} where id=1")
            con.commit()


    def get_awake_status(self) -> bool:
        with sqlite3.connect(self.db_name) as con:
            try:
                cur = con.cursor()
                res = cur.execute(f"select awake from status where id=1")
                awake = res.fetchall()
                return bool(awake[0][0])
            except Exception as ex:
                cur = con.cursor()
                print(f"inserting status 1")
                cur.execute(f"insert into status values (1, 1)")
                con.commit()
                return True
