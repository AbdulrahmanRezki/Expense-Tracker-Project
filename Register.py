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
    # Define the layout for the registration window
    loginLayout = [
        [GUI.Text("Enter your username & password:")],  # Prompt for username and password
        [GUI.Text('Username: '), GUI.Input(key='username')],  # Input field for username
        [GUI.Text('Password: '), GUI.Input(key='password', password_char='*')],  # Input field for password
        [GUI.Button("Register"), GUI.Button("Cancel")]  # Buttons for register and cancel actions
    ]

    while True:
        # Create and display the registration window
        window2 = GUI.Window("Register Portal", loginLayout)
        # Wait for user interaction and read the event and values
        event2, values = window2.read()
        # Close the window after reading the event
        window2.close()

        if event2 == "Cancel" or event2 == GUI.WIN_CLOSED:
            # If the "Cancel" button is clicked or the window is closed, exit the loop
            break

        elif event2 == "Register":
            # If the "Register" button is clicked, process the registration
            username = values['username'].strip()  # Get the entered username and strip any whitespace
            password = values['password'].strip()  # Get the entered password and strip any whitespace
            hashed_password = hash_password(password)  # Hash the entered password

            print(f"Debug: Input username: {username}")  # Debug: print the entered username
            print(f"Debug: Input hashed password: {hashed_password}")  # Debug: print the hashed password

            conn = sqlite3.connect('loginList.db')  # Connect to the SQLite database
            table_exists = check_table_exists(conn, 'List')  # Check if the table 'List' exists

            if not table_exists:
                # If the table does not exist, create it
                conn.execute("CREATE TABLE List (username TEXT, password TEXT)")

            # Insert the new username and hashed password into the 'List' table
            conn.execute("INSERT INTO List (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()  # Commit the transaction
            conn.close()  # Close the database connection

            # Display a success message after registration
            RegSuccessfully = [
                [GUI.Text("Registered successfully!")],
                [GUI.Button("OK")]
            ]
            windowSuc = GUI.Window("Register DONE: ", RegSuccessfully)
            windowSuc.read()  # Wait for user interaction
            windowSuc.close()  # Close the success message window
            break  # Exit the loop
