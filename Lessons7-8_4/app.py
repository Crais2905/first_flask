import sqlite3

with sqlite3.connect('test_db.db') as sqlite_connection:
    cursor = sqlite_connection.cursor()
    # cursor.execute('''CREATE TABLE Students (
    #     id INTEGER PRIMERY KEY,
    #     name TEXT,
    #     class INTEGER,
    #     city TEXT
    # )''')

    # cursor.execute(''' CREATE TABLE orders(
    #     id INTEGER PRIMARY KEY,
    #     title TEXT NOT NULL,
    #     decription TEXT NOT NULL,
    #     user_id INTEGER
    # )''')


    # cursor.execute('''INSERT INTO orders VALUES(1, 'phone', 'phone decription', 5) ''')
    # cursor.execute('''INSERT INTO orders VALUES(2, 'mouse', 'mouse decription', 2) ''')
    # cursor.execute('''INSERT INTO orders VALUES(3, 'keyboard', 'keyboard decription', 2) ''')
    # cursor.execute('''INSERT INTO orders VALUES(4, 'phone', 'phone decription', 8) ''')
    # cursor.execute('''INSERT INTO orders VALUES(5, 'monitor', 'monitor decription', 4) ''')


    cursor.execute(''' SELECT Students.id, Students.name, title, decription
        FROM orders 
        JOIN Students ON orders.user_id = Students.id  
    ''')



    print(cursor.fetchall())

    



    
    