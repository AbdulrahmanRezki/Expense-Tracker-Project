import PySimpleGUI as GUI
import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def print_database_contents(conn):
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
        windowLogin.close()

        if event == "Cancel" or event == GUI.WIN_CLOSED:
            break

        elif event == "Login":
            username = values['username'].strip()
            password = values['password'].strip()
            hashed_password = hash_password(password)

            print(f"Debug: Input username: {username}")
            print(f"Debug: Input hashed password: {hashed_password}")

            conn = sqlite3.connect("loginList.db")
            print_database_contents(conn)
            cur = conn.cursor()

            cur.execute("SELECT username, password FROM List WHERE username = ?", (username,))
            user = cur.fetchone()

            if user:
                stored_username, stored_password = user
                print(f"Debug: Stored username: {stored_username}")
                print(f"Debug: Stored hashed password: {stored_password}")

                if stored_password == hashed_password:
                    print("Login successful")
                    break
                else:
                    print("Debug: Password does not match")
                    layoutInvalid = [[GUI.Text("Invalid Logins.")], [GUI.Button("OK")]]
                    window3 = GUI.Window("Failure Login", layoutInvalid)
                    window3.read()
                    window3.close()
                    break
                
            else:
                print("Debug: Username not found")
                layoutInvalid = [[GUI.Text("Invalid Logins.")], [GUI.Button("OK")]]
                window3 = GUI.Window("Failure Login", layoutInvalid)
                window3.read()
                window3.close()
                break
