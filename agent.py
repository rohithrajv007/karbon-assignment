import streamlit as st
import streamlit.components.v1 as components
import pdfplumber
import json
from openai import OpenAI

OPENROUTER_API_KEY = "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"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

MODEL = "x-ai/grok-4-fast:free"

st.set_page_config(page_title="PDF Redaction + Parser", layout="wide")
st.title("PDF Redaction + Universal Bank Statement Parser")

st.markdown("""
### Step 1: Redact Sensitive Information
Use the interactive PDF redaction tool below. Draw rectangles over sensitive info and download the redacted PDF.
""")

# -------------------- HTML PDF Redaction Tool --------------------
with open("pdfeditor.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=800, scrolling=True)

# -------------------- Step 2: Bank Statement Parser --------------------


def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text

def chunk_text(text, max_len=2800):
    lines = text.split('\n')
    chunks = []
    current_chunk = []
    current_len = 0
    for line in lines:
        line_len = len(line) + 1
        if current_len + line_len > max_len:
            chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_len = line_len
        else:
            current_chunk.append(line)
            current_len += line_len
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    return chunks

def call_llm(chunk, chunk_index, total_chunks):
    prompt = f"""
You are an AI expert bank statement parser.

Input is raw bank statement text with transactions in variable formats.

Your task:
For each transaction in this text chunk, extract & assign values to these variables:
- transaction date (DD-MM-YYYY format)
- description of transaction (full details)
- debit amount (money withdrawn, 0 if none)
- credit amount (money added, 0 if none)
- balance after transaction

Ensure:
- Assign correct values to all variables, inferring missing info if needed.
- Debit and credit are mutually exclusive per transaction.
- Output ONLY JSON array of transactions, no explanations.

This is part {chunk_index} of {total_chunks} input text:
{chunk}

text
Output JSON:
"""
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a bank statement parser. Output ONLY the valid JSON array."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000,
        temperature=0,
    )
    response = completion.choices[0].message.content.strip()

    # Try to fix truncated closing bracket in response
    if not response.endswith(']'):
        response += ']'

    try:
        transactions = json.loads(response)
    except Exception as e:
        st.error(f"JSON parsing error in chunk {chunk_index}: {e}")
        st.text_area(f"LLM raw output chunk {chunk_index}:", response, height=300)
        raise e
    return transactions

def parse_pdf_statements(file):
    raw_text = extract_text(file)
    chunks = chunk_text(raw_text)
    all_transactions = []
    for idx, chunk in enumerate(chunks, 1):
        txs = call_llm(chunk, idx, len(chunks))
        all_transactions.extend(txs)
    return all_transactions

st.title("Universal Bank Statement Parser")
st.write("Upload any bank statement PDF; AI will assign values to transaction date, description, debit, credit, balance.")

uploaded = st.file_uploader("Upload PDF", type="pdf")

if uploaded:
    if st.button("Parse Statement"):
        try:
            with st.spinner("Extracting and parsing the statement..."):
                result = parse_pdf_statements(uploaded)
            st.success(f"Parsed {len(result)} transactions.")
            st.json(result)
            json_str = json.dumps(result, indent=2)
            st.download_button("Download JSON", data=json_str, file_name="transactions.json", mime="application/json")
        except Exception as err:
            st.error(f"Error parsing PDF: {err}")