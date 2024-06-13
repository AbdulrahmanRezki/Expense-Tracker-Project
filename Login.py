import PySimpleGUI as GUI  # Importing the PySimpleGUI library for GUI handling
import sqlite3  # Importing the sqlite3 library for database handling
import hashlib  # Importing the hashlib library for password hashing

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
    # Layout for the login window
    layout = [
        [GUI.Text("Enter your username & password:")],  # Prompt for username and password
        [GUI.Text('Username: '), GUI.Input(key='username')],  # Input field for username
        [GUI.Text('Password: '), GUI.Input(key='password', password_char='*')],  # Input field for password
        [GUI.Button("Login"), GUI.Button("Cancel")]  # Buttons for login and cancel actions
    ]

    while True:
        # Create and display the login window
        windowLogin = GUI.Window("Login Portal", layout)
        # Wait for user interaction and read the event and values
        event, values = windowLogin.read()
        # Close the window after reading the event
        windowLogin.close()

        if event == "Cancel" or event == GUI.WIN_CLOSED:
            # If the "Cancel" button is clicked or the window is closed, exit the loop
            break

        elif event == "Login":
            # If the "Login" button is clicked, process the login
            username = values['username'].strip()  # Get the entered username and strip any whitespace
            password = values['password'].strip()  # Get the entered password and strip any whitespace
            hashed_password = hash_password(password)  # Hash the entered password

            print(f"Debug: Input username: {username}")  # Debug: print the entered username
            print(f"Debug: Input hashed password: {hashed_password}")  # Debug: print the hashed password

            conn = sqlite3.connect("loginList.db")  # Connect to the SQLite database
            print_database_contents(conn)  # Print the current database contents for debugging
            cur = conn.cursor()

            # Query the database for the entered username
            cur.execute("SELECT username, password FROM List WHERE username = ?", (username,))
            user = cur.fetchone()

            if user:
                # If the user exists, retrieve the stored username and password
                stored_username, stored_password = user
                print(f"Debug: Stored username: {stored_username}")  # Debug: print the stored username
                print(f"Debug: Stored hashed password: {stored_password}")  # Debug: print the stored hashed password

                if stored_password == hashed_password:
                    # If the stored password matches the entered hashed password, login is successful
                    print("Login successful")
                    break
                else:
                    # If the passwords do not match, display an invalid login message
                    print("Debug: Password does not match")
                    layoutInvalid = [[GUI.Text("Invalid Logins.")], [GUI.Button("OK")]]
                    window3 = GUI.Window("Failure Login", layoutInvalid)
                    window3.read()
                    window3.close()
                    break
                
            else:
                # If the username is not found, display an invalid login message
                print("Debug: Username not found")
                layoutInvalid = [[GUI.Text("Invalid Logins.")], [GUI.Button("OK")]]
                window3 = GUI.Window("Failure Login", layoutInvalid)
                window3.read()
                window3.close()
                break
