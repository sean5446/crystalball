import sqlite3
import datetime


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
            try:
                cur = con.cursor()
                cur.execute(f"update stocks set symbol='{symbol}', date='{datetime.datetime}' where id=1")
                con.commit()
            except Exception as ex:
                print(ex)

    def get_stock(self, symbol):
        with sqlite3.connect(self.db_name) as con:
            try:
                cur = con.cursor()
                res = cur.execute(f"select * from stocks where id=1")
                stock = res.fetchall()
                db_date = stock[0][1]
                db_symbol = stock[0][2]
                if db_symbol is not symbol:
                    self.set_stock(symbol)
                else:
                    return symbol, db_date
            except Exception as ex:
                cur = con.cursor()
                cur.execute(f"insert into stocks values (1, '{symbol}', '{datetime.datetime}')")
                con.commit()
                return True

    def set_awake_status(self, status: int):
        with sqlite3.connect(self.db_name) as con:
            try:
                cur = con.cursor()
                cur.execute(f"update status set awake={status} where id=1")
                con.commit()
            except Exception as ex:
                print(ex)

    def get_awake_status(self) -> bool:
        with sqlite3.connect(self.db_name) as con:
            try:
                cur = con.cursor()
                res = cur.execute(f"select awake from status where id=1")
                awake = res.fetchall()
                return bool(awake[0][0])
            except Exception as ex:
                cur = con.cursor()
                cur.execute(f"insert into status values (1, 1)")
                con.commit()
                return True
