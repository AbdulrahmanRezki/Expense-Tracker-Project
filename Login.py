import PySimpleGUI as GUI 
import sqlite3


def login():
    
    #Desgin page:
    loginLayout = [
        [GUI.Text("Enter your username & password:")],
        [GUI.Text('Username: '), GUI.Input(key='username')],
        [GUI.Text('Password: '), GUI.Input(key='password')],
        [GUI.Button("Login"), GUI.Button("Cancel")]
    ]


    while True:
        # Display the login window and wait for user interaction
        window2 = GUI.Window("Login Portal", loginLayout)
        event2, values = window2.read()
        
        
        if event2 == "Cancel":
            # Close the window and break out of the loop if Cancel button is clicked
            window2.close()  # Closing the window for a better user experience
            break 
        
        elif event2 == "Login":
            
            #connect to database
            #con = sqlite3.connect("loginList.db")
    
            #Check if credientals are in database
            with open("loginList.db", "r") as f:
                for row in f:
                    for col in row:
                        print(col)
                break   
            
    #if username & password in database
    #go into the next page (undecided yet)
    
    #else, print unable to sign in and loop again.
    pass