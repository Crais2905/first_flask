import sqlite3
from flask import abort 

class SQLite:
    def __init__(self, name) -> None:
        with sqlite3.connect('clubs.db') as sqlite_connection:
            cursor = sqlite_connection.cursor()


    def user_len(self):
        with sqlite3.connect('clubs.db') as sqlite_connection:
            cursor = sqlite_connection.cursor()

            cursor.execute(''' SELECT count() FROM users ''')
            length = cursor.fetchall()[0][0]
            # print(length)
            return length 


    def write_user(self, name, password, email):
        try:
            values = (self.user_len()+1, name, password, email)
            with sqlite3.connect('clubs.db') as sqlite_connection:
                cursor = sqlite_connection.cursor()

                cursor.execute(''' INSERT INTO users VALUES(?, ?, ?, ?) ''', values)
        except:
            return abort(404)
        
    def valid_username(self, new_name):
        try:
            with sqlite3.connect('clubs.db') as sqlite_connection:
                cursor = sqlite_connection.cursor()

                cursor.execute(''' SELECT user_name FROM users ''')
                names = cursor.fetchall()
                return not new_name in names
        except:
            return False

bd = SQLite('clubs.db')
bd.valid_username('crais')