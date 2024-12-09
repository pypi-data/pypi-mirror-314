# test_sql_safe.py

import sqlite3

def get_user_info(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?;"
    cursor.execute(query, (username,))
    result = cursor.fetchall()
    conn.close()
    return result

user_input = input("Ingrese el nombre de usuario: ")
user_info = get_user_info(user_input)
print(user_info)
