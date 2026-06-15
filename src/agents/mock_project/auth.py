import sqlite3

ADMIN_TOKEN = "SUPER_SECRET_TOKEN_12345"

def login_user(username, password):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    
    if user:
        print(f"User {username} logged in successfully.")
        return True
    return False
