import fitz  # PyMuPDF
import streamlit as st

def ingest_pdf(uploaded_file):
    """Extracts text from PDF simply and fast."""
    try:
        # Reset file pointer to beginning
        uploaded_file.seek(0)
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def search_database(query, menu_text):
    """Simply returns the full menu text for Gemini to analyze."""
    return menu_text