
import sqlite3

from datetime import datetime


class Db:
    def __init__(self, db_name):
        self.db_name = db_name
        # each table only has one row - using the DB as thread safe, reboot persistent storage
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("create table if not exists status(id integer primary key, awake integer, log text)")
            cur.execute("create table if not exists stocks(id integer primary key, symbol text, date text, close, bid)")
            con.commit()

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
                res = cur.execute("select awake from status where id=1")
                awake = res.fetchall()
                return bool(awake[0][0])
            except Exception as ex:
                cur = con.cursor()
                print(f"inserting initial status")
                cur.execute(f"insert into status values (1, 1, 'no errors yet')")
                con.commit()
                return True

    def set_stock(self, symbol):
        with sqlite3.connect(self.db_name) as con:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                cur = con.cursor()
                if not self.get_stock():
                    raise RuntimeError
                print(f"updating stock {symbol} {now}")
                cur.execute(f"update stocks set symbol='{symbol}', date='{now}' where id=1")
                con.commit()
            except Exception as ex:
                cur = con.cursor()
                print(f"inserting symbol {symbol} {now}")
                cur.execute(f"insert into stocks values (1, '{symbol}', '{now}', '', '')")
                con.commit()

    def set_stock_prices(self, close, bid):
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            print(f"updating stock price close:{close} bid:{bid}")
            cur.execute(f"update stocks set close='{close}', bid='{bid}' where id=1")
            con.commit()

    def get_stock(self):
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            res = cur.execute("select * from stocks where id=1")
            stock = res.fetchall()
            return stock[0][1], stock[0][2], stock[0][3], stock[0][4]

    def set_log_status(self, log: str):
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            print("setting log")
            log = log.replace("'", "''") # really bad escape
            cur.execute(f"update status set log='{log}' where id=1")
            con.commit()

    def get_log_status(self) -> str:
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            res = cur.execute("select log from status where id=1")
            log = res.fetchall()
            return str(log[0][0])
        

