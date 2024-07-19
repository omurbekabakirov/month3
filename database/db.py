import sqlite3
from database import sql_queris

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()


async def create_table():
    if conn:
        print("database connected")
    cursor.execute(sql_queris.create_table_store)
    cursor.execute(sql_queris.create_table_details)
    conn.commit()


async def sql_insert(name_product, size, price, product_id, photo):
    cursor.execute(sql_queris.insert_store,
                   (
                       name_product,
                       size,
                       price,
                       product_id,
                       photo
                   ))
    conn.commit()


async def sql_insert_details(product_id, category, infoproduct):
    cursor.execute(
        sql_queris.insert_details(
            product_id, category, infoproduct
        ))
