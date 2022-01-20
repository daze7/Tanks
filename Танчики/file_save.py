import sqlite3


def save(total_score):
    bd = sqlite3.connect("data/database/users.db")
    bd_cur = bd.cursor()
    f = open('data/user.txt', 'r')
    id = f.readline()
    f.close()
    bd_cur.execute(f'SELECT * FROM user WHERE id="{id}"')
    value = bd_cur.fetchall()
    if total_score > value[0][2]:
        bd_cur.execute(f"UPDATE user \
                        SET bestscore = {total_score} \
                        WHERE id = '{id}'")
        bd.commit()
    bd_cur.close()
    bd.close()
