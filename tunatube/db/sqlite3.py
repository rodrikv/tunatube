import sqlite3

def connect(db_name='db.sqlite3'):
    con = sqlite3.connect(db_name)
    return con


def create_file_id_table(con):
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            file_id TEXT UNIQUE,
            file_name TEXT
        )''')
    con.commit()

def insert_file_id(con, file_id, file_name):
    cur = con.cursor()
    cur.execute('''INSERT INTO files (file_id, file_name) VALUES (?, ?)''', (file_id, file_name))
    con.commit()


def get_file_id(con, file_name):
    cur = con.cursor()
    cur.execute('''SELECT * FROM files WHERE file_name = ?''', (file_name,))
    return cur.fetchone()