import PySimpleGUI as GUI 
import os.path
import sqlite3 

def check_table_exists(conn, table_name):
    
    
    cur = conn.cursor()
    # Query the sqlite_master table to check for the existence of the table
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cur.fetchone()
    # Return True if the table exists, False otherwise
    return result is not None

#Main
def Register():
    # Define the layout for the login window
    loginLayout = [
        [GUI.Text("Enter your username & password:")],
        [GUI.Text('Username: '), GUI.Input(key='username')],
        [GUI.Text('Password: '), GUI.Input(key='password')],
        [GUI.Button("Register"), GUI.Button("Cancel")]
    ]

    while True:
        # Display the login window and wait for user interaction
        window2 = GUI.Window("Register Portal", loginLayout)
        event2, values = window2.read()

        if event2 == "Cancel":
            # Close the window and break out of the loop if Cancel button is clicked
            window2.close()  # Closing the window for a better user experience
            break 

        elif event2 == "Register":
            username = values['username']
            password = values['password']
            conn = sqlite3.connect('loginList.db') 
            table_exists = check_table_exists(conn, 'List')
            
            if os.path.isfile('loginList.db') and table_exists:
                conn.execute("INSERT INTO List (username, password) VALUES (?, ?)", (username, password+ '\n'))   # Use parameterized queries to prevent SQL injection attacks
                conn.commit()
                conn.close()
                window2.close()
            
            else:
                conn = sqlite3.connect('loginList.db') 
                conn.execute("CREATE TABLE List (username TEXT, password TEXT)")
                conn.execute("INSERT INTO List (username, password) VALUES (?, ?)", (username, password+'\n'))   # Use parameterized queries to prevent SQL injection attacks
                conn.commit()
                conn.close()
                window2.close()

            # Display a success message after logging in
            RegSuccessfully = [
                [GUI.Text("Registered successfully!")],
            ]
            
            while True:
                # Display the success message window
                windowSuc = GUI.Window("Register DONE: ", RegSuccessfully)
                eventSuc, values = windowSuc.read()
                break  # Exit the inner loop after showing the success message window
            break  # Exit the outer loop after successful login


# Known Issues:

# 1. Proper Window Closing:
# The main registration window (`window2`) does not handle the window close event (`GUI.WIN_CLOSED`).


# 2. Repetitive Opening of SQLite Connection:
# The SQLite connection is opened multiple times within the else block.


# 3. Success Message Window Closing:
# The success message window (`windowSuc`) does not handle the window close event (`GUI.WIN_CLOSED`).


# 4. Using Context Manager for SQLite Connection:
# Not using a context manager for the SQLite connection can lead to database locks and issues with proper closure.


# 5. Inconsistent Closing Logic:
# Multiple `window2.close()` calls in both if and else blocks can be redundant and lead to inconsistent behavior.






