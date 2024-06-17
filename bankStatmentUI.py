import pdfplumber
import PySimpleGUI as GUI
from PyPDF2 import PdfReader, PdfWriter
import pandas as pd
import sqlite3


# Function to create a new PDF by copying pages from the original
def create_decrypted_pdf():
    writer = PdfWriter()

    # Add all pages from the reader to the writer
    for page in pdf_reader.pages:
        writer.add_page(page)

    # Save the new PDF to a file
    with open("decrypted-pdf.pdf", "wb") as f:
        writer.write(f)

    # Read table data from the new PDF
    try:
        Table("decrypted-pdf.pdf")
    except Exception as e:
        print(f"Error reading table data: {e}")


def Table(file):
    # Read data stored as a csv file into a pandas DataFrame
    with pdfplumber.open(file) as pdf:
        all_tables = []
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

    if not all_tables:
        raise ValueError("No tables found in PDF")

    # Clean and combine DataFrames
    cleaned_dfs = []
    for df in all_tables:
        if df.empty:
            print("Empty DataFrame found, skipping...")
            continue
        cleaned_df = clean_data(df)
        cleaned_dfs.append(cleaned_df)
    if not cleaned_dfs:
        raise ValueError("No non-empty tables found to process")
    combined_df = pd.concat(cleaned_dfs, ignore_index=True)

    # Display the cleaned DataFrame (for debug purposes)
    print(combined_df)

    # Save cleaned data to SQLite database
    save_to_database(combined_df)


def clean_data(df):
    # Step 1: Drop columns that are completely empty
    df = df.dropna(axis=1, how='all')

    # Step 2: Drop rows that are completely empty
    df = df.dropna(how='all')

    if df.shape[1] == 0:
        raise ValueError("No columns left after dropping empty columns")

    # Step 3: Forward fill missing values
    df = df.ffill()

    # Step 4: Rename columns to have meaningful names
    num_columns = df.shape[1]
    if num_columns >= 5:
        df.columns = ['Date', 'Description', 'Debit', 'Credit', 'Balance'] + [f'Extra_{i}' for i in range(num_columns - 5)]
    else:
        raise ValueError(f"Unexpected number of columns: {num_columns}")

    # Step 5: Remove rows where 'Date' is still NaN
    df = df.dropna(subset=['Date'])

    # Step 6: Reset the index for a clean DataFrame
    df.reset_index(drop=True, inplace=True)

    return df


def save_to_database(df):
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
