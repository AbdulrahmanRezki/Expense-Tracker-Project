import pandas as pd
import PySimpleGUI as GUI
from PyPDF2 import PdfReader, PdfWriter

# Function to create a new PDF by copying pages from the original
def create_decrypted_pdf():
    writer = PdfWriter()
    
    # Add all pages from the reader to the writer
    for page in pdf_reader.pages:
        writer.add_page(page)
    
    # Save the new PDF to a file
    with open("decrypted-pdf.pdf", "wb") as f:
        writer.write(f)

# Get the file path from the user
file_path = GUI.popup_get_file('Please enter a filename')

while True:
    if not file_path:
        if GUI.popup_yes_no('No file selected, do you want to try again?') == 'Yes':
            file_path = GUI.popup_get_file('Please enter a filename')
            continue
        else:
            quit()
    else:
        break

# Create a PdfReader object
pdf_reader = PdfReader(file_path)

# Check if the PDF is encrypted
if pdf_reader.is_encrypted:
    # Loop to prompt the user for the correct password until provided or the user decides to quit
    while True:
        # Prompt the user to enter the password
        password = GUI.popup_get_text('Please enter your password:')
        
        try:
            # Attempt to decrypt the PDF with the provided password
            pdf_reader.decrypt(password)
            # Create the decrypted PDF
            create_decrypted_pdf()
            break
        
        except Exception as e:
            # If decryption fails, ask the user if they want to try again
            if GUI.popup_yes_no('Wrong password, do you want to try again?') == 'Yes':
                continue
            else:
                quit()
else:
    # If the PDF is not encrypted, create the decrypted PDF directly
    create_decrypted_pdf()

print("Done")
