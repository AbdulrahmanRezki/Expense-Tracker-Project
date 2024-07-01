import PySimpleGUI as GUI  # Importing the PySimpleGUI library for GUI handling
import os.path  # Importing the os.path library for file path handling
import sqlite3  # Importing the sqlite3 library for database handling
import hashlib  # Importing the hashlib library for password hashing

def hash_password(password):
    # Function to hash a password using SHA-256
    return hashlib.sha256(password.encode()).hexdigest()

def check_table_exists(conn, table_name):
    # Function to check if a specific table exists in the database
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cur.fetchone()
    return result is not None

def Register():
    loginLayout = [
        [GUI.Text("Enter your username & password:")],
        [GUI.Text('Username: '), GUI.Input(key='username')],
        [GUI.Text('Password: '), GUI.Input(key='password', password_char='*')],
        [GUI.Button("Register"), GUI.Button("Cancel")]
    ]

    while True:
        window2 = GUI.Window("Register Portal", loginLayout)
        event2, values = window2.read()
        window2.close()  # Ensure window is closed

        if event2 == "Cancel" or event2 == GUI.WIN_CLOSED:
            break

        elif event2 == "Register":
            username = values['username'].strip()
            password = values['password'].strip()
            hashed_password = hash_password(password)

            conn = sqlite3.connect('loginList.db')
            table_exists = check_table_exists(conn, 'List')

            if not table_exists:
                conn.execute("CREATE TABLE List (username TEXT, password TEXT)")

            conn.execute("INSERT INTO List (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()

            GUI.popup("Registered successfully!")
            break
