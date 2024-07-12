import sqlite3
from database import sql_queris


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('db.sqlite3')
        self.cursor = self.conn.cursor()

    def create_table(self):
        if self.conn:
            print("database connected")
        self.cursor.execute(sql_queris.create_table_model)

    def insert_model(self, tg_id, model_name, category, price, photo):
        self.cursor.execute(sql_queris.insert_into_table_model(None, tg_id, model_name, category, price, photo))
        self.conn.commit()
