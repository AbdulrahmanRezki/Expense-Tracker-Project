import pdfplumber
import PySimpleGUI as GUI
from PyPDF2 import PdfReader, PdfWriter
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import smtplib
import faulthandler
import logging
import matplotlib as mpl

mpl.use('tkagg')# used to display the plot in a Tkinter window. To avoid segmentation fault when plt.show() in Mac command line

faulthandler.enable()

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename='debug.log', filemode='w', format='%(asctime)s - %(message)s')

def emailSender(var):
    logging.debug('Entering emailSender function')
    response = GUI.popup_yes_no('Do you want to enter your email?')
    if response == 'No':
        logging.debug('User chose not to enter an email')
        return  # Avoid calling exit() here
    logging.debug('Email address prompt displayed')


def create_decrypted_pdf(pdf_reader):
    logging.debug('Entering create_decrypted_pdf function')
    writer = PdfWriter()
    for page in pdf_reader.pages:
        writer.add_page(page)
    with open("decrypted-pdf.pdf", "wb") as f:
        writer.write(f)
    try:
        extract_table_data("decrypted-pdf.pdf")
    except Exception as e:
        logging.error(f"Error reading table data: {e}")

def extract_table_data(file):
    logging.debug('Entering extract_table_data function')
    with pdfplumber.open(file) as pdf:
        all_tables = []
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)
    if not all_tables:
        raise ValueError("No tables found in PDF")

    cleaned_dfs = [clean_data(df) for df in all_tables if not df.empty]
    if not cleaned_dfs:
        raise ValueError("No non-empty tables found to process")
    
    combined_df = pd.concat(cleaned_dfs, ignore_index=True)
    logging.debug('Combined DataFrame created')

    if {'Date', 'Balance'}.issubset(combined_df.columns):
        filtered_df = combined_df.dropna(subset=['Date', 'Balance'])
        date_list = filtered_df['Date'].tolist()
        balance_list = filtered_df['Balance'].tolist()
        logging.debug(f"Date List: {date_list}")
        logging.debug(f"Balance List: {balance_list}")

        fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
        categories = date_list
        ax.bar(categories, balance_list)
        plt.title('Bank Balance Over Time')
        plt.grid()
        plt.show()

        emailSender("output.jpg")
    else:
        logging.warning("Date or Balance column not found in the DataFrame")
        return [], []

    save_to_database(combined_df)

def clean_data(df):
    logging.debug('Entering clean_data function')
    df = df.dropna(axis=1, how='all').dropna(how='all')
    if df.shape[1] == 0:
        raise ValueError("No columns left after dropping empty columns")

    df = df.ffill()
    num_columns = df.shape[1]
    
    if num_columns >= 5:
        df.columns = ['Date', 'Description', 'Debit', 'Credit', 'Balance'] + [f'Extra_{i}' for i in range(num_columns - 5)]
    else:
        raise ValueError(f"Unexpected number of columns: {num_columns}")

    df = df.dropna(subset=['Date'])
    df.reset_index(drop=True, inplace=True)

    return df

def save_to_database(df):
    logging.debug('Entering save_to_database function')
    con = sqlite3.connect("table.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            Date TEXT,
            Description TEXT,
            Debit REAL,
            Credit REAL,
            Balance REAL
        )
    """)
    for _, row in df.iterrows():
        cur.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?)", row[:5])
    con.commit()
    con.close()


def assas():
    logging.debug('Entering assas function')
    file_path = GUI.popup_get_file('Please enter a filename')
    while not file_path:
        if GUI.popup_yes_no('No file selected, do you want to try again?') == 'Yes':
            file_path = GUI.popup_get_file('Please enter a filename')
        else:
            logging.debug('User chose not to select a file')
            return  # Avoid calling quit()

    pdf_reader = PdfReader(file_path)
    if pdf_reader.is_encrypted:
        while True:
            password = GUI.popup_get_text('Please enter your password:')
            try:
                pdf_reader.decrypt(password)
                create_decrypted_pdf(pdf_reader)
                break
            except Exception as e:
                logging.error(f"Error decrypting PDF: {e}")
                if GUI.popup_yes_no('Wrong password, do you want to try again?') != 'Yes':
                    return  # Avoid calling quit()
    else:
        create_decrypted_pdf(pdf_reader)

    logging.debug("Process completed successfully")

