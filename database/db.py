import sqlite3
from sqlite3 import InternalError

async def create_table():
    global conn, cur
    conn = sqlite3.connect('users.sqlite')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (CHAT_ID BIGINTEGER PRIMARY KEY, user_name TEXT)""")
    conn.commit()
    try:
    	cur.execute("INSERT INTO admins VALUES (?,?)", (1030563973, "Arseniy",))
    	conn.commit()
    except Exception:
    	pass
    cur.execute("""CREATE TABLE IF NOT EXISTS admins (CHAT_ID BIGINTEGER PRIMARY KEY, name_and_surname TEXT)""")
    conn.commit()
    cur.execute("""CREATE TABLE IF NOT EXISTS orders (title TEXT PRIMARY KEY, text TEXT, price TEXT, photo_id TEXT)""")
    conn.commit()

async def add_user(chat_id, username):
    try:
        cur.execute("INSERT INTO users VALUES (?,?)", (chat_id, username,))
        conn.commit()
    except Exception:
        pass

async def add_order(title, text, price, photo):
    try:
        cur.execute("INSERT INTO orders VALUES (?,?,?,?)", (title, text, price, photo))
        conn.commit()
    except Exception:
        pass

async def add_admin(chat_id, name_and_surname):
    cur.execute("INSERT INTO admins VALUES (?,?)", (chat_id, name_and_surname))
    conn.commit()

async def get_admins():
    global admin_list
    admin_list = []
    cur.execute("""SELECT CHAT_ID FROM admins""")
    records = cur.fetchall()
    for i in range(len(records)):
        admin_list.append(records[i][0])
    print(admin_list)
    return admin_list

async def get_admins_names():
    global admin_list
    admin_list = []
    cur.execute("""SELECT name_and_surname FROM admins""")
    records = cur.fetchall()
    for i in range(len(records)):
        admin_list.append(records[i][0])
    print(admin_list)
    return admin_list


async def get_users():
    global user_list
    user_list = []
    cur.execute("""SELECT CHAT_ID FROM users""")
    records = cur.fetchall()
    for i in range(len(records)):
        user_list.append(records[i][0])
    return user_list

async def get_orders():
    global order_list
    order_list = []
    cur.execute("""SELECT * FROM orders""")
    records = cur.fetchall()
    for i in range(len(records)):
        order_list.append(records[i])
    return order_list

async def delete_order(title):
    cur.execute("""DELETE FROM orders WHERE title = (?)""", (title,))
    conn.commit()
    return "Sucsessful"

async def delete_admin(name_and_surname):
    cur.execute("""DELETE FROM admins WHERE name_and_surname = (?)""", (name_and_surname,))
    conn.commit()
    return "Sucsessful"


    
