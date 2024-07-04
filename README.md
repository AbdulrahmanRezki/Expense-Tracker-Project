# Bank Statement Management System

## Overview

This project is a comprehensive bank statement management system designed to help users securely authenticate, process bank statement PDFs, extract and visualize data, and receive results via email. It uses a range of Python libraries including PySimpleGUI, sqlite3, pdfplumber, and yagmail to provide a seamless and efficient user experience.

## Features

- **User Authentication**
  - Secure login and registration using SHA-256 password hashing.
  - Credentials stored in an SQLite database.

- **PDF Bank Statement Processing**
  - Support for encrypted and unencrypted PDFs.
  - Decryption of PDFs using user-provided passwords.
  - Extraction and cleaning of table data from PDFs.
  - Storage of extracted data in an SQLite database.

- **Data Visualization**
  - Generation of bar charts to visualize bank balances over time.
  - Saving of visualizations as image files.

- **Email Notifications**
  - Option to receive visualized data via email.
  - Integration with yagmail for sending emails.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python libraries:
  - PySimpleGUI
  - sqlite3
  - hashlib
  - pdfplumber
  - PyPDF2
  - pandas
  - matplotlib
  - yagmail
