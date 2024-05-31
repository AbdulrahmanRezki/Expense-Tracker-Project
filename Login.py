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





    layoutInvalid = [[GUI.Text("Invalid Logins.")]]
    window3 = GUI.Window("Faliure Login", layoutInvalid)
    
    

    
    
    

    while True:
        # Display the login window and wait for user interaction
        window2 = GUI.Window("Login Portal", loginLayout)
        event2, values = window2.read()
        
        
        if event2 == "Cancel":
            # Close the window and break out of the loop if Cancel button is clicked
            window2.close()  # Closing the window for a better user experience
            break 
        
        elif event2 == "Login":
            
            username = values['username']
            password = values['password'] 
            
            con = sqlite3.connect("loginList.db")
            cur = con.cursor()
    
            #Check if credientals are in database
            try:
                for row in cur.execute(f"SELECT {username} , {password} "):
                    print(row)
                    
                window2.close()
                break
        
            
            except:
                
                
                
                
                
                print("error occured here")
                event3, values3 = window3.read()
                
                if event3 == GUI.WIN_CLOSED or event3 == 'Cancel':
                    break
    #if username & password in database
    #go into the next page (undecided yet)
    
    #else, print unable to sign in and loop again.
