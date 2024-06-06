import PySimpleGUI as GUI
import os.path
import sqlite3
import hashlib

def hash_password(password):
    # Simple hashing function for demonstration purposes
    return hashlib.sha256(password.encode()).hexdigest()

def check_table_exists(conn, table_name):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cur.fetchone()
    return result is not None

def Register():
    # Define the layout for the registration window
    loginLayout = [
        [GUI.Text("Enter your username & password:")],
        [GUI.Text('Username: '), GUI.Input(key='username')],
        [GUI.Text('Password: '), GUI.Input(key='password', password_char='*')],
        [GUI.Button("Register"), GUI.Button("Cancel")]
    ]

    while True:
        # Display the registration window and wait for user interaction
        window2 = GUI.Window("Register Portal", loginLayout)
        event2, values = window2.read()
        window2.close()

        if event2 == "Cancel" or event2 == GUI.WIN_CLOSED:
            break

        elif event2 == "Register":
            username = values['username'].strip()
            password = values['password'].strip()
            hashed_password = hash_password(password)

            print(f"Debug: Input username: {username}")
            print(f"Debug: Input hashed password: {hashed_password}")

            conn = sqlite3.connect('loginList.db')
            table_exists = check_table_exists(conn, 'List')

            if not table_exists:
                conn.execute("CREATE TABLE List (username TEXT, password TEXT)")

            conn.execute("INSERT INTO List (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()

            # Display a success message after registration
            RegSuccessfully = [
                [GUI.Text("Registered successfully!")],
                [GUI.Button("OK")]
            ]
            windowSuc = GUI.Window("Register DONE: ", RegSuccessfully)
            windowSuc.read()
            windowSuc.close()
            break
