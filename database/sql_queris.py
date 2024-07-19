create_table_store = '''
    CREATE TABLE IF NOT EXISTS online_store (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    name_product TEXT,
    size TEXT,
    price TEXT,
    product_id INTEGER,
    photo TEXT
    )
'''
insert_store = '''
    INSERT INTO online_store(name_product,size,price,product_id,photo) VALUES (?, ?, ?, ?,?)
'''


create_table_details = '''
    CREATE TABLE IF NOT EXISTS prodcut_details(
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    product_id VARCHAR(255),
    category TEXT,
    infoproduct TEXT)
'''

insert_details = '''
INSERT INTO product_details(product_id,category,infoproduct) VALUES (?,?,?)
'''