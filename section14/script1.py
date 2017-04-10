import sqlite3

def create_table():
    conn=sqlite3.connect("lite.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS store (item TEXT, quantity INTEGER, price REAL)")
    cur.execute("INSERT INTO store VALUES('Wine Glass',8,10.99)")
    conn.commit()
    conn.close()

def insert(item, quantity, price):
    conn=sqlite3.connect("lite.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO store VALUES(?,?,?)",(item,quantity,price))
    conn.commit()
    conn.close()


insert("Coffee Cup",10, 1.99)

def view():
    conn=sqlite3.connect("lite.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM store")
    rows=cur.fetchall()
    conn.close()
    return rows

print(view())
