import sqlite3


def delete_all():
    con = sqlite3.connect('data/database/users.db')
    cur = con.cursor()
    query = '''DELETE FROM user'''
    cur.execute(query)
    con.commit()
    con.close()
