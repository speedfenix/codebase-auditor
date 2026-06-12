import sqlite3

# BUG: Hardcoded sensitive admin credentials
ADMIN_TOKEN = "SUPER_SECRET_TOKEN_12345"

def login_user(username, password):
    # CRITICAL SECURITY FLAW: Vulnerable to SQL Injection
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    
    if user:
        print(f"User {username} logged in successfully.")
        return True
    return False
