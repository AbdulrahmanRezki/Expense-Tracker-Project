import PySimpleGUI as GUI  # Importing the PySimpleGUI library for GUI handling
import sqlite3  # Importing the sqlite3 library for database handling
import hashlib  # Importing the hashlib library for password hashing
from bankStatmentUI import assas #if succefully logged in it will display this module

def hash_password(password):
    # Function to hash a password using SHA-256
    return hashlib.sha256(password.encode()).hexdigest()

def print_database_contents(conn):
    # Function to print the current contents of the database for debugging purposes
    cur = conn.cursor()
    cur.execute("SELECT username, password FROM List")
    rows = cur.fetchall()
    print("Debug: Current database contents:")
    for row in rows:
        print(row)

def login():
    layout = [
        [GUI.Text("Enter your username & password:")],
        [GUI.Text('Username: '), GUI.Input(key='username')],
        [GUI.Text('Password: '), GUI.Input(key='password', password_char='*')],
        [GUI.Button("Login"), GUI.Button("Cancel")]
    ]

    while True:
        windowLogin = GUI.Window("Login Portal", layout)
        event, values = windowLogin.read()
        windowLogin.close()  # Ensure window is closed

        if event == "Cancel" or event == GUI.WIN_CLOSED:
            break

        elif event == "Login":
            username = values['username'].strip()
            password = values['password'].strip()
            hashed_password = hash_password(password)

            conn = sqlite3.connect("loginList.db")
            print_database_contents(conn)
            cur = conn.cursor()

            cur.execute("SELECT username, password FROM List WHERE username = ?", (username,))
            user = cur.fetchone()

            if user:
                stored_username, stored_password = user
                if stored_password == hashed_password:
                    assas()  # Call assas function if login is successful
                    break
                else:
                    GUI.popup("Invalid Logins.")  # Use GUI popup instead of creating a new window
            else:
                GUI.popup("Invalid Logins.")  # Use GUI popup instead of creating a new window
