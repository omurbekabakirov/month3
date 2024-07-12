create_table_model = '''
CREATE TABLE IF NOT EXISTS models(
id INTEGER PRIMARY KEY,
tg_id INTEGER ,
model_name TEXT ,
category TEXT,
price INTEGER,
photo TEXT,
UNIQUE (tg_id)
)
'''
insert_into_table_model = '''
INSERT INTO models VALUES (?,?,?,?,?)'''