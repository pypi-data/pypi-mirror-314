# test_sql_injection.py

import sqlite3

def get_user_info(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "';"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

user_input = input("Ingrese el nombre de usuario: ")
user_info = get_user_info(user_input)
print(user_info)
