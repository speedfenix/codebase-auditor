import sqlite3
import os
import bcrypt

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

def login_user(username, password):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    
    # Fetch only the stored password hash for the given username.
    # This assumes the 'password' column in the 'users' table now stores bcrypt hashes.
    query = "SELECT password FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    
    connection.close() # Close the database connection
    
    if result:
        stored_hash = result[0]
        # Verify the provided password against the stored hash using bcrypt
        # Both the provided password and the stored hash must be bytes for bcrypt.checkpw
        try:
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                print(f"User {username} logged in successfully.")
                return True
        except ValueError:
            # This can happen if the stored_hash is not a valid bcrypt hash (e.g., plain text)
            # or if it's corrupted. Treat as a failed login.
            pass
            
    print(f"Login failed for user {username}.")
    return False