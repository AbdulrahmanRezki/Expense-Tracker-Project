import PySimpleGUI as GUI  # This library is chosen for its minimal GUI handling requirements.
import Register
import Login

# Layout for the initial authentication window
layout = [
    [GUI.Text("Login/Register")],
    [GUI.Button("Login")],
    [GUI.Button("Register")],
    [GUI.Button("Cancel")]
]

while True:
    # Display the authentication window and wait for user interaction
    window = GUI.Window("Portal: ", layout)
    event, values = window.read()
    window.close()

    if event == "Login":
        # Initiate the login process
        Login.login()
        break

    elif event == "Register":
        # Initiate the user registration process
        Register.Register()
        break

    elif event == "Cancel" or event == GUI.WIN_CLOSED:
        break

print("Program Terminated")














#    - Store the username and a securely hashed password in the database



# 2. Implement a login system:
#    - Prompt users to enter their username and password
#    - Verify credentials against stored information
#    - Grant access upon successful authentication

# Expense Recording:
# 3. Create a form/interface for users to add expenses
#    - Allow users to input expense details (category, amount, date, description)
#    - Store this information in the database associated with the logged-in user
# 4. Enable categorization of expenses:
#    - Implement functionality to group expenses by different categories (groceries, bills, entertainment, etc.)

# Budget Management:
# 5. Provide a feature for users to set budgets for different expense categories
#    - Allow users to input budget amounts for each category
# 6. Track spending against set budgets:
#    - Compare actual spending against allocated budgets for insights

# Data Visualization:
# 7. Create visual representations of expense data:
#    - Generate charts (bar charts, pie charts) to visualize spending patterns over time or across categories using a library like matplotlib

# Reports and Insights:
# 8. Generate summary reports:
#    - Calculate total expenses, category-wise spending, percentage of budget utilized, etc.

# Reminder and Notifications:
# 9. Implement reminders for upcoming bills or financial goals:
#    - Allow users to set reminders based on dates or specific events

# Data Persistence:
# 10. Ensure secure storage of user expense data:
#     - Implement methods to securely store and retrieve expense data associated with each user

# Export and Import:
# 11. Enable users to export/import expense data:
#     - Provide functionality to export data to formats like CSV or PDF for record-keeping
#     - Allow users to import previously exported data back into the system

# Main Program Flow:
# 12. Begin the main program flow:
#     - Display a login/registration interface to users
#     - Based on user choice (login/register), execute the respective functions
#     - Upon successful login, present a menu/interface for users to access different features (add expenses, view reports, set budgets, etc.)
#     - Handle user interactions based on selected options, calling corresponding functions to perform the desired tasks
# 13. Continuously loop through the program until the user chooses to exit or log out




print("Program Terminated")