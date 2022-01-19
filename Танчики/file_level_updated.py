import sqlite3


def game_level_update(game_level):
    bd = sqlite3.connect("data/database/users.db")
    bd_cur = bd.cursor()
    f = open('data/user.txt', 'r')
    id = f.readline()
    f.close()
    bd_cur.execute(f'SELECT * FROM user WHERE id="{id}"')
    value = bd_cur.fetchall()
    if game_level != value[0][3]:
        bd_cur.execute(f"UPDATE user \
                        SET gamelevel = {game_level} \
                        WHERE id = '{id}'")
        bd.commit()
    bd_cur.close()
    bd.close()