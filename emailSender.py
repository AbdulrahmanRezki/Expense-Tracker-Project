import yagmail #using this library since it gets the task done with the least amout of code
import PySimpleGUI as GUI


def EmailSender(content):
    '''
    usage of popups instead of layout method in PySimpleGUI to avoid excess code
    '''
    if GUI.popup_yes_no('Do you want to recieve the results via email? ') == 'No':
        exit()
    else:
        emailAddress = GUI.popup_get_text("Enter your email address:")
        if GUI.popup_ok_cancel()=="Cancel":
            exit()
        else:
        
            yag = yagmail.SMTP('bankstatment14@gmail.com', 'ytdw ctkl hths wpqe')

            yag.send(emailAddress, 'subject', content)
            
        
        #orginal code:somethingSomething123