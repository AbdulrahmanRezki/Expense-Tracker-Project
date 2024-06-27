import pdfplumber
import PySimpleGUI as GUI
from PyPDF2 import PdfReader, PdfWriter
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

def create_decrypted_pdf(pdf_reader):
    """
    Create a decrypted copy of the PDF and extract tables from it.
    """
    writer = PdfWriter()

    # Add all pages from the reader to the writer
    for page in pdf_reader.pages:
        writer.add_page(page)

    # Save the new PDF to a file
    with open("decrypted-pdf.pdf", "wb") as f:
        writer.write(f)

    # Read table data from the new PDF
    try:
        extract_table_data("decrypted-pdf.pdf")
    except Exception as e:
        print(f"Error reading table data: {e}")

def extract_table_data(file):
    """
    Extract tables from the PDF, clean the data, and save it to a database.
    """
    with pdfplumber.open(file) as pdf:
        all_tables = []
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                # Convert the table into a DataFrame
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

    if not all_tables:
        raise ValueError("No tables found in PDF")

    # Clean each table and combine them into a single DataFrame
    cleaned_dfs = [clean_data(df) for df in all_tables if not df.empty]
    if not cleaned_dfs:
        raise ValueError("No non-empty tables found to process")
    
    combined_df = pd.concat(cleaned_dfs, ignore_index=True)
    print(combined_df)

    # Extract 'Date' and 'Balance' columns, ensuring they match in order
    if {'Date', 'Balance'}.issubset(combined_df.columns):
        filtered_df = combined_df.dropna(subset=['Date', 'Balance'])
        date_list = filtered_df['Date'].tolist()
        balance_list = filtered_df['Balance'].tolist()
        print("Date List:", date_list)
        print("Balance List:", balance_list)

        # Plotting the data
        fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
        categories = date_list

        ax.bar(categories, balance_list)
        plt.title('Bank Balance Over Time')
        plt.grid()
        plt.show()
    else:
        print("Date or Balance column not found in the DataFrame")
        return [], []

    # Save cleaned data to SQLite database
    save_to_database(combined_df)

def clean_data(df):
    """
    Clean the data by handling missing values and renaming columns.
    """
    # Drop columns and rows where all values are NaN
    df = df.dropna(axis=1, how='all').dropna(how='all')

    if df.shape[1] == 0:
        raise ValueError("No columns left after dropping empty columns")

    # Forward fill to handle missing data
    df = df.ffill()
    num_columns = df.shape[1]
    
    # Rename columns based on expected format
    if num_columns >= 5:
        df.columns = ['Date', 'Description', 'Debit', 'Credit', 'Balance'] + [f'Extra_{i}' for i in range(num_columns - 5)]
    else:
        raise ValueError(f"Unexpected number of columns: {num_columns}")

    # Drop rows where 'Date' is NaN and reset index
    df = df.dropna(subset=['Date'])
    df.reset_index(drop=True, inplace=True)

    return df

def save_to_database(df):
    """
    Save the cleaned data to an SQLite database.
    """
    con = sqlite3.connect("table.db")
    cur = con.cursor()
    
    # Create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            Date TEXT,
            Description TEXT,
            Debit REAL,
            Credit REAL,
            Balance REAL
        )
    """)

    # Insert DataFrame rows into the database
    for _, row in df.iterrows():
        cur.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?)", row[:5])
    
    con.commit()
    con.close()

def assas():
    # Get the file path from the user
    file_path = GUI.popup_get_file('Please enter a filename')

    # Loop until a valid file path is provided or the user chooses to quit
    while not file_path:
        if GUI.popup_yes_no('No file selected, do you want to try again?') == 'Yes':
            file_path = GUI.popup_get_file('Please enter a filename')
        else:
            quit()

    # Create a PdfReader object
    pdf_reader = PdfReader(file_path)

    # Check if the PDF is encrypted
    if pdf_reader.is_encrypted:
        while True:
            password = GUI.popup_get_text('Please enter your password:')
            try:
                # Attempt to decrypt the PDF with the provided password
                pdf_reader.decrypt(password)
                create_decrypted_pdf(pdf_reader)
                break
            except Exception as e:
                # If decryption fails, ask the user if they want to try again
                if GUI.popup_yes_no('Wrong password, do you want to try again?') != 'Yes':
                    quit()
    else:
        create_decrypted_pdf(pdf_reader)

    print("Done")
