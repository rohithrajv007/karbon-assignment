# PDF Redaction + Universal Bank Statement Parser

![PDF Redaction and Parsing](https://img.shields.io/badge/Status-Active-brightgreen)  
![Python](https://img.shields.io/badge/Python-3.10+-blue)  
![Streamlit](https://img.shields.io/badge/Streamlit-Yes-orange)

---

## Overview

This project is a **powerful, browser-based tool** that allows you to:

1. **Redact sensitive information** in PDF files directly in your browser.
2. **Parse bank statements from any bank** and extract structured transaction data (date, description, debit, credit, balance) in JSON format using AI.

The tool is **universal** and works for various banks, formats, and transaction types. No manual configuration is required.

---

## Features

### 1. PDF Redaction Tool
- **Interactive redaction**: Draw rectangles over sensitive data like account numbers or personal details.
- **Undo functionality**: Easily undo the last redaction.
- **Download redacted PDF**: Save a fully redacted version for secure sharing.
- **Browser-based**: No file leaves your computer; your data stays private.

### 2. Universal Bank Statement Parser
- **AI-powered parsing**: Uses a large language model (LLM) to read raw text from PDFs and extract transactions.
- **Works on any bank**: Automatically handles different statement formats without manual rules.
- **Structured JSON output**: Each transaction includes:
  - Transaction Date (DD-MM-YYYY)
  - Description
  - Debit Amount (0 if none)
  - Credit Amount (0 if none)
  - Balance after transaction
- **Chunking for large PDFs**: Handles long statements by splitting them into manageable chunks for AI processing.
- **Downloadable JSON**: Export parsed transactions for further analysis.

---

## Output Examples

Here are some screenshots of the tool in action:

1. **PDF Redaction Interface**  
![Redaction Interface](Screenshot%202025-10-03%20152957.png)

2. **Drawing Redaction Rectangles**  
![Drawing Redaction](Screenshot%202025-10-03%20153437.png)

3. **Redacted PDF Preview**  
![Redacted PDF](Screenshot%202025-10-03%20153446.png)

4. **Parsed Transaction JSON Preview**  
![JSON Preview](Screenshot%202025-10-03%20160340.png)

5. **Download Parsed JSON**  
![Download JSON](Screenshot%202025-10-03%20160358.png)

---

## Tech Stack

- **Frontend / UI**:
  - HTML, TailwindCSS
  - PDF.js for rendering PDF pages
  - pdf-lib for redaction and saving
- **Backend / AI Processing**:
  - Python 3.10+
  - Streamlit for web app interface
  - pdfplumber for text extraction from PDFs
  - OpenAI / OpenRouter API for AI-powered parsing

---

## How It Works

1. **Upload a PDF**: Start by uploading your PDF statement.
2. **Redact sensitive information**:  
   - Use your mouse to draw rectangles over sensitive info.
   - Click "Undo" if you make a mistake.
   - Click "Download Redacted PDF" to save.
3. **Parse Bank Statement**:
   - Upload the redacted (or original) PDF.
   - Click "Parse Statement."
   - The AI reads the text and extracts all transactions into a **clean JSON format**.
   - Download the parsed transactions for analysis or record-keeping.

The AI parser handles **multiple banks and varying statement layouts** automatically, making it universal.

---

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/pdf-bank-parser.git
cd pdf-bank-parser
Install dependencies

bash
Copy code
pip install -r requirements.txt
Setup API Key

Store your OpenRouter / OpenAI API key in a .env file:

env
Copy code
OPENROUTER_API_KEY="your_api_key_here"
Load the key in your app:

python
Copy code
from dotenv import load_dotenv
import os

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
Run the Streamlit app

bash
Copy code
streamlit run app.py
Open your browser
Go to http://localhost:8501 to access the app.

Usage
Open the app in your browser.

Step 1: Redact Sensitive Information

Upload any PDF and draw rectangles over the data you want to hide.

Download the redacted PDF.

Step 2: Parse Bank Statement

Upload the redacted (or original) PDF.

Click "Parse Statement."

Wait for AI to extract transactions.

Download JSON of transactions.

Example Output
json
Copy code
[
  {
    "transaction_date": "01-10-2025",
    "description": "Amazon Purchase",
    "debit": 1500.00,
    "credit": 0,
    "balance": 10000.50
  },
  {
    "transaction_date": "02-10-2025",
    "description": "Salary Credit",
    "debit": 0,
    "credit": 50000.00,
    "balance": 60000.50
  }
]
Advantages
Fully universal for all banks

Easy browser-based PDF redaction

Clean JSON transaction extraction

No manual parsing or rules needed

Maintains user privacy

Future Improvements
Add automatic detection of sensitive fields for redaction.

Support CSV export along with JSON.

Enhance UI/UX for mobile devices.

Add multi-language support for international bank statements.

