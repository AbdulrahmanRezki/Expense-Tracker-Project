import PySimpleGUI as GUI  # This library is chosen for its minimal GUI handling requirements.
import Register  # Importing the Register module
import Login  # Importing the Login module

# Layout for the initial authentication window
layout = [
    [GUI.Text("Login/Register")],  # Displaying the title text
    [GUI.Button("Login")],  # Button for initiating the login process
    [GUI.Button("Register")],  # Button for initiating the registration process
    [GUI.Button("Cancel")]  # Button for cancelling the operation and exiting
]

while True:
    # Create and display the authentication window
    window = GUI.Window("Portal: ", layout)
    # Wait for user interaction and read the event and values
    event, values = window.read()
    # Close the window after reading the event
    window.close()

    if event == "Login":
        # If the "Login" button is clicked, initiate the login process
        Login.login()
        break  # Exit the loop after handling the event


    elif event == "Register":
        # If the "Register" button is clicked, initiate the user registration process
        Register.Register()
        break  # Exit the loop after handling the event

    elif event == "Cancel" or event == GUI.WIN_CLOSED:
        # If the "Cancel" button is clicked or the window is closed, exit the loop
        break


print("Program Terminated")
