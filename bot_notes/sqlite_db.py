import sqlite3 as sq

async def db_connect():
    global db, cur
    db = sq.connect("new.db")
    cur = db.cursor()

    db.commit()


async def create_new_table(user_id):
    table_name = "user_" + str(user_id)
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name}(notes_id INTEGER PRIMARY KEY,name TEXT)")

    db.commit()

async def get_all_notes(user_id):
    table_name = "user_" + str(user_id)
    notes = cur.execute(f"SELECT * FROM {table_name}").fetchall()

    return notes


async def  create_new_notes(state,user_id):
    table_name = "user_" + str(user_id)
    async with state.proxy() as data:
        notes = cur.execute(f"INSERT INTO {table_name} (name)VALUES (?)",(data["name"],))

        db.commit()

    return notes


async def delete_notes(user_id ,notes_id: int) -> None:
    table_name = "user_" + str(user_id)

    cur.execute(f"DELETE FROM {table_name} WHERE notes_id = ?", (notes_id,))
    db.commit()



async def edit_notes(user_id ,notes_id: int, name: str) -> None:
    table_name = "user_" + str(user_id)

    cur.execute(f"UPDATE {table_name} SET name = ? WHERE notes_id = ?", (name, notes_id,))
    db.commit()

